import networkx as nx
import heapq


def dijkstra(G, start):
    queue = [(0, start)]
    dist = {node: float('infinity') for node in G.nodes}
    dist[start] = 0

    while queue:
        d, node = heapq.heappop(queue)
        if d > dist[node]:
            continue
        for neighbor in G.neighbors(node):
            edge_weight = G[node][neighbor]['weight']
            if dist[node] + edge_weight < dist[neighbor]:
                dist[neighbor] = dist[node] + edge_weight
                heapq.heappush(queue, (dist[neighbor], neighbor))

    return dist


def evacuate(G, S, D, Ts):
    for s in S:
        dist = dijkstra(G, s)
        reachable_destinations = [d for d in D if dist[d] <= Ts]
        if reachable_destinations:
            print(f"Evacuate starting from {s} to destinations {reachable_destinations}")
        else:
            print(f"No reachable destinations within time limit for evacuation starting from {s}")


# 示例输入：路网G，疏散原点集合S，疏散目的地集合D，安全时限Ts
G = nx.Graph()

# 添加节点和边，并设置边的通行能力和节点的疏散人数属性
nodes = ['A1', 'E1', 'C1']
edges = [('A1', 'E1', {'weight': 18, 'capacity': 100}), ('E1', 'C1', {'weight': 12, 'capacity': 80})]

G.add_nodes_from(nodes)
G.add_edges_from(edges)

S = ['A1']
D = ['C1']
Ts = 20

evacuate(G, S, D, Ts)