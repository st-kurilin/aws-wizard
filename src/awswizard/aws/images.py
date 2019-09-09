import logging

from .u import aws


def find_ubuntu_ami():
    return "ami-0e0256d97a585c486"
    query = 'reverse(sort_by(Images,&CreationDate))[0:100][ImageId, Description]'
    ebs = "Name=root-device-type,Values=ebs"
    available = 'Name=state,Values=available'
    res = aws(f"aws ec2 describe-images --owners 099720109477 --query '{query}' --filters {ebs} {available}")
    for l in res.splitlines():
        if "UNSUPPORTED" in l:
            continue
        if "LTS" in l:
            [ami, desc] = l.split(maxsplit=1)
            logging.debug(f"Selected image: {ami} / {desc}")
            return ami
    raise Exception("Failed to find ubuntu ami")
