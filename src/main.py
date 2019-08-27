import sys
import logging

import cert
import cloudfront
import route53
import s3


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    domain=sys.argv[1]
    path=sys.argv[2]

    s3.obtain_web_bucket(domain)
    s3.sync(domain, path)
    (cert, cert_recordsset) = cert.cert_and_recordsets(domain)
    route53.add_recordsset(domain, cert_recordsset)
    route53.add_recordsset(domain, cloudfront.recordsset(domain, cert, "index.html"))
    route53.add_recordsset(domain, cloudfront.recordsset(f"www.{domain}", cert, ""))

