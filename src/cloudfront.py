import json

from u import exec


def recordsset(domain, s3_website, cert, root_object):
    dist = _get_distribution(domain)
    if dist is None:
        print(f"Distribution for {domain} not found. Will create new one")
        _create_distribution(domain, s3_website, cert, root_object)
        return _wrap_in_recordsset(domain, _get_distribution(domain)['dist_domain'])
    else:
        print(f"Distribution for {domain} already exist: {dist['dist_domain']}")
        if dist['enabled'] is False: raise Exception(f"distribution found, but it's not enabled")
        if dist['cert'] != cert: raise Exception(f"distribution found, but it has different certificate")
        return _wrap_in_recordsset(domain, dist['dist_domain'])


def _wrap_in_recordsset(domain, dist_domain):
    if dist_domain is None:
        return []
    else:
        return [{
            "AliasTarget": {
                "HostedZoneId": "Z2FDTNDATAQYW2",  # const from docs https://stackoverflow.com/a/39669786/230717
                "EvaluateTargetHealth": False,
                "DNSName": f"{dist_domain}."
            },
            "Type": "A",
            "Name": f"{domain}."
        }]


def _get_distribution(domain):
    res = exec(
        f'aws cloudfront list-distributions --output text --query "DistributionList.Items[*].[Aliases.Items[0], DomainName, Enabled, ViewerCertificate.ACMCertificateArn]"')
    found = [{"dist_domain": l.split()[1], "enabled": l.split()[2] == "True", "cert": l.split()[3]}
             for l in res.splitlines() if l.startswith(domain)]
    return found[0] if found else None


def _create_distribution(domain, s3_website, cert, root_object):
    config = {
        "CallerReference": f"dist-{domain}",
        "Aliases": {
            "Items": [
                domain
            ],
            "Quantity": 1
        },
        "DefaultRootObject": root_object,
        "Origins": {
            "Quantity": 1,
            "Items": [
                {
                    "Id": f"S3-Website-{s3_website}",
                    "DomainName": s3_website,
                    "CustomOriginConfig": {
                        "OriginSslProtocols": {
                            "Items": [
                                "TLSv1",
                                "TLSv1.1",
                                "TLSv1.2"
                            ],
                            "Quantity": 3
                        },
                        "OriginProtocolPolicy": "http-only",
                        "OriginReadTimeout": 30,
                        "HTTPPort": 80,
                        "HTTPSPort": 443,
                        "OriginKeepaliveTimeout": 5
                    },
                }
            ]
        },
        "HttpVersion": "http2",
        "DefaultCacheBehavior": {
            "TargetOriginId": f"S3-Website-{s3_website}",
            "ViewerProtocolPolicy": "redirect-to-https",
            "MinTTL": 0,
            "TrustedSigners": {
                "Enabled": False,
                "Quantity": 0
            },
            "ForwardedValues": {
                "Headers": {
                    "Quantity": 0
                },
                "Cookies": {
                    "Forward": "none"
                },
                "QueryString": True
            },
        },
        "CacheBehaviors": {
            "Quantity": 0
        },

        "ViewerCertificate": {
            "SSLSupportMethod": "sni-only",
            "ACMCertificateArn": cert,
            "MinimumProtocolVersion": "TLSv1.1_2016",
            "Certificate": cert,
            "CertificateSource": "acm"
        },
        "Comment": "auto",
        "Logging": {
            "Enabled": False,
            "IncludeCookies": True,
            "Bucket": "",
            "Prefix": ""
        },
        "PriceClass": "PriceClass_100",  # PriceClass_All
        "Enabled": True
    }
    try:
        exec(f"aws cloudfront create-distribution --distribution-config '{json.dumps(config)}'")
    except Exception as e:
        if "CNAMEAlreadyExists" in str(e):
            print("cloudfront distribution already exist for this domain")
        else:
            raise e
