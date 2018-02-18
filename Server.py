import sys
import rpyc
import socket
import thread
from rpDBMethods import Internship
from rpDBMethods import Client
from rpyc.utils.server import ThreadedServer

data = None

class PersistentData:
    def __init__(self, myHost, myPort, dbHost, dbPort, crowdsHost, crowdsPort):
        self.host = myHost
        self.port = myPort
        self.threadLock = thread.allocate_lock()
        self.dbPort = dbPort
        self.dbHost = dbHost
        #self.db = rpyc.connect(dbHost, dbPort, config={"allow_all_attrs": True})
        #self.crowds = rpyc.connect(crowdsHost, crowdsPort, config={"allow_all_attrs": True})
        #self.crowds.add_port(self.port)
        #self.crowds.close()

class MiddleServer(rpyc.Service):
    connections = 0

    #ensure stable matching
    def on_connect(self):
        MiddleServer.connections = MiddleServer.connections + 1

    def on_disconnect(self):
        MiddleServer.connections = MiddleServer.connections - 1

    #IPv4 when working with sockes, not suitable for rpyc
    def generatePort(self):
        global data
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = data.host
        port = 1024
        for attempt in range(1024,4000,1):
            try:
                result = s.connect((host, attempt))
            except Exception:
                port = attempt
                break
        return port

    def exposed_connectionAllowed(self):
        global data
        with data.threadLock:
            if MiddleServer.connections > 1:
                return False
            return True

    def exposed_getPort(self):
        global data
        return data.port

    def exposed_findMeAnInternshipAlready(self, client):
        global data
        with data.threadLock:
            internship = None
            connection = rpyc.connect(data.dbHost, data.dbPort, config={"allow_all_attrs":True})
            db = connection.root.DBConnection()
            internships = db.getInternships();
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
            company = db.getCompanyName(internship.company)
            language= db.getLanguageName(internship.language)
            location = db.getLocationName(internship.location)
            internshipString = "Internship at " + company + "\n" \
                                + "Location: " + location + "\n" \
                                + "Language: " + language + "\n" \
                                + "Experience: " + str(internship.experience) + "\n" \
                                + "Duration: " + str(internship.duration)
            connection.close()
            return internshipString

    #only for testing reasons
    def sayHello(self):
        print ("hello, i've connected on port " + str(self.exposed_getPort()))

    #only for testing reasons
    def wait(self):
        while(True):
            pass

def main():
    global data
    data = PersistentData(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],sys.argv[5], sys.argv[6])
    ThreadedServer(MiddleServer, port = int(sys.argv[2]),
                   protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()

if __name__ == "__main__":
    main()
