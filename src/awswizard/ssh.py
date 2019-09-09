import subprocess


def generate_ssh(domain, expected):
    res = subprocess.run([f"ssh-keygen -t rsa -N ''"],
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    if res.returncode != 0:
        raise Exception(f"exec errorcode {res.returncode}: {res.stdout}/ {res.stderr}")
