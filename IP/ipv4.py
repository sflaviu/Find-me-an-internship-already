import rpyc
import random
import time


class IPv4:
    allIps = {}

    def __init__(self, sIps):
        self.realIp = sIps
        self.assignedIp = '169.254.0.0'  # Not usable IP

        # Range 169.254.1.0 to 169.254.254.255

    def reconfigure(self):
        time.sleep(2)
        newIp = chooseIP()
        return newIp

    def chooseIP(self):
        firstI = randint(1, 254)
        secondI = randint(0, 255)

        currentAIp = '169.254.' + str(firstI) + '.' + str(secondI)

        for ip in allIps.items():
            if ip[1] != realIp:
                conn = rpyc.connect(ip[1], 2222,
                                    config={'allow_all_attrs': True})
                answer = conn.root.check_ip(currentAIp)
                if answer == true:
                    reconfiguredIP = reconfigure()
                    return reconfiguredIP
        allIps[currentAIp] = realIp
        return currentAIp

    def checkIp(self, ip):
        if assignedIp == ip:
            return true
        return false



