import cmd
import rpyc
from rpyc.utils.server import ThreadedServer
import sys
import random
from rpDBMethods import Client
from Server import MiddleServer


class ClientComm(cmd.Cmd):
    def do_set_name(self, args):
        global pref
        global name
        pref += 1
        name = args
        print "Name: " + name

    def do_set_experience(self, args):
        global pref
        global exp
        pref += 1
        exp = int(args)
        print "Experience: " + str(exp)

    def do_set_duration(self, args):
        global pref
        global duration
        pref += 1
        duration = int(args)
        print "Duration: " + str(duration)

    def do_set_locations(self, args):
        global pref
        global locations
        pref += 1
        locations = args.split()  # map(str, args.split())
        print "Locations: " + str(locations)

    def do_set_languages(self, args):
        global pref
        global languages
        pref += 1
        languages = args.split()
        print "Languages: " + str(languages)

    def do_start_matching(self, args):
        global pref
        if pref > 4:
            conn = rpyc.connect("10.142.0.2", 1234, config={"allow_all_attrs": True})
            conn.root.connect_me(ip, port)
            conn.close()
            ThreadedServer(ClientServer, port=port,
                           protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()

    def do_show_results(self, args):
        global result
        print str(result)

    def do_send_my_data(self, args):
        # check if data can be sent
        me = Client()
        me.userName = name
        me.experience = exp
        me.duration = duration
        me.locations = locations
        me.languages = languages
        global result
        result = ClientServer.exposed_send_data(ClientServer(), my_server, me)


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
            conn = rpyc.connect(server.host, server.port, config={"allow_all_attrs": True})
            return conn.root.findMeAnInternshipAlready(data)
        else:
            conn = rpyc.connect(next_client.host, next_client.port, config={"allow_all_attrs": True})
            return conn.root.send_data(server, data)

    def exposed_choose_server(self):
        global my_server
        # my_server = servers[random.randint(0, len(servers)-1)]
        for i in servers:
            conn = rpyc.connect(i.host, i.port, config={"allow_all_attrs": True})
            if conn.root.connectionAllowed():
                my_server = i
            conn.close()


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
ip = sys.argv[1]  # start with self ip and port
port = sys.argv[2]
result = None
cC = ClientComm()
cC.prompt = 'Client>>'
cC.cmdloop('Client')