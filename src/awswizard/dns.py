import subprocess
import logging

def check(domain, expected):
    actual = _get_actual(domain)
    matched = len(set(actual) & set(expected))
    logging.debug(f"Checking dns records for {domain}. {matched} matched. Actual {actual}, Expected: {expected}")
    return matched >= 2 # two is a number that provides a single backup. It's more likely to be four.

def _get_actual(domain):
    res = subprocess.run([f"whois {domain}"],
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    if res.returncode != 0:
        raise Exception(f"exec errorcode {res.returncode}: {res.stdout}/ {res.stderr}")
    else:
        return [f"{l.split()[2].lower()}." for l in res.stdout.decode('utf-8').splitlines() if l.startswith("Name Server:")]