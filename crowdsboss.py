import rpyc
import subprocess
import socket
import thread
from cmd import Cmd
from rpyc.utils.server import ThreadedServer
from rpDBMethods import Client
from rpDBMethods import Internship
from rpDBMethods import Location
from rpDBMethods import Language
from rpDBMethods import Company

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
            clients = data.clients
            clients.remove(c)
            s.get_clients(clients)

    def do_add_internship(self):
        connection = rpyc.connect(data.dbHost, data.dbPort, config={"allow_all_attrs": True})
        db = connection.root.DBConnection()
        internships = db.getInternships()
        languages = db.getLanguages()
        locations = db.getLocations()
        companies = db.getCompanies()
        internship_id = 0
        for internship in internships:
            if internship.id > internship_id:
                internship_id = internship.id
        internship_id = internship_id + 1
        print("Select one of the companies' IDs")
        ids = []
        for c in companies:
            ids.append(c.id)
            print(str(c.id) + " " + c.name)
        company = -1
        while (company == -1):
            company_string = input();
            try:
                company = int(company_string)
                if company not in ids:
                    company = -1
            except ValueError:
                company = -1
            if (company == -1):
                print ("Invalid input, try again")
        print("Select one of the languages' IDs")
        ids = []
        for c in languages:
            ids.append(c.id)
            print(str(c.id) + " " + c.name)
        language = -1
        while (language == -1):
            language_string = input();
            try:
                language = int(language_string)
                if language not in ids:
                    language = -1
            except ValueError:
                language = -1
            if (language == -1):
                print ("Invalid input, try again")
        print("Select one of the locations' IDs")
        ids = []
        for c in locations:
            ids.append(c.id)
            print(str(c.id) + " " + c.city)
        location = -1
        while (location == -1):
            location_string = input();
            try:
                location = int(location_string)
                if location not in ids:
                    location = -1
            except ValueError:
                location = -1
            if (location == -1):
                print ("Invalid input, try again")
        duration_string =input("Please insert the duration of the internship")
        duration = -1
        while (duration == -1):
            try:
                duration = int(duration_string)
            except ValueError:
                duration = -1
                print ("Invalid input, try again")
        experience_string = input("Please insert your experience")
        experience = -1
        while (experience == -1):
            try:
                experience = int(experience_string)
            except ValueError:
                experience = -1
                print ("Invalid input, try again")
        myInternship = Internship();
        myInternship.id = internship_id;
        myInternship.experience = experience;
        myInternship.duration = duration;
        myInternship.company = company;
        myInternship.language = language;
        myInternship.location =location
        db.insertInternship(myInternship)
        connection.close()

    def do_remove_internship(self):
        connection = rpyc.connect(data.dbHost, data.dbPort, config={"allow_all_attrs": True})
        db = connection.root.DBConnection()
        internships = db.getInternships()
        print ("Select the id of the internship to delete")
        ids = []
        for i in internships:
            ids.append(i.id)
            print(str(i.id)+ " " +str(i.company))
        id_string = input()
        id = -1
        while (id == -1):
            try:
                id = int(id_string)
                if id not in ids:
                    id = -1
            except ValueError:
                id = -1
                print("Invalid input, please try again")
        myInternship = Internship();
        myInternship.id = id
        db.deleteInternship(myInternship)

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


def server_start()
    ThreadedServer(CrowdsMaster, port=data.port,
                   protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()


def main():
    global data
    data = PersistentData()
    thread.start_new_thread(server_start, ())
    myConsole = CrowdsConsole()
    myConsole.prompt = ">"
    myConsole.cmdloop("Server has started\nAvailable commands\nstable_mathcing\nadd_internship\nremove_internship\n")

if __name__ == "__main__":
    main()