import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._allGenes = DAO.get_all_nodes()
        self._threshold = 100000
        self._ris = []
        self._risWeight = -100000
        self.solBest = []

    def _builGraph(self):
        self.addNodes()
        self.addEdges()
        self._grafo.remove_edge(2,4)

    def longest_path(self,l):
        self._threshold = l
        self._ris = []
        for n in self._grafo.nodes:
            self.recursion(n,[])

    def recursion(self, lastV, partialEdges : list):
        #controllo ottimalità
        #print(partialEdges)
        if len(partialEdges) > 0:
            if not self.hasSpace(lastV,partialEdges):
                if self.calculateWeight(partialEdges) > self._risWeight:
                    self._ris = partialEdges[::]
                    self._risWeight = self.calculateWeight(partialEdges)
                    return

        #ricorsione
        for n in self._grafo.neighbors(lastV):
            #controllo ammissibilità
            if self.isAdmissible(lastV,n,partialEdges):
                partialEdges.append((lastV,n))
                self.recursion(n,partialEdges)
                partialEdges.pop()

    def isAdmissible(self, last, next, sol):
        if ((last,next) in sol) or ((next,last) in sol) or (self._grafo.get_edge_data(last,next)['weight'] < self._threshold):
            return False
        return True


    #Vero se dato l'utlimo nodo visitato io ho ancora nodi visitabili attraverso edge non percorsi
    def hasSpace(self,lastVisited, sol : list):
        for n in self._grafo.neighbors(lastVisited):
            if self._grafo[lastVisited][n]['weight'] > self._threshold:
                if ((lastVisited,n) not in sol) and ((n,lastVisited) not in sol):
                    return True
        return False



    #calcola il peso dato da una lista di tuple (edges) che rappresentano un cammino
    def calculateWeight(self, edgeList : list):
        pathWeight = 0
        for i in edgeList:
            pathWeight += self._grafo.get_edge_data(i[0],i[1])['weight']
        return  pathWeight


    #numero di nodi
    def addNodes(self):
        self._grafo.clear()
        for g in self._allGenes:
            if g.Chromosome != 0:
                self._grafo.add_node(g.Chromosome)

    def addEdges(self):
        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if n1 != n2:
                    w = DAO.get_edge(n1,n2)[0]['weight']
                    if w is not None:
                        self._grafo.add_edge(n1,n2,weight = w)


    def numNodes(self):
        return self._grafo.number_of_nodes()
    # numero di archi

    def numEdges(self):
        return self._grafo.number_of_edges()

    # archi con peso maggiore e minore
    def weightInfo(self):
        if self.numEdges() == 0:
            return 0,0
        ordEdges = sorted(self._grafo.edges(data=True), key=lambda edge : edge[2].get('weight',1))
        return ordEdges[0][2]['weight'], ordEdges[-1][2]['weight']

    # numero di archi maggiori/minore della soglia
    def countLimit(self, limit):
        edges = self._grafo.edges(data=True)
        countMore = 0
        countLess = 0
        for e in edges:
            if e[2].get('weight',1) > limit:
                countMore += 1
            elif e[2].get('weight', 1) < limit:
                countLess += 1
        return countMore,countLess

    def buildGraph(self):
        self._builGraph()

    def searchPath(self, t):

        for n in self._grafo.nodes():
            partial = []
            partial_edges = []

            partial.append(n)
            self.ricorsione2(partial, partial_edges, t)

        print("final", len(self.solBest), [i[2]["weight"] for i in self.solBest])

    def ricorsione2(self, partial, partial_edges, t):
        n_last = partial[-1]
        neigh = self.getAdmissibleNeighbs(n_last, partial_edges, t)

        # stop
        if len(neigh) == 0:
            weight_path = self.computeWeightPath(partial_edges)
            weight_path_best = self.computeWeightPath(self.solBest)
            if weight_path > weight_path_best:
                self.solBest = partial_edges[:]
            return

        for n in neigh:
            partial.append(n)
            partial_edges.append((n_last, n, self._grafo.get_edge_data(n_last, n)))
            self.ricorsione2(partial, partial_edges, t)
            partial.pop()
            partial_edges.pop()

    def getAdmissibleNeighbs(self, n_last, partial_edges, t):
        all_neigh = self._grafo.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if e[2]["weight"] > t:
                e_inv = (e[1], e[0], e[2])
                if (e_inv not in partial_edges) and (e not in partial_edges):
                    result.append(e[1])
        return result

    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight

    def count_edges(self, t):
        count_bigger = 0
        count_smaller = 0
        for x in self.get_edges():
            if x[2]['weight'] > t:
                count_bigger += 1
            elif x[2]['weight'] < t:
                count_smaller += 1
        return count_bigger, count_smaller
