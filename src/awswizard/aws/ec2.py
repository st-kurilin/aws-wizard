import logging
import os
import time

from .u import aws

NAME_TAG = "awswizard-name"
security_group_name = "awswizzard-sec-group"


def _get_aws_pairs():
    return [l.split()[1]
            for l in aws("aws ec2 describe-key-pairs "
                         " --region us-east-1  --output=text --query='KeyPairs'").splitlines()]


def get_keys_name(specified):
    available = _get_aws_pairs()
    if specified in available:
        logging.debug(f"Using SSH Key {specified} from AWS1")
        return input
    name = ''.join(os.path.basename(specified).split())  # filename without spaces
    if name in available:
        logging.debug(f"Using SSH Key {name} from AWS2")
        return name
    for path in [f"./{specified}.pub", f"~/.ssh/{specified}.pub", specified, f"~/.ssh/{specified}", ]:
        try:
            aws(f"aws ec2 import-key-pair --key-name '{name}' --public-key-material file://{path}")
            logging.debug(f"Using SSH Key {name} that was imported to AWS from {specified}")
            return name
        except:
            logging.debug(f"Failed to generate aws keys from {path}")
    return None


def run_instance(ami, tag, keys):
    def is_instance_ready():
        instance = find_instance_by_tag(tag)
        if instance['state'] != 'running':
            logging.debug(f"Instance {instance['id']} state is {instance['state']}. Expected: running.")
            return False
        else:
            status = _get_instance_status(instance['id'])
            if status != "ok":
                logging.debug(f"Instance {instance['id']} status is {status}. Expecting ok.")
                return False
            return True

    ins_id = aws(f"aws ec2 run-instances"
                 f" --image-id {ami}"
                 f" --instance-type t2.nano --key-name {keys} --query 'Instances[0].InstanceId'")
    time.sleep(5)
    aws(f"aws ec2 create-tags --resources {ins_id}  --tags Key={NAME_TAG},Value={tag}")
    group = _obtain_security_group("awswizard-public", [22, 80])
    aws(f"aws ec2 modify-instance-attribute --instance-id {ins_id} --groups {group}")

    return [ins_id, find_instance_by_tag(tag)['ip'], is_instance_ready]


def terminate_instance(tag):
    instance = find_instance_by_tag(tag)
    if instance is None:
        return [None, lambda: True]
    else:
        ins_id = instance['id']
        aws(f"aws ec2 terminate-instances --instance-ids {ins_id}")
        return [ins_id, lambda: find_instance_by_tag(tag) is None]


def find_instance_by_tag(tag):
    res = aws(f"aws ec2 describe-instances"
              f" --filter Name=tag:{NAME_TAG},Values={tag} "
              f"--query 'Reservations[*].Instances[0].[InstanceId, PublicIpAddress, State.Name]'")
    for l in res.splitlines():
        [ins_id, ip, state] = l.split()
        if state != "terminated":
            logging.debug(f"Instance by tag {tag}: {ins_id} ({state})")
            return {"id": ins_id, "ip": ip, "state": state}
    return None


def _get_instance_status(ins_id):
    out = aws(f"aws ec2 describe-instance-status --instance-ids {ins_id}"
              f" --query 'InstanceStatuses[0].[SystemStatus.Status,InstanceStatus.Status]'")
    non_ok = [s for s in out.split() if s != "ok"]
    return "ok" if len(non_ok) == 0 else non_ok[0]


def _obtain_security_group(name, open_ports):
    try:
        group = aws(f"aws ec2 describe-security-groups "
                    f"--group-names {name} --query 'SecurityGroups[*].[GroupId]'")
        logging.debug(f"Existing security group found for {name}: {group}")
        return group
    except:
        group = aws(f"aws ec2 create-security-group"
                    f" --group-name {name} --description 'aws-wizard'")
        logging.debug(f"Created new security group {group} for {name}")

        for p in open_ports:
            aws(f"aws ec2 authorize-security-group-ingress "
                f"--group-id {group} --protocol tcp --port {p} --cidr 0.0.0.0/0")
        return group
