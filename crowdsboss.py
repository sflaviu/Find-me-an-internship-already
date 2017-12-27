import rpyc
import subprocess
import socket
from cmd import Cmd
from rpyc.utils.server import ThreadedServer

global data

class PersistentData():
    def __init__(self):
        self.clients = []
        self.clientsRPYC = []
        self.servers = []
        # to be changed accordingly
        self.host = socket.gethostname()
        self.port = 1024
        self.dbHost = "localhost"
        self.dbPort = 1234

class CrowdsConsole(Cmd):
    def do_stable_matching(self, args):
        global data
        ports = 1024
        for i in data.clients:
            ports += 1
            subprocess.call(
                ["python", "Server.py " + str(data.host) + " " + str(ports) + " " + str(data.dbHost) //
                 + " " + str(data.dbPort) + " " + str(data.host) + " " + str(data.port)])
            # get port of each server in a list
            data.servers.append((data.host, ports))
        for c in data.clientsRPYC:
            # name should be adjusted accordingly
            s = c.root.ClientServer()
            s.get_servers(data.servers)

    def do_add_internship(self):
        #to do
        pass

    def do_remove_internship(self):
        #to do
        pass

    def do_quit(self, args):
        print "Program terminated."
        raise SystemExit



class CrowdsMaster(rpyc.Service):
    #called by client
    def exposed_connect_me(self, ip, port):
        global data
        client = rpyc.connect(ip, port, config={"allow_all_attrs": True})
        data.clientsRPYC.append(client)
        data.clients.append((ip, port))

    def exposed_get_clients(self):
        global data
        return data.clients

    def exposed_disconnect_me(self, ip, port):
        global data
        data.clients.remove((ip, port))

    #not using this anymore
    def exposed_add_port(self, port):
        global data
        data.servers.append(port)


def main():
    global data
    data = PersistentData()
    ThreadedServer(CrowdsMaster, port=data.port,
                   protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()
    myConsole = CrowdsConsole()
    myConsole.prompt(">");
    myConsole.cmdloop("Server has started\nAvailable commands\nstable_mathcing\nadd_internship\nremove_internship\n")

if __name__ == "__main__":
    main()
