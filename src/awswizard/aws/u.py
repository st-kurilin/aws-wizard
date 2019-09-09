import logging
import subprocess


def aws(_cmd):
    cmd = f"{_cmd.strip()}{'' if '--region' in _cmd else ' --region us-east-1'}{'' if '--output' in _cmd else ' --output text'}"
    logging.debug(f"exec: >{cmd}<")
    res = subprocess.run([cmd],
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    logging.debug(f"exec completed {res.returncode}")
    if res.returncode != 0:
        raise Exception(f"exec errorcode {res.returncode}: {res.stdout}/ {res.stderr}")
    else:
        out = res.stdout.decode('utf-8')
        if out is None:
            return ""
        out = out.strip()
        if out == "None":
            return ""
        else:
            return out


# DEPRECATED: use u.aws
def exec(_cmd):
    return aws(_cmd)
