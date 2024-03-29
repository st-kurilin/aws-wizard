import logging
import time

from . import dns
from . import ssh
from .aws import ec2
from .aws import images
from .aws import route53


def register_commands(parser):
    sp = parser.add_parser('run-server', help="Run AWS instance with name if doesn't exist")
    sp.add_argument('server_name', help='Server name', metavar='myserver', default="")
    sp.add_argument('--ami', help='Base AMI.', metavar='ami-1234', default='')
    sp.add_argument('--image-name', help='Your image that was created by freezing server', metavar='myimage',
                    default='')
    sp.add_argument('--ssh-keys', help='SSH keys to be used to access instance', metavar='./id_rsa.pub',
                    default='id_rsa', dest="keys")

    ls = parser.add_parser('list-servers', help="Lists all running servers")
    ls.add_argument('--name', help='Server name', metavar='myserver', default="")

    cp = parser.add_parser('connect-to-server', help="SSH to server")
    cp.add_argument('server_name', help='Server name', metavar='myserver', default="")
    cp.add_argument('--index', help='If there are more than one server with such name. Sorted by IP. 1-based indexes',
                    metavar='1', default="")
    cp.add_argument('--ip', help='If there are more than one server with such name. ', metavar='10.10.10.10',
                    default="")
    cp.add_argument('--ssh-keys', help='SSH keys that were used during server creation', metavar='./id_rsa',
                    default='id_rsa', dest="keys")

    ksp = parser.add_parser('kill-servers', help="Terminates AWS Instance")
    ksp.add_argument('name', help='Server name', metavar='myserver', default="")

    fp = parser.add_parser('create-image', help='Saves instance to image')
    fp.add_argument('server', help='Name for server that is running', metavar='myserver')
    fp.add_argument('--image-name', help='Image name. Default to server-name ', metavar='myimage', default='',
                    dest="image_name")

    parser.add_parser('list-images', help='Lists images created by current user')

    df = parser.add_parser('delete-image', help="Removes image")
    df.add_argument('image_name', help='Image name', metavar='myimage', default="")

    ssp = parser.add_parser('run-cluster', help='Runs scalable group of servers')
    ssp.add_argument('cluster_name', help='Name for server group', metavar='mygroup')
    ssp.add_argument('--image-name', help='Name for image to run in group', metavar='myimage', dest="image_name",
                     required=True)
    ssp.add_argument('--domain', help='Domain name to be attached to server', metavar='mysite.com', default='')
    ssp.add_argument('--ssh-keys', help='SSH keys to be used to access instance', metavar='./id_rsa.pub',
                     default='id_rsa', dest="keys")
    ssp.add_argument('--min-size', help='Minimum number of instances. Default to 2',
                     metavar='2', default='2', type=int, dest="min_size")
    ssp.add_argument('--max-size', help='Maximum number of instances. Default to 5',
                     metavar='5', default='5', type=int, dest="max_size")

    parser.add_parser('list-clusters', help='Lists all clusters')

    dsp = parser.add_parser('kill-cluster', help='Deletes resources related to cluster')
    dsp.add_argument('cluster_name', help='Name for cluster', metavar='mycluster')




def exec_command(argv, args):
    if "run-server" in argv:
        server(args.server_name, args.ami, args.keys)
        return True
    if "list-servers" in argv:
        list_servers(args.name)
        return True
    if "connect-to-server" in argv:
        connect_to_server(args.server_name, args.keys, args.ip, args.index)
        return True
    elif "kill-servers" in argv:
        kill_server(args.name)
        return True
    elif "create-image" in argv:
        img = args.image_name if args.image_name != "" else args.server
        create_image(args.server, img)
        return True
    elif "list-images" in argv:
        list_images()
        return True
    elif "delete-image" in argv:
        delete_image(args.image_name)
        return True
    elif "run-cluster" in argv:
        img = args.image_name if args.image_name != "" else args.cluster_name
        run_cluster(args.cluster_name, img, args.domain, args.keys, args.min_size, args.max_size)
        return True
    elif "list-clusters" in argv:
        list_clusters()
        return True
    elif "kill-cluster" in argv:
        delete_cluster(args.cluster_name)
        return True
    else:
        return False


def server(name, image_ami, keys):
    exists = ec2.find_instances_by_tag(name)
    if len(exists) != 0:
        print (f"Instance with name {name} already exists: {instance['id']}")
        print (instance['ip'])
    else:
        print (f"Spanning new server with name {name}.")
        ami = image_ami if image_ami != "" else images.find_ubuntu_ami()
        ins_id, ip, _is_ready_fun = ec2.run_instance(name, ami, _get_aws_keys(keys))
        print (f"Instance with name {name} created: {ins_id}. Waiting initialization.")
        time.sleep(15)
        while not _is_ready_fun():
            time.sleep(15)
            print ("Initializing...")
        print (f"Server {name} is ready. IP:")
        print (ip)


