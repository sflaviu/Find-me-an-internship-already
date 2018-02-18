class Match:
    def __init__(self, id, p):
        self.jobID = id
        self.percent = p


class Node:

    def __init__(self, id, bestMatch = 0, indexOfBestMatch = -1, totalMatches = 0, matches = []):
        self.id = id
        self.bestMatch = bestMatch
        self.indexOfBestMatch = indexOfBestMatch
        self.totalMatches = totalMatches
        self.matches = matches

    def recomputeBestMatch(self):
        self.bestMatch = -1
        for i in range(len(self.matches)):
            if self.matches[i] > self.bestMatch:
                self.bestMatch = self.matches[i]
                self.indexOfBestMatch = i

    def setBestMatch(self, n, i):
        self.bestMatch = n
        self.indexOfBestMatch = i

    def setTotalMatches(self, n):
        self.totalMatches = n

    def setMatches(self, list):
        self.matches = []
        for i in list:
            self.matches.append(i)

class PriorityQueue:
    list = []
    fails = []

    def __init__(self):
        self.list = []
        self.fails = []

    def addToPriorityQueue(self,node):
        i = 0
        while (i < len(self.list)) and (self.list[i].totalMatches < node.totalMatches):
            i = i + 1
        while (i<len(self.list)) and (self.list[i].totalMatches == node.totalMatches) and (self.list[i].bestMatch > node.bestMatch):
            i = i + 1
        self.list.insert(i, node)

    def removeFirst(self):
        if len(self.list) > 0:
            node = self.list[0]
            for i in range(1, len(self.list)):
                #print(node.id, node.indexOfBestMatch, self.list[i].id, self.list[i].matches[0])
                if self.list[i].matches[node.indexOfBestMatch] > 0:
                    #print(node.id, self.list[i].id)
                    self.list[i].matches[node.indexOfBestMatch] = 0
                    self.list[i].totalMatches -=1
                    self.list[i].recomputeBestMatch()
                    if self.list[i].totalMatches == 0:
                        self.fails.append(self.list[i])
            self.list.remove(node)
            for e in self.fails:
                self.list.remove(e)
            if len(self.list) > 0:
                self.list.sort(key = lambda x: (x.totalMatches, - x.bestMatch))
            return node
        else:
            raise Exception("No more elements in the list")

    def length(self):
        return len(self.list)


class StableMatching:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        #self.matrix = [[0 for j in range(cols)] for i in range(rows+1)]
        #self.nodes = []
        self.priorityQueue = PriorityQueue()

    def addStudent(self, id, percents):
        if len(percents) != self.cols:
            raise Exception("Input list has an illegal number of elements")

        node = Node(id)

        for i in range(len(percents)):
            #self.matrix[id][i] = percents[i]
            if percents[i] > 0:
                node.setTotalMatches(node.totalMatches + 1)
            if percents[i] > node.bestMatch :
                node.setBestMatch(percents[i], i)

        node.setMatches(percents)
        #self.nodes.append(node)
        self.priorityQueue.addToPriorityQueue(node)

    def run(self):
        dict = {}
        while(self.priorityQueue.length() > 0):
            node = self.priorityQueue.removeFirst();
            #print(str(node.id), str(node.bestMatch), str(node.indexOfBestMatch))
            dict[node.id] = Match(node.indexOfBestMatch, node.bestMatch)
        return dict