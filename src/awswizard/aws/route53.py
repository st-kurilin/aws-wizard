import logging

from .u import exec

def get_ns_servers(domain):
    return _get_recorsets(domain, "NS")

def add_recordsset(domain, records):
    if len(records) > 0:
        hostedzone = _obtain_hostedzone(domain)
        logging.info(f'Adding records {len(records)} to hostedzone {hostedzone} for domain {domain}')
        _add_records_to_hostedzone(hostedzone, records)


def _obtain_hostedzone(domain):
    logging.debug(f'Obtaining hostedzone for {domain}')
    get = _get_hostedzone(domain)
    if get is None:
        created = _create_hostedzone(domain)
        if created is None:
            logging.debug(f'Will try to get hostedzone once again {domain}')
            get = _get_hostedzone(domain)
            if get is None:
                raise Exception(f"Failed to obtain hostedzone for {domain} ")
            else:
                return get
        else:
            return created
    else:
        return get


def _add_records_to_hostedzone(hostedzone, records):
    import json
    data = {'Changes': [{"Action": "UPSERT", "ResourceRecordSet": r} for r in records]}
    change_batch = json.dumps(data)
    logging.debug(change_batch)

    cc = f"aws route53 change-resource-record-sets --hosted-zone-id {hostedzone} --change-batch '{change_batch}'"
    exec(cc)


def _create_hostedzone(domain):
    logging.debug(f'Creating hostedzone for {domain}')
    loaded = exec(f'aws route53 create-hosted-zone --name {domain} --caller-reference {domain} --hosted-zone-config Comment="wizzard"')
    # handle HostedZoneAlreadyExists
    created = [l.split()[2].split("/")[2] for l in loaded.splitlines() if l.startswith("HOSTEDZONE")]
    logging.debug(f'Created hostedzones {created}')
    return created[0]


def _get_hostedzone(domain):
    logging.debug(f'Searching hostedzone for {domain}')
    stdout = exec(f'aws route53 list-hosted-zones-by-name --output text --query "HostedZones[*].[Name, Id]"')
    found = [l.split()[1].split("/")[2] for l in stdout.splitlines() if l.startswith(domain)]
    logging.debug(f'found hostzones: .')
    if len(found) > 0:
        res = found[0]
        logging.debug(f'found hostzones {found}. will return hostzone: {res}.')
        return res
    else:
        logging.debug(f'get_hostedzone did not find any hostzones.')
        return None

def _get_recorsets(domain, record_type):
    hostedzone = _obtain_hostedzone(domain)
    stdout = exec(f"aws route53 list-resource-record-sets --hosted-zone-id {hostedzone} --output text")
    res = []
    in_flag = False
    for l in stdout.splitlines():
        splitted = l.split()
        if splitted[0] == "RESOURCERECORDSETS" and len(splitted) == 4 and \
                        splitted[1] == f"{domain}." and splitted[3] == record_type:
            in_flag = True
        else:
            if in_flag:
                if splitted[0] == "RESOURCERECORDS":
                    res.append(splitted[1])
                else:
                    in_flag = False

    return res