def list_servers(name):
    if name == "":
        names = ec2.find_server_names()
        if len(names) == 0:
            print (f"No servers found")
        else:
            names.sort()
            print ("\n".join(names))
    else:
        instances = ec2.find_instances_by_tag(name)
        instances.sort(key=lambda e: e['ip'])
        if len(instances) == 0:
            print (f"No servers found")
        else:
            for num, ins in enumerate(instances, start=1):
                print (f"({num}): {ins['ip']} ({ins['id']})")

def list_clusters():
    clusters = ec2.list_load_balancers()
    clusters.sort(key=lambda e: e['name'])
    if len(clusters) == 0:
        print (f"No clusters found")
    else:
        for num, ins in enumerate(clusters, start=1):
            print (f"({num}): {ins['name']} ({ins['dns_name']})")

def connect_to_server(name, keys, ip_filter, index_filter):
    servers = [ins for num, ins in enumerate(ec2.find_instances_by_tag(name), start=1)
               if ip_filter == "" or ip_filter == ins['ip']
               if index_filter == "" or index_filter == str(num)]
    if len(servers) == 0:
        print (f"Cannot find server matching criteria")
    elif len(servers) > 1:
        print (f"More than one server matching criteria exists")
    else:
        ins = servers[0]
        print (f"Connecting to server {name} ({ins['id']}/{ins['ip']})")
        ssh.login_to_server("ubuntu", ins['ip'], keys)


def kill_server(name):
    ins_id, is_completed_func = ec2.terminate_instances(name)
    if ins_id is []:
        print (f"Could not find server named {name}")
    else:
        print (f"Found instances by name {name}: {','.join(ins_id)}. Going to terminate.")
        while not is_completed_func():
            print (f"Terminating...")
            time.sleep(10)
        print (f"Server {name} killed.")


def create_image(server_name, image_name):
    ins = ec2.find_instances_by_tag(server_name)
    if len(ins) == 0:
        print (f"Cannot find server with name {server_name}")
    elif len(ins) > 1:
        print (f"More than one server with name {server_name} exists")
    else:
        instance = ins[0]
        print (f"Creating image {image_name} from server {server_name}...")
        image_id = images.create_image(instance['id'], image_name)
        print (f"Image {image_name} created:")
        print (image_id)


def list_images():
    imgs = images.get_my_images()
    if len(imgs) == 0:
        print("You have no saved images.")
    else:
        print("Your images:")
        print("\n".join(imgs))


def delete_image(image_name):
    ami = images.find_own_image_by_name(image_name)
    if ami is None:
        print (f"Didn't find any image named {image_name}")
    else:
        print (f"Deleting image {image_name}({ami})...")
        images.delete_image(ami)
        while image_name in images.get_my_images():
            time.sleep(15)
            print("Deleting...")
        print (f"Image {image_name}({ami}) deleted...")


def run_cluster(group_name, image_name, domain, keys, min_size, max_size):
    ami = image_name if image_name.startswith("ami") else images.find_own_image_by_name(image_name)
    if ami is None:
        print (f"Cannot find image for with name {image_name}")
    else:
        template = ec2.create_launch_template(group_name, ami, _get_aws_keys(keys))
        target_group = ec2.create_target_group(group_name)
        is_ready = ec2.create_auto_scaling_group(group_name, group_name, target_group, min_size, max_size)
        [lb_dns, ns] = ec2.create_load_balancer(group_name, target_group, domain)
        if len(ns) != 0:
            route53.add_recordsset(domain, ns)
            dns.wait_for_dns_config(domain)
        while is_ready() is False:
            print (f"Waiting instances initialization...")
            time.sleep(15)
        print (f"Server group available via {domain if domain != '' else lb_dns}")


def delete_cluster(group_name):
    ec2.delete_load_balancer(group_name)
    print (f"Load balancer deleted.")
    #todo: delete all route53 records
    auto_scaling_group = ec2.delete_auto_scaling_group(group_name)
    print (f"Autoscaling group deleted")
    ins_id, is_completed_func = ec2.terminate_instances(group_name)
    time.sleep(10)
    while not is_completed_func():
        print (f"Terminating instances...")
        time.sleep(10)
    print (f"Instances terminated.")


def _get_aws_keys(input):
    if input == "":
        ssh.generate_ssh()
        aws_keys = ec2.get_keys_name("id_rsa.pub")
        logging.debug(f"New aws keys generated: {aws_keys}")
        if aws_keys is None:
            raise Exception(f"Failed to obtain aws-ssh-keys for {input}")
    else:
        aws_keys = ec2.get_keys_name(input)
        if aws_keys is not None:
            logging.debug(f"Reusing existing aws keys: {aws_keys}")
            return aws_keys
