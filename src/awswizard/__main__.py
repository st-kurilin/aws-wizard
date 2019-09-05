import argparse
import logging
import sys
import time

from . import cert
from . import cloudfront
from . import dns
from . import route53
from . import s3

def publish_static(domain, directory):
    print("=======Step 1/3: Publish Content to S3 Buckets=======")
    (s3_website, s3_recordsset) = s3.obtain_web_bucket(domain)
    s3.sync(domain, directory)
    print(f"=======Step 1/3 Completed: Content available by http://{s3_website} =======")
    print("=======Step 2/3: Configure Domain=======")
    route53.add_recordsset(domain, s3_recordsset)
    ns_servers = route53.get_ns_servers(domain)
    dns_ok = dns.check(domain, ns_servers)
    if not dns_ok:
        print("Please add NS records to your DNS")
        print("\n".join(ns_servers))
        print ()
        print("It's the only manual step required. Don't worry, here are some tutorials:") #todo: move to separate page
        print("GoDaddy:         https://www.godaddy.com/help/add-an-ns-record-19212")
        print("Google Domains:  https://support.google.com/domains/answer/6353515")
        print("namecheap:       https://www.namecheap.com/support/knowledgebase/article.aspx/434/2237")
        print ()
        print("After you update DNS it could take up to 48 hours to take effect. It's safe to re-run this script later. But let's hope it would work faster.")
        print ()
        while not dns_ok:
            time.sleep(30)
            dns_ok = dns.check(domain, ns_servers)
            print("NS records doesn't match. It could be because you didn't update it yet or changes not propagated yet. We'll check it again in a bit.")
    print(f"=======Step 2/3 Completed: Content available by http://{domain} =======")
    print("=======Step 3/3: Configure HTTPS=======")
    (cert_val, cert_recordsset) = cert.cert_and_recordsets(domain)
    route53.add_recordsset(domain, cert_recordsset)
    if len(cert_recordsset) != 0:
        print("Issuing ssl certificate can take some time. No manual actions required.")
        while len(cert_recordsset) != 0:
            time.sleep(30)
            (cert_val, cert_recordsset) = cert.cert_and_recordsets(domain)
            print("Waiting for certificate [no actions required].")
        print("Certificate issues and validated.")

    route53.add_recordsset(domain, cloudfront.recordsset(domain, s3_website, cert_val, "index.html"))
    route53.add_recordsset(domain, cloudfront.recordsset(f"www.{domain}", s3_website, cert_val, ""))
    print(f"=======Step 3/3 Completed: Content will be available soon at https://{domain} =======")

def update_static(domain, directory):
    print("=======Step 1/2: Sync S3 Bucket=======")
    s3.sync(domain, directory)
    print(f"=======Step 1/2 S3 Content Updated =======")
    print("=======Step 2/2: Invalidate CloudFront Distribution=======")
    is_invalidation_completed_func = cloudfront.invalidate(domain)
    time.sleep(15)
    invalidation_completed = is_invalidation_completed_func()
    while not invalidation_completed:
        print(f"Waiting for CloudFront invalidation to complete...")
        time.sleep(30)
        invalidation_completed = is_invalidation_completed_func()
    print("=======Step 2/2: CloudFront invalidated. New content should in 5-10 minutes.=======")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AWS made easy.')
    parser.add_argument('--verbose', '-V', help='Give more output.', action="store_true", default=False)
    subparsers = parser.add_subparsers(help='commands')

    list_parser = subparsers.add_parser('static_website', help='Publish static website')
    list_parser.add_argument('domain', help='Your domain', metavar='yourdomain.com', default="")
    list_parser.add_argument('--directory', '-d', help='Local directory to publish', metavar='./content',default='./')

    list_parser = subparsers.add_parser('update_static', help='Update static content. Works faster than static_website command')
    list_parser.add_argument('domain', help='Your domain', metavar='yourdomain.com', default="")
    list_parser.add_argument('--directory', '-d', help='Local directory to publish', metavar='./content',default='./')

    list_parser = subparsers.add_parser('publish_lambda', help='Publish lambda function')
    list_parser.add_argument('file',  help='Path to local file', default='./main.py')

    args = parser.parse_args()  #should be called before "if" to support "awswizard -h"
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.WARNING))
    if "static_website" in sys.argv:
        publish_static(args.domain, args.directory)
    elif "update_static" in sys.argv:
        update_static(args.domain, args.directory)
        print ("------------------------")
    else:
        raise Exception("Failed to parse arguments.\nTo get assistance run "
                        "'python -m awswizard -h' or visit aws-wizard.com ")
    print ("------------------------2")

