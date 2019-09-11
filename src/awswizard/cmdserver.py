import logging
import time

from . import ssh
from .aws import ec2
from .aws import images


def register_commands(parser):
    sp = parser.add_parser('server', help="Run AWS instance with name if doesn't exist")
    sp.add_argument('server_name', help='Server name', metavar='myserver', default="")
    sp.add_argument('--ami', help='Base AMI.', metavar='ami-1234', default='')
    sp.add_argument('--image-name', help='Your image that was created by freezing server', metavar='myimage',
                    default='')
    sp.add_argument('--ssh-keys', help='SSH keys to be used to access instance', metavar='./id_rsa.pub',
                    default='id_rsa', dest="keys")

    cp = parser.add_parser('connect-to-server', help="SSH to server")
    cp.add_argument('server_name', help='Server name', metavar='myserver', default="")
    cp.add_argument('--ssh-keys', help='SSH keys that were used during server creation', metavar='./id_rsa',
                    default='id_rsa', dest="keys")

    ksp = parser.add_parser('kill-server', help="Terminate and delete AWS Instance")
    ksp.add_argument('name', help='Server name', metavar='myserver', default="")

    fp = parser.add_parser('freeze-server', help='Saves instance to image')
    fp.add_argument('server', help='Name for server that is running', metavar='myserver')
    fp.add_argument('--image-name', help='Image name. Default to server-name ', metavar='myimage', default='',
                    dest="image_name")

    parser.add_parser('list-frozen', help='Lists images created by current user')

    df = parser.add_parser('delete-frozen', help="Removes image")
    df.add_argument('image_name', help='Image name', metavar='myimage', default="")

    ssp = parser.add_parser('server-group', help='Runs scalable group of servers')
    ssp.add_argument('server_group_name', help='Name for server group', metavar='mygroup')
    ssp.add_argument('--image-name', help='Name for image to run in group', metavar='myimage', dest="image_name", required=True)
    ssp.add_argument('--ssh-keys', help='SSH keys to be used to access instance', metavar='./id_rsa.pub',
                     default='id_rsa', dest="keys")
    ssp.add_argument('--min-size', help='Minimum number of instances. Default to 2',
                     metavar='2', default='2', type=int, dest="min_size")
    ssp.add_argument('--max-size', help='Maximum number of instances. Default to 5',
                     metavar='5', default='5', type=int, dest="max_size")

    dsp = parser.add_parser('kill-server-group', help='Deletes resources connected to server group')
    dsp.add_argument('server_group_name', help='Name for server-group', metavar='mygroup')


def exec_command(argv, args):
    if "server" in argv:
        server(args.server_name, args.ami, args.keys)
        return True
    if "connect-to-server" in argv:
        connect_to_server(args.server_name, args.keys)
        return True
    elif "kill-server" in argv:
        kill_server(args.name)
        return True
    elif "freeze-server" in argv:
        img = args.image_name if args.image_name != "" else args.server_group
        freeze(args.server, img)
        return True
    elif "list-frozen" in argv:
        list_frozen()
        return True
    elif "delete-frozen" in argv:
        delete_image(args.image_name)
        return True
    elif "server-group" in argv:
        img = args.image_name if args.image_name != "" else args.server_group
        server_group(args.server_group_name, img, args.keys, args.min_size, args.max_size)
        return True
    elif "kill-server-group" in argv:
        delete_server_group(args.server_group_name)
        return True
    else:
        return False


def server(name, image_ami, keys):
    exists = ec2.find_instance_by_tag(name)
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


def connect_to_server(name, keys):
    ins = ec2.find_instances_by_tag(name)
    if len(ins) == 0:
        print (f"Cannot find server with name {name}")
    elif len(ins) > 1:
        print (f"More than one server with name {name} exists")
    else:
        instance = ins[0]
        print (f"Cannecting to server {name} ({instance['id']}/{instance['ip']})")
        ssh.login_to_server("ubuntu", instance['ip'], keys)


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


def freeze(server_name, image_name):
    ins = ec2.find_instances_by_tag(name)
    if len(ins) == 0:
        print (f"Cannot find server with name {name}")
    elif len(ins) > 1:
        print (f"More than one server with name {name} exists")
    else:
        instance = ins[0]
        print (f"Creating image {image_name} from server {server_name}...")
        image_id = images.create_image(instance['id'], image_name)
        print (f"Image {image_name} created:")
        print (image_id)


def list_frozen():
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


def server_group(group_name, image_name, keys, min_size, max_size):
    ami = image_name if image_name.startswith("ami") else images.find_own_image_by_name(image_name)
    if ami is None:
        print ("Cannot find image for with name {image_name}")
    else:
        template = ec2.create_launch_template(group_name, ami, _get_aws_keys(keys))
        target_group = ec2.create_target_group(group_name)
        is_ready = ec2.create_auto_scaling_group(group_name, group_name, target_group, min_size, max_size)
        dns = ec2.create_load_balancer(group_name, target_group)
        while is_ready() is False:
            print (f"Waiting instances initialization...")
            time.sleep(15)
        print (f"Server group available via {dns}")


def delete_server_group(group_name):
    ec2.delete_load_balancer(group_name)
    print (f"Load balancer deleted.")
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
