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


def create_image(ins_id, name):
    return aws(f"aws ec2 create-image --instance-id {ins_id} --name '{name}' --no-reboot --query ImageId")


def get_my_images():
    return aws(f"aws ec2 describe-images --owners self --query Images[0].Name").splitlines()

def find_own_image_by_name(name):
    return aws(f"aws ec2 describe-images --owners self --filters 'Name=name,Values={name}' --query Images[0].ImageId")


def delete_image(image_id):
    return aws(f"aws ec2 deregister-image --image-id {image_id}")
