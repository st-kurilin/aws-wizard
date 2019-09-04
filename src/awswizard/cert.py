import logging
from .u import exec


def cert_and_recordsets(domain):
    logging.debug(f"Getting validated cert for {domain}")
    cert = _obtain_certificate(domain)
    cert_unvalid_status = _get_certificate_non_success_status(cert)
    if cert_unvalid_status is not None:
        logging.debug(f"Certificate is not valid yet {cert}: {cert_unvalid_status}. Will add records and check again.")
        return (cert, _get_certificate_validation_records(cert))
    else:
        logging.debug(f"Valid cert already exist {cert}")
        return (cert, [])

def _obtain_certificate(domain):
    arn = _get_cert(domain)
    if arn is None:
        return _request_certificate(domain)
    else:
        logging.debug(f"Reusing already created cert {arn}")
        return arn


def _get_certificate_non_success_status(arn):
    logging.debug(f'Searching for cert statuses {arn}')
    loaded = exec(f'aws acm describe-certificate --certificate-arn {arn} --output text')
    statuses = [line.split()[4] for line in loaded.splitlines() if
                line.startswith("DOMAINVALIDATIONOPTIONS")]
    logging.debug(f"reported statuses {statuses}")
    for s in statuses:
        if s != 'SUCCESS':
            logging.debug(f"cert {arn} is not valid due partial status {s}")
            return s
    logging.debug(f"cert {arn} indicated as valid")
    return None


def _get_certificate_validation_records(arn):
    loaded = exec(f'aws acm describe-certificate --certificate-arn {arn} --output text')
    return [{
                "Name": l.split()[1],
                "Type": "CNAME",
                "TTL": 300,
                "ResourceRecords": [{"Value": l.split()[3]}]
            } for l in loaded.splitlines() if l.startswith('RESOURCERECORD')]


def _get_cert(domain):
    logging.debug(f'Searching cert for {domain}')
    loaded = exec(f'aws acm list-certificates --output text')
    matched = [line.split()[1] for line in loaded.splitlines() if line.split()[2] == domain]
    if len(matched) > 0:
        res = matched[0]
        logging.debug(f"found matching certificates {matched}. will use {res}")
        return res
    else:
        logging.debug(f"Did not find any cert for {domain}")
        return None


def _request_certificate(domain):
    logging.debug(f'Requesting certificate for {domain}')
    arn = exec(f'aws acm request-certificate --domain-name {domain} --validation-method DNS  --subject-alternative-names www.{domain}').strip()
    logging.debug(f"Certificate requested: {arn}")
    return arn
