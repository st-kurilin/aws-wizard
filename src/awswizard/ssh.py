import subprocess
import logging


def generate_ssh(domain, expected):
    res = subprocess.run([f"ssh-keygen -t rsa -N ''"],
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    if res.returncode != 0:
        raise Exception(f"exec errorcode {res.returncode}: {res.stdout}/ {res.stderr}")

def login_to_server(user, ip, keys):
    res = subprocess.run([f"ssh -oStrictHostKeyChecking=no -i {keys} {user}@{ip} "],
                         shell=True)
    if res.returncode == 127 or res.returncode == 130:
        # regular exit?
        logging.debug(f"SSH executed with exit code {res.returncode}. Should be fine..")
        return
    if res.returncode != 0:
        raise Exception(f"exec errorcode {res.returncode}: {res.stdout}/ {res.stderr}")
