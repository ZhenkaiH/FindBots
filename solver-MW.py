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
    halfV = client.v / 2

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

        def revealV(bestVW):
            print("They claim that a bot is in ", bestVW)
            get = client.remote(bestVW, h)
            #Make sure we don't use this vertex again, assign a negative value
            reportTrue[bestVW] = -10
            if get == 1:
                return bestVW, True
            else:
                return bestVW, False

        epsilon = 1 - 0.910298
        #Adjust weights of students and return whether we remote a bot to home
        def studentsWeightAdjust(v, result):
            print("ssssssMW")
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
        
        


    while fromTheMostTrueV < 5:
        if multiWeightsDecide():
            fromTheMostTrueV +=1

    



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


