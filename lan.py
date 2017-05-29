from __future__ import print_function

import socket
import shlex
import sys
import threading
import time
from subprocess import Popen, PIPE

import Pyro4

@Pyro4.expose
class LAN(object):

    def __init__(self):
        pass

    def get_ip(self):
    	try:
    		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    		s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    		local_ip_address = s.getsockname()[0]
    	except:
    		local_ip_address = "127.0.1.1"
    	finally:
    		s.close()

    	return local_ip_address

def main():

    l = LAN()

    obj_port, ns_port = 50011, 50010
    daemon = Pyro4.Daemon(host='localhost', port=obj_port)
    uri = daemon.register(l, objectId="lan.LAN")
    _, obj_port = uri.location.split(":")
    ns = Pyro4.locateNS('localhost',ns_port)
    ns.register("LAN", uri)
    print("Object registered on uri: {}".format(uri))
    print("Creating SSH tunnels")
    command = "ssh -N {0} {1}:{2}:{3} {4}"
    ns_command = command.format('-R', ns_port, 'localhost', ns_port, 'do-droplet')
    obj_command = command.format('-R', obj_port, 'localhost', obj_port, 'do-droplet')
    print("Invoking NS tunnel command: {}".format(ns_command))
    ns_args = shlex.split(ns_command)
    ns_proc = Popen(ns_args, shell=False, stdout=PIPE, stderr=PIPE)
    print("Invoking object tunnel command: {}".format(obj_command))
    obj_args = shlex.split(obj_command)
    obj_proc = Popen(obj_args, shell=False, stdout=PIPE, stderr=PIPE)
    print("\rLaunching server...",end="")
    t = threading.Thread(target=daemon.requestLoop)
    t.daemon = True
    t.start()
    print("\rLaunching server... Done.")

    while True:
        try:
            time.sleep(0.001)
        except KeyboardInterrupt:
            print("\rCleaning up the tunnel processes...",end="")
            obj_proc.kill()
            ns_proc.kill()
            print("\rCleaning up the tunnel processes... Done.")
            print("Exiting...")
            sys.exit()

if __name__ == '__main__':

    main()
