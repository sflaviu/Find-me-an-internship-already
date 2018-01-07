import rpyc
import random
import time
import thread

from rpyc.utils.server import ThreadedServer

global ni

class NetworkInfo():
    def __init__(self):
        self.allIps={}
        self.ports=[]
        self.lastport=2222

class IPv4(rpyc.Service):

    global ni

    def reconfigure(self):
        time.sleep(2)
        newIp = chooseIP()
        return newIp

    def exposed_chooseIp(self,rIp):
        firstI = random.randint(1, 254)
        secondI = random.randint(0, 255)

        currentAIp = '169.254.' + str(firstI) + '.' + str(secondI)

        i=0
        for ip in ni.allIps.items():
            if ip[1] != rIp:
                print ip[1] 
                print ni.ports[i]
                conn = rpyc.connect(ip[1], ni.ports[i],config={'allow_all_attrs': True})
                answer = conn.root.check_ip(currentAIp)
                if answer == True:
                    reconfiguredIP = reconfigure()
                    return reconfiguredIP
            i=i+1
        ni.allIps[currentAIp] = rIp
        ni.ports.append(ni.lastport+1)
        ni.lastport=ni.lastport+1
        
        self.printIps()
        return (currentAIp,ni.lastport)

    def printIps(self):
        print "All Ips"
        for keys,values in ni.allIps.items():
            print(keys)
            print(values)
            print ""

    def deleteIP(self):
        i = 0
        for ip in IPv4.allIps.items():
            if ip[1] == self.realIp:
                del IPv4.allIps[ip]
                del ports[i]
                break
            i = i + 1


def server_start():
    ThreadedServer(IPv4, port=4321,protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()


if __name__ == "__main__":
    global ni
    ni=NetworkInfo()
    thread.start_new_thread(server_start,())
    while 1==1:
        pass
