# Put your solution here.
import networkx as nx
import random
import math
import queue
luckyStudent = -1
def solve(client):
    client.end()
    client.start()

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
            global luckyStudent
            if luckyStudent == -1:
                reportTrueW = [-1 for i in range(V)]
                for v, guess in guessResults:
                    if v != -1 and v not in usedV:
                        thinkBotHereW = 0
                        for s in range(1, client.students + 1):
                            if guess[s]:
                                thinkBotHereW += 1 * studentWeights[s]
                        reportTrueW[v] = thinkBotHereW
            else:
                for v, guess in guessResults:
                    if v != -1 and v not in usedV:
                        if guess[luckyStudent]:
                            usedV.add(v)
                            return v
                return -1
            
            maxVoteNumW = max(reportTrueW)
            if maxVoteNumW >= 0:
                bestVW = reportTrueW.index(maxVoteNumW)
                usedV.add(bestVW)
                return bestVW
            else:
                print("bestVwithMW: maxVoteNumW Error")
                return 0

        # Try remote on BESTVW with the first edge in shortest path to home
        # The goal is get location of bot
        def revealV(bestVW):
            #Make sure we don't use this vertex again, assign a negative value
            reportTrue[bestVW] = -10
            Homepath = dijkstra(bestVW, h)
            get = client.remote(Homepath[0], Homepath[1])
            if get == 0:
                return bestVW, False
            return bestVW, True


        #Lucky student who got wrong |V|/2 times
        
        # 0.910298 is number which has: (0.910298) ^ 49 = 0.01
        # Because if a student scout 49 times right, his scouting result becomes unreliable!
        # 49 is the half of vertices numbers (99 / 2)
        # Feel free to tweak 0.910298
        epsilon = 1 - 0.910298
        #Adjust weights of students and return whether we remote a bot to home
        def studentsWeightAdjust(v, result):
            global luckyStudent
            v, guess = guessResults[v]
            if luckyStudent != -1:
                return True
            if result:
                for s in range(1, client.students + 1):
                    if guess[s]:
                        #Since s is right, the probability of guess right on next time will be smaller
                        studentWeights[s] = studentWeights[s] * (1 - epsilon)
                    else:
                        studentWrongtimes[s] += 1
                        if studentWrongtimes[s] >= 50:
                            luckyStudent = s
                            return True
                sWeightSUM = sum(studentWeights, 1)
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
                        if studentWrongtimes[s] >= 50:
                            luckyStudent = s
                            return False
                sWeightSUM = sum(studentWeights, 1)
                for s in range(1, client.students + 1):
                    studentWeights[s] = studentWeights[s] / sWeightSUM
                return False

        vertexRemoted, result = revealV(bestVwithMW())
        return studentsWeightAdjust(vertexRemoted, result)

    #A Dijkstra return path from S to T.
    def dijkstra(s, t):
        if s != t:
            dist = [math.inf for i in range(V)]
            prev = [-1 for i in range(V)]
            dist[s] = 0
            H = queue.PriorityQueue()
            for v in range(1, V):
                H.put((dist[v],v))
            while not H.empty():
                uPair = H.get()
                u = uPair[1]
                for v in range(1,V):
                    if u != v:
                        edgeWeight = client.G[u][v]['weight']
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
        else:
            return 0

    #Calculate the total weight of entire PATH which from s to t
    def pathCost(path):
        cost = 0
        for i in range(len(path) - 1):
            cost += client.G[path[i]][path[i+1]]['weight']
        return cost


    #Find a lowest cost vertex for bot (labeled with its location) in BOTS to be together!
    #All bots must go there on their own
    def goodVToMeet(bots):
        lowestCost = math.inf
        goodV = -1
        for v in range(1, V):
            totalCost = 0
            for b in bots:
                if b != v and b != h:
                    bCost = pathCost(dijkstra(b, v))
                    totalCost += bCost
            if totalCost < lowestCost:
                lowestCost = totalCost
                goodV = v
        return lowestCost, [goodV] * len(bots)

    def goTo(path):
        if path != 0 and len(path) > 0:
            for i in range(len(path) - 1):
                client.remote(path[i], path[i+1])



    

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
    
    #Determine the location of bots
    while len(client.bot_locations) < 5:
        multiWeightsDecide()

    #Get meeting vertex. It takes long time to run it.
    meetV = goodVToMeet(client.bot_locations)

    #All bots go to meeting vertex
    for b in client.bot_locations:
        if b != meetV[1][0] and b != h and client.bot_count[h] < 5:
            goTo(dijkstra(b, meetV[1][0]))
    

    #All bots go home
    if client.bot_count[h] < 5:
        finalPath = dijkstra(meetV[1][0], h)
        goTo(finalPath)
            
    client.end()


