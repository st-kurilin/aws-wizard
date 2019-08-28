import sys

import cert
import cloudfront
import route53
import s3


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    domain=sys.argv[1]
    path=sys.argv[2]

    print("=======Step 1/3: Publish Content to S3 Buckets=======")
    (s3_website, s3_recordsset) = s3.obtain_web_bucket(domain)
    s3.sync(domain, path)
    print(f"=======Step 1/3 Completed: Content available by http://{s3_website} =======")
    print("=======Step 2/3: Configure Domain=======")
    #TODO implement
    print(f"=======Step 2/3 Completed: Content available by http://{domain} =======")
    print("=======Step 3/3: Configure HTTPS=======")
    (cert, cert_recordsset) = cert.cert_and_recordsets(domain)
    route53.add_recordsset(domain, cert_recordsset)
    route53.add_recordsset(domain, cloudfront.recordsset(domain, cert, "index.html"))
    route53.add_recordsset(domain, cloudfront.recordsset(f"www.{domain}", cert, ""))
    print(f"=======Step 3/3 Completed: Content available by https://{domain} =======")


