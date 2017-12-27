import sys
import rpyc
import socket
import thread
from DBConnection27 import Internship
from DBConnection27 import Client
from rpyc.utils.server import ThreadedServer

class MiddleServer(rpyc.Service):

    def myInit(self, myHost, myPort, dbHost, dbPort, crowdsHost, crowdsPort):
        self.connections = 0
        self.host = myHost
        self.port = myPort
        #ph = PortHandler(self.host, self.port)
        #ph.start()
        self.threadLock = thread.allocate_lock()
        self.db = rpyc.connect(dbHost, dbPort, config={"allow_all_attrs":True})
        self.crowds = rpyc.connect(crowdsHost, crowdsPort, config={"allow_all_attrs":True})
        self.crowds.add_port(self.port)
        self.crowds.close()

    #ensure stable matching
    def on_connect(self):
        self.connections = self.connections + 1

    def on_disconnect(self):
        self.connections = self.connections - 1

    #IPv4 when working with sockes, not suitable for rpyc
    def generatePort(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = self.host
        port = 1024
        for attempt in range(1024,4000,1):
            try:
                result = s.connect((host, attempt))
            except Exception:
                port = attempt
                break
        return port

    def exposed_connectionAllowed(self):
        with self.threadLock:
            if self.connections > 1:
                return False
            return True

    def exposed_getPort(self):
        return self.port

    def exposed_findMeAnInternshipAlready(self, client):
        with self.threadLock:
            internship = None
            internships = self.db.getInternships();
            bestMatch = 0
            for i in internships:
                match = 0;
                if client.experience >= i.experience:
                    match = match + 1
                if client.duration == i.duration:
                    match = match + 1
                if len(client.locations) == 0:
                    match = match + 2
                else :
                    if (i.location is not None) and (i.location in client.locations):
                        match = match + 2
                if len(client.languages) == 0:
                    match = match + 3
                    if (i.language is not None) and (i.language in client.languages):
                        match = match + 3
                if match > bestMatch:
                    bestMatch = match
                    internship = i
            return internship

    #only for testing reasons
    def sayHello(self):
        print ("hello, i've connected on port " + str(self.exposed_getPort()))

    #only for testing reasons
    def wait(self):
        while(True):
            pass


def main():
    md = MiddleServer();
    md = md.myInit(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5])
    ThreadedServer(md, port=1234,
                   protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()

if __name__ == "__main__":
    main()