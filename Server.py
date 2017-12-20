import sys
import rpyc
import socket
import thread
from DBConnection27 import Internship
from DBConnection27 import Client

class MiddleServer(rpyc.Service):

    def __init__(self, dbHost, dbPort, crowdsHost, crowdsPort):
        self.connections = 0
        self.host = socket.gethostname()
        self.port = self.generatePort();
        self.threadLock = thread.allocate_lock()
        self.db = rpyc.connect(dbHost, dbPort)
        self.crowds = rpyc.connect(crowdsHost, crowdsPort)
        self.crowds.add_port(self.port)
        self.crowds.close()

    def on_connect(self):
        self.connections = self.connections + 1

    def on_disconnect(self):
        self.connections = self.connections - 1

    def generatePort(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 1024
        for attempt in xrange(1024,4000,1):
            result = s.connect((host, attempt))
            if result == 0 :
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


if __name__ == "main":
    md = MiddleServer(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3])