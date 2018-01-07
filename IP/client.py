import cmd
import rpyc
from rpyc.utils.server import ThreadedServer
import sys
import random
from rpDBMethods import Client
import thread
from Server import MiddleServer

class ClientComm(cmd.Cmd):
    #Method for showing IP
    def do_show_ip(self):
        global assignedIp
        print("My assigned IP is: "+assignedIp)

    def do_set_name(self, args):
        global pref
        global name
        pref += 1
        name = args
        print ("Name: " + name)

    def do_set_experience(self, args):
        global pref
        global exp
        pref += 1
        exp = int(args)
        print ("Experience: " + str(exp))

    def do_set_duration(self, args):
        global pref
        global duration
        pref += 1
        duration = int(args)
        print ("Duration: " + str(duration))

    def do_set_locations(self, args):
        global pref
        global locations
        pref += 1
        locations = args.split()  # map(str, args.split())
        print ("Locations: " + str(locations))

    def do_set_languages(self, args):
        global pref
        global languages
        pref += 1
        languages = args.split()
        print ("Languages: " + str(languages))

    def do_start_matching(self, args):
        global pref, port, ip
        if pref > 4:
            conn = rpyc.connect("10.142.0.3", 1024, config={"allow_all_attrs": True})
            conn.root.connect_me(ip, port)
            conn.close()
            # ThreadedServer(ClientServer, port=port,
            #             protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()
            thread.start_new_thread(start_server, ())

    def do_show_results(self, args):
        global result
        print (str(result))

    def do_see_client(self, args):
        print (next_client[0])
        print (str(next_client[1]))

    def do_send_my_data(self, args):
        # check if data can be sent
        me = Client()
        me.userName = name
        me.experience = exp
        me.duration = duration
        me.locations = locations
        me.languages = languages
        global result
        result = ClientServer.send_data(my_server, me)


class ClientServer(rpyc.Service):
    def exposed_get_servers(self, server_list):
        global servers
        servers = server_list

    def exposed_get_clients(self, client_list):
        global next_client
        next_client = client_list[random.randint(0, len(client_list)-1)]

    def exposed_send_data(self, server, data):
        rand = random.randint(1, 100)
        if rand < 20:
            conn = rpyc.connect(server[0], server[1], config={"allow_all_attrs": True})
            internship = conn.root.findMeAnInternshipAlready(data)
            return internship
        else:
            conn = rpyc.connect(next_client[0], next_client[1], config={"allow_all_attrs": True})
            internship = conn.root.send_data(server, data)
            return internship

    @staticmethod
    def send_data(server, data):
        rand = random.randint(1, 100)
        if rand < 20:
            conn = rpyc.connect(server[0], server[1], config={"allow_all_attrs": True})
            internship = conn.root.findMeAnInternshipAlready(data)
            return internship
        else:
            conn = rpyc.connect(next_client[0], next_client[1], config={"allow_all_attrs": True})
            internship = conn.root.send_data(server, data)
            return internship

    def exposed_choose_server(self):
        global my_server
        # my_server = servers[random.randint(0, len(servers)-1)]
        for i in servers:
            # print "Connecting to "+i[0]+" "+str(i[1])
            conn = rpyc.connect(i[0], i[1], config={"allow_all_attrs": True})
            if conn.root.connectionAllowed():
                my_server = i
            conn.close()

class ClientIpChecker(rpyc.Service):

    def exposed_check_ip(self, sIp):
        global assignedIp
        if(assignedIp==sIp):
            return true
        return false
		
def start_server():
    global port, ip
    ThreadedServer(ClientServer, port=port,
                   protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()

def launch_Ip_checker(portS):
    global ipGiver
    ThreadedServer(ClientIpChecker,port=portS,protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()

global ip
def get_Ip():
    global ip
    conn=rpyc.connect(ip,port=4321,config={"allow_all_attrs": True})
    return conn.root.chooseIp("10.142.0.2")

global assignedIp

if __name__ == '__main__':
    my_server = None
    random.seed()
    pref = 0
    next_client = None
    name = ""
    exp = 0
    duration = 0
    locations = []
    languages = []
    servers = []

    global ip
    ip = sys.argv[1]  # start with self ip and port
    port = int(sys.argv[2])

    aIp = get_Ip()

    assignedIp = aIp[0]

    print "My assigned IP is " + assignedIp

    thread.start_new_thread(launch_Ip_checker, (ip[1],))

    result = None
    cC = ClientComm()
    cC.prompt = 'Client>>'
    cC.cmdloop('Client')
