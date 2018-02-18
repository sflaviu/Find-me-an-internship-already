# Stable matching between Client and Server
from random import randint


class ExperimentStableMatching:    
    def count_stable_matchings(self):
        for n in range(4,8):
            min = 10000
            max = -1
            sum = 0
            for nr in range(1,1000):
                preferences = []
                for i in range(0,n):
                    preferences.append(self.get_servers(n))
                allStableMatchings = []
                for i in range(1, (2*n)):
                    availableServer = []
                    for k in range(0,n):
                        availableServer.append(1)
                    clients = []
                    for k in range(0,n):
                        clients.append(-1)
                    initial_match = self.generate_initial_match(n) 
                    for k in initial_match:
                        clients[k] = self.choose_server(availableServer, preferences[k])
                        availableServer[clients[k]] = 0
                    ok = True
                    for stableMatch in allStableMatchings:
                        if self.check_equality(clients, stableMatch) == True:
                            ok = False
                    if ok == True:
                        allStableMatchings.append(clients)
                if len(allStableMatchings) < min:
                    min = len(allStableMatchings)
                if len(allStableMatchings) > max:
                    max = len(allStableMatchings)
                sum = sum + len(allStableMatchings)
            sum = sum/1000
            print(str(n) + "   " + str(min) + "   " + str(max) + "  " + str(sum))


    def get_servers(self, n):
        serversList = []
        for i in range(0,n):
            serversList.append(i)
        newServersList = self.set_preferences(serversList, n)
        return newServersList

    def generate_initial_match(self, n):
        p = self.get_servers(n)
        return p

    def choose_server(self, availableServers, clientPreferences):
        for server in clientPreferences:
            if availableServers[server] == 1:
                return server
                    
    def set_preferences(self, serversList, n):
        var = 2*n
        for i in range(0,var):
            tmp1 = randint(0, n-1)
            tmp2 = randint(0, n-1)
            tmp = serversList[tmp1]
            serversList[tmp1] = serversList[tmp2]
            serversList[tmp2] = tmp
        return serversList

    def check_equality(self, list1, list2):
            for i in range(0,len(list1)):
                if (list1[i] != list2[i]):
                    return False
            return True


test1 = ExperimentStableMatching()
test1.count_stable_matchings()
        
                
            
                    
                    


                
            
