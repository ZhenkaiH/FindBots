# Put your solution here.
import networkx as nx
import random
import matplotlib.pyplot as plt
import math
import queue
def solve(client):
    client.end()
    client.start()
    def findShortestE():
        minW = math.inf
        minU, minV = -1, -1
        for u, v in edges:
            if client.G[u][v]['weight'] < minW and usedEdges[u][v] == -1:
                minU, minV, minW = u, v, client.G[u][v]['weight']
        usedEdges[minU][minV], usedEdges[minV][minU] = minW, minW
        return minU, minV, minW

    def guessAll():
        for v in non_home:
            guess = client.scout(v, all_students)
            guessResults[v] = (v, guess)
            thinkBotHere = 0
            for s in range(1, client.students + 1):
                if guess[s]:
                    thinkBotHere += 1
            reportTrue[v] = thinkBotHere


    #W in variable means weighted.
    def multiWeightsDecide():
        def bestVwithMW():
            reportTrueW = [-1 for i in range(V)]
            for v, guess in guessResults:
                if v != -1 and v not in usedV:
                    thinkBotHereW = 0
                    for s in range(1, client.students + 1):
                        if guess[s]:
                            thinkBotHereW += 1 * studentWeights[s]
                    reportTrueW[v] = thinkBotHereW
            
            maxVoteNumW = max(reportTrueW)
            if maxVoteNumW >= 0:
                bestVW = reportTrueW.index(maxVoteNumW)
                usedV.add(bestVW)
                return bestVW
            else:
                print("bestVwithMW: maxVoteNumW Error")
                return 0

        # Try remote the bot on BESTVW with the first edge in shortest path to home
        # If it works, remote bot to home
        def revealV(bestVW):
            print("Home",h)
            Homepath = dijkstra(bestVW, h)
            print("Homepath",Homepath)
            HomeCost = 0
            for i in range(len(Homepath) - 1):
                HomeCost += client.G[Homepath[i]][Homepath[i+1]]['weight']
            print("Homecost",HomeCost)
            print("direct to home cost", client.G[bestVW][h]['weight'])
            #Make sure we don't use this vertex again, assign a negative value
            reportTrue[bestVW] = -10
            for i in range(len(Homepath) - 1):
                get = client.remote(Homepath[i], Homepath[i+1])
                if get == 0:
                    return bestVW, False
            return bestVW, True


        epsilon = 1 - 0.910298
        #Adjust weights of students and return whether we remote a bot to home
        def studentsWeightAdjust(v, result):
            v, guess = guessResults[v]
            if result:
                for s in range(1, client.students + 1):
                    if guess[s]:
                        #Since s is right, the probability of guess right on next time will be smaller
                        studentWeights[s] = studentWeights[s] * (1 - epsilon)
                    else:
                        studentWrongtimes[s] += 1
                sWeightSUM = sum(studentWeights, 1)
                # x_i = w_s / sum(w)
                for s in range(1, client.students + 1):
                    studentWeights[s] = studentWeights[s] / sWeightSUM
                return True
            else:
                for s in range(1, client.students + 1):
                    if not guess[s]:
                        #Since s is right, the probability of guess right on next time will be smaller
                        studentWeights[s] = studentWeights[s] * (1 - epsilon)
                    else:
                        studentWrongtimes[s] += 1
                sWeightSUM = sum(studentWeights, 1)
                # x_i = w_s / sum(w)
                for s in range(1, client.students + 1):
                    studentWeights[s] = studentWeights[s] / sWeightSUM
                return False

        vertexRemoted, result = revealV(bestVwithMW())
        return studentsWeightAdjust(vertexRemoted, result)

    #A Dijkstra return path from S to T.
    def dijkstra(s, t):
        dist = [math.inf for i in range(V)]
        prev = [-1 for i in range(V)]
        dist[s] = 0
        H = queue.PriorityQueue()
        for v in range(1, V):
            H.put((dist[v],v))
        while not H.empty():
            uPair = H.get()
            u = uPair[1]
            # print("u",u)
            for v in range(1,V):
                if u != v:
                    # print("u",u,"v",v)
                    edgeWeight = client.G[u][v]['weight']
                    # print("edgeWeight",edgeWeight)
                    if dist[v] > dist[u] + edgeWeight:
                        dist[v] =  dist[u] + edgeWeight
                        H.put((dist[v],v))
                        prev[v] = u
        path = []
        pointer = t
        while pointer != s:
            path.append(pointer)
            pointer = prev[pointer]
        path.append(pointer)
        return path[::-1]




    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    edges = list(client.G.edges())
    
    V = client.v + 1
    S = len(all_students)
    h = client.home
    halfV = client.v / 2
    fromTheMostTrueV = 0

    usedEdges = []
    usedV = set()
    for i in range(V):
        usedEdges.append([-1] * V)
    posOfBots = []
    guessResults = [(-1, {}) for i in range(V)]
    reportTrue = [-1 for i in range(V)]

    #Because the index of students starts from 1
    studentWeights = [0] + [1 for i in range(1, client.students + 1)]
    studentWrongtimes = [0] + [0 for i in range(1, client.students + 1)]

        
    guessAll()
    


    while len(client.bot_locations) < 5:
        multiWeightsDecide()


    client.end()


