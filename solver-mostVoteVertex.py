# Put your solution here.
import networkx as nx
import random
import matplotlib.pyplot as plt 
def solve(client):
    client.end()
    client.start()
    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    edges = list(client.G.edges())
    
    V = client.v + 1
    S = len(all_students)
    h = client.home

    usedEdges = []
    usedV = set()
    for i in range(V):
        usedEdges.append([-1] * V)
    
    posOfBots = []
    guessResults = [(-1, {}) for i in range(V)]
    reportTrue = [-1 for i in range(V)]

    def findShortestE():
        minW = 9999999
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
        print(reportTrue)
    guessAll()
    
    fromTheMostTrueV = 0
    def revealV():
        maxVoteNum = max(reportTrue)
        bestV = reportTrue.index(maxVoteNum)
        print("They claim that a bot is in ", bestV)
        get = client.remote(bestV, h)
        reportTrue[bestV] = -10
        if get == 1:
            return True

    for i in range(len(reportTrue)):
        maxVoteNum = max(reportTrue)
        if maxVoteNum >= 0:
            if fromTheMostTrueV < 5 and revealV():
                fromTheMostTrueV +=1
                print("WOW",client.bot_locations)



    # testedNodesNum = 0
    # while len(posOfBots) < 5:
    #     u, v, w = findShortestE()
    #     print("This time mini edge is",u,v,"with weight",w)
    #     testedNodesNum += 1
    #     print("Oyep!",client.scout(random.choice(non_home), all_students))
    #     # guessResults[u] = client.scout(u, all_students)
    #     # guessResults[v] = client.scout(v, all_students)
    #     # print(guessResults[u])
    #     posOfBots += [1]
        


    client.end()


