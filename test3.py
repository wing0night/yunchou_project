
import networkx as nx
import heapq
import random


def dijkstra(G, start):
    queue = [(0, start)]
    dist = {node: float('infinity') for node in G.nodes}
    dist[start] = 0

    while queue:
        d, node = heapq.heappop(queue)
        if d > dist[node]:
            continue
        for neighbor in G.neighbors(node):
            edge_weight = G[node][neighbor]['weight'] + G[node][neighbor].get('penalty', 0)  # 加上惩罚项
            if dist[node] + edge_weight < dist[neighbor]:
                dist[neighbor] = dist[node] + edge_weight
                heapq.heappush(queue, (dist[neighbor], neighbor))

    return dist


def evacuate(G, S, D, Ts):
    all_paths = {}
    for s in S:
        dist = dijkstra(G, s)
        reachable_destinations = [d for d in D if dist[d] <= Ts]
        if reachable_destinations:
            for d in reachable_destinations:
                all_paths[(s, d)] = dist[d]

    # 计算出每条路径的宽敞度，根据人数和惩罚项计算，这里使用随机生成的数模拟
    paths = {node: [] for node in D}
    total_people = sum([random.randint(1, 10) for _ in range(len(S))])
    for (s, d), distance in all_paths.items():
        proportion = random.randint(1, 10) / total_people
        paths[d].append((s, proportion, distance))

    for node in D:
        paths[node] = sorted(paths[node], key=lambda x: x[1], reverse=True)  # 按人数占比排序
        print(f"路径信息：")
        for (s, proportion, distance) in paths[node]:
            print(f"{s}中{proportion}的人的路线为Path to {node}: {' -> '.join(s for s, _ in paths[node])}, Distance: {distance}")

# 示例输入：路网G，疏散原点集合S，疏散目的地集合D，安全时限Ts
G = nx.Graph()
nodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
        '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
        '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
        '51', 'A1', 'B1', 'C1', 'D1', 'E1', 'F1',
        'G1', 'H1', 'I1', 'J1'
        ]
G.add_nodes_from(nodes)

edges = [
    ('1', '2', {'weight': 20}), ('1', '3', {'weight': 8}), ('1', '9', {'weight': 22}), ('1', 'E1', {'weight': 8}), ('1', 'C1', {'weight': 15}),
    ('2', '8', {'weight': 35}), ('2', '36', {'weight': 3}), ('2', '34', {'weight': 30}), ('2', 'C1', {'weight': 6}), ('2', 'D1', {'weight': 23}),
    ('3', '6', {'weight': 17}), ('3', '4', {'weight': 23}), ('3', 'F1', {'weight': 16}),
    ('4', '7', {'weight': 25}), ('4', 'F1', {'weight': 7}), ('4', 'G1', {'weight': 10}), ('4', '13', {'weight': 37}),
    ('5', '7', {'weight': 13}), ('5', '14', {'weight': 29}), ('5', 'I1', {'weight': 17}), ('5', '16', {'weight': 52}),
    ('6', '11', {'weight': 31}), ('6', '12', {'weight': 37}), ('6', 'H1', {'weight': 19}), ('6', 'F1', {'weight': 13}),
    ('7', '8', {'weight': 27}), ('7', 'J1', {'weight': 29}), ('7', 'G1', {'weight': 12}), ('7', '17', {'weight': 42}),
    ('8', 'D1', {'weight': 23}), ('8', '50', {'weight': 9}),
    ('9', 'A1', {'weight': 11}), ('9', 'B1', {'weight': 20}), ('9', 'E1', {'weight': 13}), ('9', '10', {'weight': 32}), ('9', '37', {'weight': 35}),
    ('10', '11', {'weight': 33}), ('10', '26', {'weight': 8}), ('10', '27', {'weight': 23}), ('10', '38', {'weight': 37}), ('10', 'B1', {'weight': 15}),
    ('11', '25', {'weight': 16}), ('11', 'H1', {'weight': 13}),
    ('12', '25', {'weight': 9}), ('12', '13', {'weight': 15}),
    ('13', '14', {'weight': 7}),
    ('14', '15', {'weight': 17}), ('14', 'I1', {'weight': 17}),
    ('15', '16', {'weight': 30}), ('15', '32', {'weight': 22}),
    ('16', '21', {'weight': 12}), ('16', '33', {'weight': 27}),
    ('17', '50', {'weight': 49}), ('17', '18', {'weight': 22}), ('17', 'J1', {'weight': 16}),
    ('18', '19', {'weight': 10}), ('18', '21', {'weight': 44}),
    ('19', '20', {'weight': 21}), ('19', '23', {'weight': 34}),
    ('20', '22', {'weight': 29}),
    ('21', '22', {'weight': 18}),
    ('22', '24', {'weight': 18}),
    ('23', '24', {'weight': 44}),
    ('24', '49', {'weight': 54}),
    ('25', '29', {'weight': 22}),
    ('26', '40', {'weight': 36}), ('26', '41', {'weight': 42}),
    ('27', '43', {'weight': 30}), ('27', '44', {'weight': 39}),
    ('28', '45', {'weight': 33}),
    ('29', '30', {'weight': 14}),
    ('30', '31', {'weight': 12}),
    ('31', '32', {'weight': 24}), ('31', '46', {'weight': 30}),
    ('32', '47', {'weight': 32}),
    ('33', '47', {'weight': 43}), ('33', '48', {'weight': 39}),
    ('34', '35', {'weight': 42}), ('34', '50', {'weight': 31}),
    ('35', '36', {'weight': 21}),
    ('36', '37', {'weight': 16}),
    ('37', '38', {'weight': 26}),
    ('38', '39', {'weight': 37}),
    ('39', '40', {'weight': 10}),
    ('40', '41', {'weight': 36}),
    ('41', '42', {'weight': 13}),
    ('42', '43', {'weight': 28}),
    ('43', '44', {'weight': 26}),
    ('44', '45', {'weight': 7}),
    ('45', '51', {'weight': 35}),
    ('46', '47', {'weight': 12}), ('46', '51', {'weight': 20}),
    ('47', '48', {'weight': 45}),
    ('48', '49', {'weight': 18}),
    ('45', '51', {'weight': 35}),
]

G.add_edges_from(edges)

S = ['A1', 'B1', 'E1', 'H1', 'F1', 'G1', 'C1', 'D1', 'J1', 'I1']
D = ['41', '43', '48', '49', '51']
Ts = 200

evacuate(G, S, D, Ts)