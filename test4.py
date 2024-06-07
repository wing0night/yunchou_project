import networkx as nx
import heapq
from tabulate import tabulate

def dijkstra(G, start):
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
            # edge_weight = G[node][neighbor]['weight'] + edge_usage[(node, neighbor)] * 4
            edge_weight = G[node][neighbor]['weight'] / (1 - (5 - G[node][neighbor]['capacity']) * 0.5)
            # edge_weight = G[node][neighbor]['weight']
            if dist[node] + edge_weight < dist[neighbor]:
                dist[neighbor] = dist[node] + edge_weight
                heapq.heappush(queue, (dist[neighbor], neighbor, node))  # 传递前一个节点信息到下一步
                # 统计边的通过次数，考虑边的节点按照字典序排序

                #edge = (node, neighbor)  # 使用有序元组作为边的识别符
                #edge = tuple(sorted([node, neighbor]))  # 边的节点按照字典序排序
                #edge_usage[edge] += 1

    return dist, prev

def evacuate(G, S, D, Ts):
    edge_usage = {(u, v): 0 for u, v, d in G.edges(data=True)}  # 存放每个路径的通过次数
    new_edge_usage = {(v, u): 0 for u, v, d in G.edges(data=True)}  # 将同一条路径的反向键值也加进字典
    edge_usage.update(new_edge_usage)
    for t in range(0, 5):  # 设置为循环10次
        rows = []
        edge_usage = {key: 0 for key in edge_usage}  # 每一次循环开头初始化edge_usage（后面计算是用已更新的capacity）
        for s in S:
            dist, prev = dijkstra(G, s)

            dist_init = 10000  # 创建int型的变量dist_init用于后面的对比
            for d in D:
                if dist[d] < dist_init:
                    dist_init = dist[d]
                    d_choose = d
            if dist[d_choose] <= Ts:
                path = []
                node = d_choose
                while node is not None:  # 从目的地一直回溯到起始节点
                    path.insert(0, node)
                    # 对于真的加到路径中的通过次数进行统计
                    neighbor = prev[node]
                    if neighbor is not None:
                        edge_usage[(node, neighbor)] += 1  # 统计边的通过次数
                        edge_usage[(neighbor, node)] += 1  # 给一条路径的相反端点描述键值也加上1，不然会导致成为有向图
                    node = prev[node]
                path_str = ' -> '.join(path)

                data = (("", f"Path from {s} to {d_choose}", f"{path_str}", f"Time: {dist[d_choose]}"))
                rows.append(data)

        headers = [f"Round: {t}", "route", "path", "Time"]
        table = tabulate(rows, headers, tablefmt="fancy_grid")
        print(table)

                # print(f"Path from {s} to {d_choose}: {path_str}, Time: {dist[d_choose]}")


        # 根据每条边被通过的次数更新宽敞度参数
        for key, value in edge_usage.items():
            # capacity = G[u][v]['capacity']  # 假设初始宽敞度为1
            # capacity = 1
            capacity = 5
            deterioration_factor = 0.1  # 宽敞度衰减因子 
            deterioration = value * deterioration_factor  # 根据通过次数更新衰减量
            new_capacity = max(3.1, capacity - deterioration)  # 更新后的宽敞度不能小于3
            G[key[0]][key[1]]['capacity'] = new_capacity


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
    ('1', '2', {'weight': 20, 'capacity': 10}), ('1', '3', {'weight': 8, 'capacity': 10}), ('1', '9', {'weight': 22, 'capacity': 10}), ('1', 'E1', {'weight': 8, 'capacity': 10}), ('1', 'C1', {'weight': 15, 'capacity': 10}),
    ('2', '8', {'weight': 35, 'capacity': 10}), ('2', '36', {'weight': 3, 'capacity': 10}), ('2', '34', {'weight': 30, 'capacity': 10}), ('2', 'C1', {'weight': 6, 'capacity': 10}), ('2', 'D1', {'weight': 23, 'capacity': 10}),
    ('3', '6', {'weight': 17, 'capacity': 10}), ('3', '4', {'weight': 23, 'capacity': 10}), ('3', 'F1', {'weight': 16, 'capacity': 10}),
    ('4', '7', {'weight': 25, 'capacity': 10}), ('4', 'F1', {'weight': 7, 'capacity': 10}), ('4', 'G1', {'weight': 10, 'capacity': 10}), ('4', '13', {'weight': 37, 'capacity': 10}),
    ('5', '7', {'weight': 13, 'capacity': 10}), ('5', '14', {'weight': 29, 'capacity': 10}), ('5', 'I1', {'weight': 17, 'capacity': 10}), ('5', '16', {'weight': 52, 'capacity': 10}),
    ('6', '11', {'weight': 31, 'capacity': 10}), ('6', '12', {'weight': 37, 'capacity': 10}), ('6', 'H1', {'weight': 19, 'capacity': 10}), ('6', 'F1', {'weight': 13, 'capacity': 10}),
    ('7', '8', {'weight': 27, 'capacity': 10}), ('7', 'J1', {'weight': 29, 'capacity': 10}), ('7', 'G1', {'weight': 12, 'capacity': 10}), ('7', '17', {'weight': 42, 'capacity': 10}),
    ('8', 'D1', {'weight': 23, 'capacity': 10}), ('8', '50', {'weight': 9, 'capacity': 10}),
    ('9', 'A1', {'weight': 11, 'capacity': 10}), ('9', 'B1', {'weight': 20, 'capacity': 10}), ('9', 'E1', {'weight': 13, 'capacity': 10}), ('9', '10', {'weight': 32, 'capacity': 10}), ('9', '37', {'weight': 35, 'capacity': 10}),
    ('10', '11', {'weight': 33, 'capacity': 10}), ('10', '26', {'weight': 8, 'capacity': 10}), ('10', '27', {'weight': 23, 'capacity': 10}), ('10', '38', {'weight': 37, 'capacity': 10}), ('10', 'B1', {'weight': 15, 'capacity': 10}),
    ('11', '25', {'weight': 16, 'capacity': 10}), ('11', 'H1', {'weight': 13, 'capacity': 10}),
    ('12', '25', {'weight': 9, 'capacity': 10}), ('12', '13', {'weight': 15, 'capacity': 10}),
    ('13', '14', {'weight': 7, 'capacity': 10}),
    ('14', '15', {'weight': 17, 'capacity': 10}), ('14', 'I1', {'weight': 17, 'capacity': 10}),
    ('15', '16', {'weight': 30, 'capacity': 10}), ('15', '32', {'weight': 22, 'capacity': 10}),
    ('16', '21', {'weight': 12, 'capacity': 10}), ('16', '33', {'weight': 27, 'capacity': 10}),
    ('17', '50', {'weight': 49, 'capacity': 10}), ('17', '18', {'weight': 22, 'capacity': 10}), ('17', 'J1', {'weight': 16, 'capacity': 10}),
    ('18', '19', {'weight': 10, 'capacity': 10}), ('18', '21', {'weight': 44, 'capacity': 10}),
    ('19', '20', {'weight': 21, 'capacity': 10}), ('19', '23', {'weight': 34, 'capacity': 10}),
    ('20', '22', {'weight': 29, 'capacity': 10}),
    ('21', '22', {'weight': 18, 'capacity': 10}),
    ('22', '24', {'weight': 18, 'capacity': 10}),
    ('23', '24', {'weight': 44, 'capacity': 10}),
    ('24', '49', {'weight': 54, 'capacity': 10}),
    ('25', '29', {'weight': 22, 'capacity': 10}),
    ('26', '40', {'weight': 36, 'capacity': 10}), ('26', '41', {'weight': 42, 'capacity': 10}),
    ('27', '43', {'weight': 30, 'capacity': 10}), ('27', '44', {'weight': 39, 'capacity': 10}),
    ('28', '45', {'weight': 33, 'capacity': 10}),
    ('29', '30', {'weight': 14, 'capacity': 10}),
    ('30', '31', {'weight': 12, 'capacity': 10}),
    ('31', '32', {'weight': 24, 'capacity': 10}), ('31', '46', {'weight': 30, 'capacity': 10}),
    ('32', '47', {'weight': 32, 'capacity': 10}),
    ('33', '47', {'weight': 43, 'capacity': 10}), ('33', '48', {'weight': 39, 'capacity': 10}),
    ('34', '35', {'weight': 42, 'capacity': 10}), ('34', '50', {'weight': 31, 'capacity': 10}),
    ('35', '36', {'weight': 21, 'capacity': 10}),
    ('36', '37', {'weight': 16, 'capacity': 10}),
    ('37', '38', {'weight': 26, 'capacity': 10}),
    ('38', '39', {'weight': 37, 'capacity': 10}),
    ('39', '40', {'weight': 10, 'capacity': 10}),
    ('40', '41', {'weight': 36, 'capacity': 10}),
    ('41', '42', {'weight': 13, 'capacity': 10}),
    ('42', '43', {'weight': 28, 'capacity': 10}),
    ('43', '44', {'weight': 26, 'capacity': 10}),
    ('44', '45', {'weight': 7, 'capacity': 10}),
    ('45', '51', {'weight': 35, 'capacity': 10}),
    ('46', '47', {'weight': 12, 'capacity': 10}), ('46', '51', {'weight': 20, 'capacity': 10}),
    ('47', '48', {'weight': 45, 'capacity': 10}),
    ('48', '49', {'weight': 18, 'capacity': 10}),
    ('45', '51', {'weight': 35, 'capacity': 10}),

]

# new_edges = [(u, v, {**data}, {'capacity': 1}) for u, v, data in edges]  # 添加capacity键（都赋值为1）
# edges['capacity'] = 1

G.add_edges_from(edges)

# 设置疏散原点、目的地和安全时限
S = ['35', '36', '37']
D = ['48', '43', '51']
Ts = 200

evacuate(G, S, D, Ts)

