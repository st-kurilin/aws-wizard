import logging
import time

from . import ssh
from .aws import ec2
from .aws import images


def register_commands(parser):
    sp = parser.add_parser('server', help="Run AWS instance with name if doesn't exist")
    sp.add_argument('name', help='Server name', metavar='myserver', default="")
    sp.add_argument('--ami', help='Base AMI.', metavar='ami-1234', default='')
    sp.add_argument('--image-name', help='Your image that was created by freezing server', metavar='myimage', default='')
    sp.add_argument('--ssh-keys', help='SSH keys to be used to access instance', metavar='./id_rsa',
                    default='id_rsa.pub', dest="keys")

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
    ssp.add_argument('name', help='Name for server group', metavar='mygroup')
    ssp.add_argument('image', help='Name for image to run in group', metavar='myimage')
    ssp.add_argument('min', help='Minimum number of instances. Default to 2', metavar='2', default='2', type=int)
    ssp.add_argument('max', help='Maximum number of instances. Default to 5', metavar='5', default='5', type=int)

    ssp = parser.add_parser('delete-server-group', help='Deletes resources connected to server group')
    ssp.add_argument('image', help='Name for server-group', metavar='myimage')


def exec_command(argv, args):
    if "server" in argv:
        server(args.name, args.ami, args.keys)
        return True
    elif "kill-server" in argv:
        kill_server(args.name)
        return True
    elif "freeze-server" in argv:
        freeze(args.server, args.image_name if args.image_name != "" else args.server)
        return True
    elif "list-frozen" in argv:
        list_frozen()
        return True
    elif "delete-frozen" in argv:
        delete_image(args.image_name)
        return True
    elif "server-group" in argv:
        server_group(args.name, args.image, args.min, args.max)
        return True
    elif "delete-server-group" in argv:
        delete_server_group(args.name)
        return True
    else:
        return False


def server(name, image_ami, keys):
    instance = ec2.find_instance_by_tag(name)
    if instance is not None:
        print (f"Instance with name {name} already exists: {instance['id']}")
        print (instance['ip'])
    else:
        print (f"Spanning new server with name {name}.")
        ami = image_ami if image_ami != "" else images.find_ubuntu_ami()
        ins_id, ip, _is_ready_fun = ec2.run_instance(ami, name, _get_aws_keys(keys))
        print (f"Instance with name {name} created: {ins_id}. Waiting initialization.")
        time.sleep(15)
        while not _is_ready_fun():
            time.sleep(15)
            print ("Initializing...")
        print (f"Server {name} is ready. IP:")
        print (ip)


def kill_server(name):
    ins_id, is_completed_func = ec2.terminate_instance(name)
    if ins_id is None:
        print (f"Could not find server named {name}")
    else:
        print (f"Found instance by name {name}: {ins_id}. Going to terminate.")
        while not is_completed_func():
            print (f"Terminating...")
            time.sleep(10)
        print (f"Server {name} killed.")


def freeze(server_name, image_name):
    instance = ec2.find_instance_by_tag(server_name)
    if instance is None:
        print (f"Could not find server named {server_name}")
    else:
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


def server_group(group_name, image_name, min, max):
    raise Exception("Not implemented")


def delete_server_group(group_name):
    raise Exception("Not implemented")


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
