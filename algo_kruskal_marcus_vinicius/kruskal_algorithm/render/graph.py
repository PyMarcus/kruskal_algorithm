import networkx as nx
import matplotlib.pyplot as plt


ORIGINAL = None
GLOBAL_POS = None


def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    graph = [list(map(int, line.strip().replace(';', '').split(','))) for line in lines]
    return graph


def visualize_graph(graph):
    global ORIGINAL, GLOBAL_POS

    G = nx.Graph()
    ORIGINAL = G
    for i in range(len(graph)):
        for j in range(i + 1, len(graph[i])):
            if graph[i][j] != 0:
                G.add_edge(i, j, weight=graph[i][j])

    pos = nx.spring_layout(G)
    GLOBAL_POS = pos
    labels = {(i, j): graph[i][j] for i, j, _ in G.edges(data=True)}

    nx.draw(G, pos, with_labels=True, labels={i: str(i) for i in G.nodes()}, node_size=700, node_color="skyblue",
            font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Graph")
    plt.savefig("static/image.jpg")
    # plt.show()


def kruskal_mst(graph):
    plt.close()

    G = nx.Graph()
    sum = 0
    edges = []

    for i in range(len(graph)):
        for j in range(i + 1, len(graph[i])):
            if graph[i][j] != 0:
                w = graph[i][j]
                edges.append((i, j, w))

    # ordena por peso
    edges.sort(key=lambda x: x[2])

    parent = [i for i in range(len(graph))]
    rank = [0] * len(graph)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)

        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1
            return True
        # forma ciclo:
        return False

    for edge in edges:
        u, v, weight = edge
        if union(u, v):
            G.add_edge(u, v, weight=weight)
            sum += weight

    with open("static/weight.txt", 'w') as f:
        f.write(str(sum))

    pos_original = nx.spring_layout(ORIGINAL)
    #sorted(G.nodes(), reverse=True)
    #pos = {node: pos_original[node] for node in G.nodes()}

    labels = {(u, v): weight for u, v, weight in G.edges(data='weight')}

    nx.draw(G, GLOBAL_POS, with_labels=True, labels={i: str(i) for i in G.nodes()}, node_size=724, node_color="lightgreen",
            font_size=16)
    nx.draw_networkx_edge_labels(G, GLOBAL_POS, edge_labels=labels)
    plt.title("Minimum Spanning Tree")
    # plt.show()
    plt.savefig("static/im.jpg")
