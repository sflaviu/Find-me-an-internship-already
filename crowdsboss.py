import rpyc
import subprocess
import socket


class CrowdsMaster(rpyc.Service):
    def __init__(self):
        self.clients = []
        self.serverPorts = []

    def exposed_connect_me(self, ip, port):
        self.clients.append((ip, port))

    def exposed_get_clients(self):
        return self.clients

    def exposed_disconnect_me(self, ip, port):
        self.clients.remove((ip, port))

    def start_matching(self):
        ports = 1024
        for i in self.clients:
            ports += 1
            subprocess.call(["python", "Server.py " + str(ports) + " " + str(ip1) + " " + str(port1) + " " + str(myip) + " " + str(myport)])
            # get port of each server in a list
            pass
        for i in self.clients:
            # send all ports
            pass
        pass

    def exposed_add_port(self, port):
        self.serverPorts.append(port)


# not working
def generate_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 1024
    for attempt in xrange(1024, 4000, 1):
        result = s.connect((host, attempt))
        if result == 0:
            port = attempt
            break
    return port


# ask sysadmin for db ip and port
ip1 = 0
port1 = 0
