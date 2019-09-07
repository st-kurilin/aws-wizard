

def register_commands(parser):
    sp = parser.add_parser('server', help="Run AWS instance with name if doesn't exist")
    sp.add_argument('name', help='Server name', metavar='myserver', default="")
    sp.add_argument('--ami', help='Base AMI.', metavar='ami-1234', default='')

    ksp = parser.add_parser('kill-server', help="Terminate and delete AWS Instance")
    ksp.add_argument('name', help='Server name', metavar='myserver', default="")

    fp = parser.add_parser('freeze-server', help='Saves instance to image')
    fp.add_argument('server', help='Name for server that is running', metavar='myserver')
    fp.add_argument('--image', help='Image name. Default to server-name ', metavar='myimage', default='')

    ksp = parser.add_parser('delete-image', help="Removes image")
    ksp.add_argument('name', help='Image name', metavar='myserver', default="")

    ssp = parser.add_parser('server-group', help='Runs scalable group of servers')
    ssp.add_argument('name', help='Name for server group', metavar='mygroup')
    ssp.add_argument('image', help='Name for image to run in group', metavar='myimage')
    ssp.add_argument('min', help='Minimum number of instances. Default to 2', metavar='2', default='2', type=int)
    ssp.add_argument('max', help='Maximum number of instances. Default to 5', metavar='5', default='5', type=int)

    ssp = parser.add_parser('delete-server-group', help='Deletes resources connected to server group')
    ssp.add_argument('image', help='Name for server-group', metavar='myimage')


def exec_command(args):
    if "server" in args:
        server(args.name, args.ami)
        return True
    elif "kill-server" in args:
        server(args.name)
        return True
    elif "freeze-server" in args:
        freeze(args.server, args.image if args.image != "" else args.server)
        return True
    elif "delete-image" in args:
        freeze(args.image)
        return True
    elif "server-group" in args:
        server_group(args.name, args.image, args.min, args.max)
        return True
    elif "delete-server-group" in args:
        delete_server_group(args.name)
        return True
    else:
        return False

def server(name, image_ami):
    raise Exception("Not implemented")

def kill_server(name):
    raise Exception("Not implemented")

def freeze(server_name, image_name):
    raise Exception("Not implemented")

def delete_image(image_name):
    raise Exception("Not implemented")

def server_group(group_name, image_name, min, max):
    raise Exception("Not implemented")

def delete_server_group(group_name):
    raise Exception("Not implemented")
