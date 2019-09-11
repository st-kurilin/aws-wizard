import json
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
        return specified
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


def _is_instances_ready(tag):
    def res():
        for instance in find_instances_by_tag(tag):
            if instance['state'] != 'running':
                logging.debug(f"Instance {instance['id']} state is {instance['state']}. Expected: running.")
                return False
            else:
                status = _get_instance_status(instance['id'])
                if status != "ok":
                    logging.debug(f"Instance {instance['id']} status is {status}. Expecting ok.")
                    return False
        logging.debug(f"Instances {tag} ready.")
        return True

    return res


def run_instance(tag, ami, keys):
    ins_id = aws(f"aws ec2 run-instances"
                 f" --image-id {ami}"
                 f" --instance-type t2.nano --key-name {keys} --query 'Instances[0].InstanceId'")
    time.sleep(5)
    aws(f"aws ec2 create-tags --resources {ins_id}  --tags Key={NAME_TAG},Value={tag}")
    group = _obtain_security_group("awswizard-public", [22, 80])
    aws(f"aws ec2 modify-instance-attribute --instance-id {ins_id} --groups {group}")

    return [ins_id, find_instances_by_tag(tag)[0]['ip'], lambda: _is_instances_ready(tag)]


def terminate_instances(tag):
    all = find_instances_by_tag(tag)
    if len(all) == 0:
        return [None, lambda: True]
    else:
        ids = []
        for ins in all:
            ids.append(ins['id'])
            aws(f"aws ec2 terminate-instances --instance-ids {ins['id']}")
        return [ids, lambda: len(find_instances_by_tag(tag)) == 0]


def find_instances_by_tag(tag):
    res = aws(f"aws ec2 describe-instances"
              f" --filter Name=tag:{NAME_TAG},Values={tag} "
              f"--query 'Reservations[*].Instances[0].[InstanceId, PublicIpAddress, State.Name]'")
    return [{"id": ins[0], "ip": ins[1], "state": ins[2]}
            for ins in [l.split() for l in res.splitlines()] if ins[2] != "terminated"]


def find_server_names():
    res = aws(f"aws ec2 describe-instances"
              f" --filter Name=tag-key,Values={NAME_TAG} "
              f"--query 'Reservations[*].Instances[0].[InstanceId, PublicIpAddress, State.Name, Tags[?Key==`{NAME_TAG}`]|[0].Value]'")
    names = [ins[3] for ins in [l.split() for l in res.splitlines()] if ins[2] != "terminated"]
    return list(set(names))


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


def create_launch_template(name, ami, keys):
    try:
        aws(f"aws ec2 delete-launch-template --launch-template-name {name}")
    except:
        pass  # template doesn't exist

    sec_group = _obtain_security_group("awswizard-public", [22, 80])
    logging.debug(f"Security group to be used for launch template: {sec_group}")
    data = {
        "SecurityGroupIds": [sec_group],
        "ImageId": ami,
        "InstanceType": "t2.nano",
        "KeyName": keys,
        "TagSpecifications": [
            {"ResourceType": "instance", "Tags": [{"Key": NAME_TAG, "Value": name}]}
        ]
    }
    res = aws(f"aws ec2 create-launch-template --launch-template-name {name}"
              f" --launch-template-data '{json.dumps(data)}'"
              f" --query LaunchTemplate.LaunchTemplateId")
    logging.debug(f"Launch Template {name} created({res})")
    return res


def create_target_group(name):
    vpc = _get_vpc_id()
    res = aws(f"aws elbv2 create-target-group --name {name} "
              f" --protocol TCP --port 80 --vpc-id {vpc} --query TargetGroups[0].TargetGroupArn")
    logging.debug(f"Target group {name} created({res})")
    return res


def create_auto_scaling_group(name, template_name, target_group, min, max):
    vpc = _get_vpc_id()
    subnets = aws(f"aws ec2 describe-subnets "
                  f"--filters 'Name=vpc-id,Values={vpc}' --query 'Subnets[*].SubnetId'").split()
    logging.debug(f"Subnets in VPC {vpc}: {subnets}")
    try:
        res = aws(f"aws autoscaling create-auto-scaling-group --auto-scaling-group-name {name} "
                  f" --launch-template LaunchTemplateName={template_name} "
                  f" --min-size {min} --max-size {max} "
                  f" --target-group-arns {target_group} --vpc-zone-identifier {','.join(subnets)}")
        logging.debug(f"Auto scaling group {name} created({res})")
        return _is_instances_ready(name)
    except Exception as e:
        if "AlreadyExists" in str(e):
            logging.debug(f"Auto scaling group {name} already exists")
            return lambda: True
        else:
            raise e


def delete_auto_scaling_group(name):
    try:
        return aws(f"aws autoscaling delete-auto-scaling-group --force-delete  --auto-scaling-group-name {name}");
    except:
        pass  # doesnt exist?


def create_load_balancer(name, target_group, domain):
    def _wrap_in_recordsset(dns):
        if domain == "":
            return []
        else:
            return [{
                "AliasTarget": {
                    # const from docs https://docs.aws.amazon.com/general/latest/gr/rande.html
                    "HostedZoneId": "Z26RNL4JYFTOTI",
                    "EvaluateTargetHealth": False,
                    "DNSName": f"{dns}."
                },
                "Type": "A",
                "Name": f"{domain}."
            }]
    vpc = _get_vpc_id()
    subnets = aws(f"aws ec2 describe-subnets "
                  f" --filters 'Name=vpc-id,Values={vpc}' --query 'Subnets[*].SubnetId'").split()
    logging.debug(f"Subnets in VPC {vpc}: {subnets}")
    lb = aws(f"aws elbv2 create-load-balancer --name {name} "
             f" --type network --subnets {' '.join(subnets)} --query LoadBalancers[0].LoadBalancerArn")
    logging.debug(f"Load balancer created {lb}")
    listener = aws(f"aws elbv2 create-listener --load-balancer-arn {lb} "
                   f" --protocol TCP --port 80  --default-actions Type=forward,TargetGroupArn={target_group}")
    logging.debug(f"Listener to connect load balancer {lb} with target group {target_group} created: {listener}")
    dns = aws(f"aws elbv2 describe-load-balancers --load-balancer-arns {lb} --query LoadBalancers[0].DNSName")
    return [dns, _wrap_in_recordsset(dns)]


def delete_load_balancer(name):
    arns = [lb["arn"] for lb in list_load_balancers() if lb["name"] == name]
    if len(arns) == 0:
        logging.debug(f"No load balancers with name {name} found")
    else:
        logging.debug(f"Going to delete load balancer {name} ({arns[0]})")
        aws(f"aws elbv2 delete-load-balancer --load-balancer-arn {arns[0]}")

def list_load_balancers():
    out = aws(f"aws elbv2 describe-load-balancers "
              f" --query LoadBalancers[*][LoadBalancerName,DNSName,LoadBalancerArn]")
    return [{"name": ll[0], "dns_name": ll[1], "arn": ll[2]}for ll in [l.split() for l in out.splitlines()]]


def _get_vpc_id():
    return aws("aws ec2 describe-vpcs --filters 'Name=isDefault, Values=true' --query=Vpcs[0].VpcId")
