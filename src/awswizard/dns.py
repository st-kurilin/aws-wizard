import logging
import subprocess
import time

from .aws import route53


def wait_for_dns_config(domain):
    ns_servers = route53.get_ns_servers(domain)
    dns_ok = _check(domain, ns_servers)
    if not dns_ok:
        print("Please add NS records to your DNS")
        print("\n".join(ns_servers))
        print ()
        print(
        "It's the only manual step required. Don't worry, here are some tutorials:")  # todo: move to separate page
        print("GoDaddy:         https://www.godaddy.com/help/add-an-ns-record-19212")
        print("Google Domains:  https://support.google.com/domains/answer/6353515")
        print("namecheap:       https://www.namecheap.com/support/knowledgebase/article.aspx/434/2237")
        print ()
        print(
        "After you update DNS it could take up to 48 hours to take effect. It's safe to re-run this script later. But let's hope it would work faster.")
        print ()
        while not dns_ok:
            time.sleep(30)
            dns_ok = _check(domain, ns_servers)
            print(
            "NS records doesn't match. It could be because you didn't update it yet or changes not propagated yet. We'll check it again in a bit.")


def _check(domain, expected):
    actual = _get_actual(domain)
    matched = len(set(actual) & set(expected))
    logging.debug(f"Checking dns records for {domain}. {matched} matched. Actual {actual}, Expected: {expected}")
    return matched >= 2  # two is a number that provides a single backup. It's more likely to be four.


def _get_actual(domain):
    res = subprocess.run([f"whois {domain}"],
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    if res.returncode != 0:
        raise Exception(f"exec errorcode {res.returncode}: {res.stdout}/ {res.stderr}")
    else:
        return [f"{l.split()[2].lower()}." for l in res.stdout.decode('utf-8').splitlines() if
                l.startswith("Name Server:")]
