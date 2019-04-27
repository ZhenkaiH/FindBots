# Put your solution here.
import networkx as nx
import random
import matplotlib.pyplot as plt 
def solve(client):
    client.end()
    client.start()
    nx.draw(client.G)
    plt.savefig("path.png")
    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    client.scout(random.choice(non_home), all_students)

    print("Guava",client.bots)
    for _ in range(100):
        u, v = random.choice(list(client.G.edges()))
        print(client.G[u][v]['weight'])
        client.remote(u, v)
    
    minw = 9999999
    maxw = 0
    edges = list(client.G.edges())
    for u, v in edges:
        if client.G[u][v]['weight'] < minw:
            minw = client.G[u][v]['weight']
    print(min,minw)
    client.end()
