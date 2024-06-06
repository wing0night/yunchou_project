
import networkx as nx
import heapq

def dijkstra(G, start, edge_usage):
    queue = [(0, start, None)]  # 添加一个None记录前一个节点
    dist = {node: float('infinity') for node in G.nodes}
    prev = {node: None for node in G.nodes}  # 记录前一个节点
    dist[start] = 0

    while queue:
        d, node, prev_node = heapq.heappop(queue)
        if d > dist[node]:
            continue
        prev[node] = prev_node  # 记录前一个节点
        for neighbor in G.neighbors(node):
            # edge_weight = G[node][neighbor]['weight'] + G[node][neighbor].get('penalty', 0) + G[node][neighbor].get('deterioration', 0)  # 加上惩罚项和变化项
            edge_weight = G[node][neighbor]['weight'] + edge_usage[(node, neighbor)] * 4
            if dist[node] + edge_weight < dist[neighbor]:
                dist[neighbor] = dist[node] + edge_weight
                heapq.heappush(queue, (dist[neighbor], neighbor, node))  # 传递前一个节点信息到下一步
                # 统计边的通过次数，考虑边的节点按照字典序排序
                edge_usage[(node, neighbor)] += 1  # 统计边的通过次数
                edge_usage[(neighbor, node)] += 1  # 给一条路径的相反端点描述键值也加上1，不然会导致成为有向图

                #edge = (node, neighbor)  # 使用有序元组作为边的识别符
                #edge = tuple(sorted([node, neighbor]))  # 边的节点按照字典序排序
                #edge_usage[edge] += 1

    return dist, prev

def evacuate(G, S, D, Ts):
    edge_usage = {(u, v): 0 for u, v, d in G.edges(data=True)}  # 存放每个路径的通过次数
    new_edge_usage = {(v, u): 0 for u, v, d in G.edges(data=True)}  # 将同一条路径的反向键值也加进字典
    edge_usage.update(new_edge_usage)
    for s in S:
        dist, prev = dijkstra(G, s, edge_usage)
        dist_init = dist[0]
        for d in D:


            if dist[d] <= Ts:
                path = []
                node = d
                while node is not None:  # 从目的地一直回溯到起始节点
                    path.insert(0, node)
                    node = prev[node]
                path_str = ' -> '.join(path)
                print(f"Path from {s} to {d}: {path_str}, Distance: {dist[d]}")

    # 根据每条边被通过的次数更新宽敞度参数
    for (u, v), usage in edge_usage.items():
        capacity = G[u][v].get('capacity', 1)  # 假设初始宽敞度为1
        deterioration_factor = 0.1  # 宽敞度衰减因子
        deterioration = usage * deterioration_factor  # 根据通过次数更新衰减量
        new_capacity = max(0, capacity - deterioration)  # 更新后的宽敞度不能小于0
        G[u][v]['capacity'] = new_capacity

# 示例输入和设置的代码
G = nx.Graph()
# 输入节点和边
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

# 设置疏散原点、目的地和安全时限
S = ['22', '29', '20']
D = ['48', '43', '51']
Ts = 200

evacuate(G, S, D, Ts)

evacuate(G, S, D, Ts)