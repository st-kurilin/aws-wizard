from u import exec
import json
import logging

def obtain_web_bucket(name):
    logging.info(f"configuring s3 bucket {name}")
    _make_sure_bucket_exists(name)
    _serve_web(name)
    _make_public(name)

    www = f"www.{name}"
    logging.info(f"configuring s3 bucket {www}")
    _make_sure_bucket_exists(www)
    _make_public(www)

    _redirect_www(name)

def sync(domain, dir):
    exec (f"aws s3 sync {dir} s3://{domain}/ --delete")


def _make_sure_bucket_exists(name):
    found = [l for l in exec("aws s3 ls").splitlines() if l.endswith(name)]
    if len(found) > 0:
        logging.debug(f"bucket {name} already exists")
    else:
        exec(f"aws s3 mb s3://{name}")


def _serve_web(name):
    exec(f"aws s3 website s3://{name}/ --index-document index.html --error-document error.html")


def _make_public(name):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{name}/*"
            }
        ]
    }
    exec(f"aws s3api put-bucket-policy --bucket {name} --policy '{json.dumps(policy)}'")

def _redirect_www(name):
    conf = {
        "RedirectAllRequestsTo": {
            "HostName": name,
            "Protocol": "https"
        }
    }
    exec(f"aws s3api put-bucket-website --bucket www.{name} --website-configuration '{json.dumps(conf)}'")
