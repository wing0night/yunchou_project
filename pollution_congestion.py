import networkx as nx
import heapq
from tabulate import tabulate
import re

my_list = []
pathdata = []
my_data = [
    {'rfk': ('A1', '39'), 'Tfk_v_road': 10, 'Mf': 10, 'Bk': 100},
    {'rfk': ('A1', '10'), 'Tfk_v_road': 10, 'Mf': 10, 'Bk': 60},
    {'rfk': ('A1', '11'), 'Tfk_v_road': 10, 'Mf': 10, 'Bk': 50},
    {'rfk': ('A1', '12'), 'Tfk_v_road': 10, 'Mf': 10, 'Bk': 40},
    {'rfk': ('A1', 'J1'), 'Tfk_v_road': 10, 'Mf': 10, 'Bk': 80},
    {'rfk': ('B1', '39'), 'Tfk_v_road': 10, 'Mf': 50, 'Bk': 100},
    {'rfk': ('B1', '10'), 'Tfk_v_road': 10, 'Mf': 50, 'Bk': 60},
    {'rfk': ('B1', '11'), 'Tfk_v_road': 10, 'Mf': 50, 'Bk': 50},
    {'rfk': ('B1', '12'), 'Tfk_v_road': 10, 'Mf': 50, 'Bk': 40},
    {'rfk': ('B1', 'J1'), 'Tfk_v_road': 10, 'Mf': 50, 'Bk': 80},
    {'rfk': ('E1', '39'), 'Tfk_v_road': 10, 'Mf': 30, 'Bk': 100},
    {'rfk': ('E1', '10'), 'Tfk_v_road': 10, 'Mf': 30, 'Bk': 60},
    {'rfk': ('E1', '11'), 'Tfk_v_road': 10, 'Mf': 30, 'Bk': 50},
    {'rfk': ('E1', '12'), 'Tfk_v_road': 10, 'Mf': 30, 'Bk': 40},
    {'rfk': ('E1', 'J1'), 'Tfk_v_road': 10, 'Mf': 30, 'Bk': 80},
    {'rfk': ('C1', '39'), 'Tfk_v_road': 10, 'Mf': 20, 'Bk': 100},
    {'rfk': ('C1', '10'), 'Tfk_v_road': 10, 'Mf': 20, 'Bk': 60},
    {'rfk': ('C1', '11'), 'Tfk_v_road': 10, 'Mf': 20, 'Bk': 50},
    {'rfk': ('C1', '12'), 'Tfk_v_road': 10, 'Mf': 20, 'Bk': 40},
    {'rfk': ('C1', 'J1'), 'Tfk_v_road': 10, 'Mf': 20, 'Bk': 80},
    {'rfk': ('D1', '39'), 'Tfk_v_road': 10, 'Mf': 80, 'Bk': 100},
    {'rfk': ('D1', '10'), 'Tfk_v_road': 10, 'Mf': 80, 'Bk': 60},
    {'rfk': ('D1', '11'), 'Tfk_v_road': 10, 'Mf': 80, 'Bk': 50},
    {'rfk': ('D1', '12'), 'Tfk_v_road': 10, 'Mf': 80, 'Bk': 40},
    {'rfk': ('D1', 'J1'), 'Tfk_v_road': 10, 'Mf': 80, 'Bk': 100},
]
my_data_cp = []  # 在副本上进行修改，以便后续循环继续调用完好的my_data

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
            # 添加惩罚项的道路权值函数
            if G[node][neighbor]['capacity'] <= 5:  # 进行判断，当道路容纳量小于5时才添加惩罚项
                # edge_weight = G[node][neighbor]['weight'] + G[node][neighbor]['weight'](1 - (5 - G[node][neighbor]['capacity']) * 0.5)
                edge_weight = G[node][neighbor]['weight'] + G[node][neighbor]['Concentration'] * G[node][neighbor]['weight'] / (G[node][neighbor]['capacity'] / 5 * 1.4)

            else:
                edge_weight = G[node][neighbor]['weight']

            if dist[node] + edge_weight < dist[neighbor]:
                dist[neighbor] = dist[node] + edge_weight
                heapq.heappush(queue, (dist[neighbor], neighbor, node))  # 传递前一个节点信息到下一步

    return dist, prev

def evacuate(G, S, D, Ts):
    global pathdata
    global my_data
    global my_data_cp
    my_data_cp = my_data.copy()

    edge_usage = {(u, v): 0 for u, v, d in G.edges(data=True)}  # 存放每个路径的通过次数
    new_edge_usage = {(v, u): 0 for u, v, d in G.edges(data=True)}  # 将同一条路径的反向键值也加进字典
    edge_usage.update(new_edge_usage)
    for t in range(0, 1):  # 设置为循环5次
        rows = []
        edge_usage = {key: 0 for key in edge_usage}  # 每一次循环开头初始化edge_usage（后面计算是用已更新的capacity）
        for s in S:
            dist, prev = dijkstra(G, s)

            # dist_init = 10000  # 创建int型的变量dist_init用于后面的对比
            for d in D:
                '''if dist[d] < dist_init:
                    dist_init = dist[d]
                    d_choose = d'''  # 将所有路径输出，不再设置d_choose
                for i in range(0, 25):  # 将Dijkstra规划的结果更新到data字典中
                    if my_data_cp[i]['rfk'][0] == s and my_data_cp[i]['rfk'][1] == d:
                        my_data_cp[i]['Tfk_v_road'] = dist[d]

                if dist[d] <= Ts:
                    path = []
                    node = d
                    while node is not None:  # 从目的地一直回溯到起始节点
                        path.insert(0, node)
                        # 对于真的加到路径中的通过次数进行统计
                        neighbor = prev[node]
                        if neighbor is not None:
                            edge_usage[(node, neighbor)] += 1  # 统计边的通过次数
                            edge_usage[(neighbor, node)] += 1  # 给一条路径的相反端点描述键值也加上1，不然会导致成为有向图
                        node = prev[node]
                    path_str = ' -> '.join(path)

                    data = (("", f"Path from {s} to {d}", f"{path_str}", f"H: {dist[d]}"))
                    rows.append(data)
                    data_itm = {'s': f"{s}", 'd': f"{d}", 'Path': f"{path_str}", 'Time': dist[d]}
                    pathdata.append(data_itm)

        # 表格输出
        headers = [f"Dijkstra", "route", "path", "Harm"]
        table = tabulate(rows, headers, tablefmt="fancy_grid")
        print(table)

        my_list.append(rows)  # 将规划路径输出到全局列表

        # 根据每条边被通过的次数更新宽敞度参数
        for key, value in edge_usage.items():
            deterioration_factor = 0.1  # 宽敞度衰减因子
            deterioration = value * deterioration_factor  # 根据通过次数更新衰减量
            new_capacity = max(3.1, G[key[0]][key[1]]['capacity'] - deterioration)  # 更新后的宽敞度不能小于3
            G[key[0]][key[1]]['capacity'] = new_capacity

def adjust():
    """
    实现 Adust 算法

    Args:
        data: 一个列表, 每个元素是一个字典, 包含 'rfk', 'Tfk_v_road', 'Mf', 'Bk' 四个键值对

    Returns:
        一个列表, 包含经过 Adust 算法处理后的字典
    """
    global pathdata
    global my_data_cp

    # Step 1: 按 Tfk_v_road 由小到大排序
    my_data_cp.sort(key=lambda item: item['Tfk_v_road'])
    pathdata.sort(key=lambda item: item['Time'])

    # Step 2 & 3: 循环处理每个字典
    i = 0
    while i < len(my_data_cp):
        f1 = my_data_cp[i]['rfk'][0]  # 获取人群节点
        k1 = my_data_cp[i]['rfk'][1]  # 获取出口节点
        Mf1 = my_data_cp[i]['Mf']  # 获取人群节点人数
        Bk1 = my_data_cp[i]['Bk']  # 获取出口节点理论疏散人数

        # Step 2: 人群节点人数小于出口理论疏散人数
        if Mf1 < Bk1:
            for item in my_data_cp:
                if item['rfk'][0] == f1:
                    print(f"起点{f1} {Mf1} 人的疏散出口为 {k1}：{pathdata[i]['Path']}。规划目标z = {my_data_cp[i]['Tfk_v_road']}。{f1} 完成疏散")
            # 删除人群节点为 f1 的所有字典
                    # 提取path中的路段并更新其capacity用于下次循环计算
                    result = re.findall(r'\w+', pathdata[i]['Path'])
                    for i in range(0, len(result)-1):
                        G[result[i]][result[i+1]]['capacity'] = G[result[i]][result[i+1]]['capacity'] - Mf1 / 20  # 根据通过的人数更新道路capacity
                        if G[result[i]][result[i+1]]['capacity'] <= 1:
                            G[result[i]][result[i+1]]['capacity'] = 1  # 设置一个下限

                    my_data_cp = [item for item in my_data_cp if item['rfk'][0] != f1]
                    pathdata = [item for item in pathdata if item['s'] != f1]
                    break

            # 更新出口节点 k1 剩余疏散人数
            for item in my_data_cp:
                if item['rfk'][1] == k1:
                    item['Bk'] = Bk1 - Mf1

            # 重复 Step 1
            my_data_cp.sort(key=lambda item: item['Tfk_v_road'])
            i = 0  # 从头开始重新遍历

        elif Mf1 == Bk1:
            for item in my_data_cp:
                if item['rfk'][1] == k1 and item['rfk'][0] == f1:
                    print(f"起点{f1}刚好全部 {Mf1} 人的疏散出口为 {k1}：{pathdata[i]['Path']}。规划目标z = {my_data_cp[i]['Tfk_v_road']}。出口{k1} 刚好达到人数容量")

                    # 提取path中的路段并更新其capacity用于下次循环计算
                    result = re.findall(r'\w+', pathdata[i]['Path'])

                    for i in range(0, len(result) - 1):
                        G[result[i]][result[i + 1]]['capacity'] = G[result[i]][result[i + 1]][
                                                                      'capacity'] - Mf1 / 20  # 根据通过的人数更新道路capacity
                        if G[result[i]][result[i + 1]]['capacity'] <= 1:
                            G[result[i]][result[i + 1]]['capacity'] = 1  # 设置一个下限

                    # 删除人群节点为 f1 的所有字典
                    my_data_cp = [item for item in my_data_cp if item['rfk'][0] != f1]
                    pathdata = [item for item in pathdata if item['s'] != f1]

                    # 删除出口节点为 k1 的所有字典
                    my_data_cp = [item for item in my_data_cp if item['rfk'][1] != k1]
                    pathdata = [item for item in pathdata if item['d'] != k1]

                    break

            # 重复 Step 1
            my_data_cp.sort(key=lambda item: item['Tfk_v_road'])
            i = 0  # 从头开始重新遍历


        # Step 3: 人群节点人数大于出口理论疏散人数
        else:
            for item in my_data_cp:
                if item['rfk'][1] == k1:
                    print(f"起点{f1} {Bk1} 人的疏散出口为 {k1}：{pathdata[i]['Path']}。规划目标z = {my_data_cp[i]['Tfk_v_road']}。出口{k1} 达到人数容量")

                    # 提取path中的路段并更新其capacity用于下次循环计算
                    result = re.findall(r'\w+', pathdata[i]['Path'])

                    for i in range(0, len(result) - 1):
                        G[result[i]][result[i + 1]]['capacity'] = G[result[i]][result[i + 1]][
                                                                      'capacity'] - Mf1 / 20  # 根据通过的人数更新道路capacity
                        if G[result[i]][result[i + 1]]['capacity'] <= 1:
                            G[result[i]][result[i + 1]]['capacity'] = 1  # 设置一个下限

                    # 删除出口节点为 k1 的所有字典
                    my_data_cp = [item for item in my_data_cp if item['rfk'][1] != k1]
                    pathdata = [item for item in pathdata if item['d'] != k1]
                    break

            # 更新人群节点 f1 剩余人数
            for item in my_data_cp:
                if item['rfk'][0] == f1:
                    item['Mf'] = Mf1 - Bk1

            # 重复 Step 1
            my_data_cp.sort(key=lambda item: item['Tfk_v_road'])
            i = 0  # 从头开始重新遍历

        i += 1  # 移动到下一个字典

    return my_data_cp

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
    ('1', '2', {'weight': 20, 'capacity': 5, 'Concentration': 4.9275}), ('1', '3', {'weight': 8, 'capacity': 10, 'Concentration': 2.1351}), ('1', '9', {'weight': 22, 'capacity': 10, 'Concentration': 0}), ('1', 'E1', {'weight': 8, 'capacity': 10, 'Concentration': 2.1351}), ('1', 'C1', {'weight': 15, 'capacity': 10, 'Concentration': 2.1351}),
    ('2', '8', {'weight': 35, 'capacity': 5, 'Concentration': 4.9275}), ('2', '36', {'weight': 3, 'capacity': 10, 'Concentration': 4.9275}), ('2', '34', {'weight': 30, 'capacity': 10, 'Concentration': 4.9275}), ('2', 'C1', {'weight': 6, 'capacity': 10, 'Concentration': 4.9275}), ('2', 'D1', {'weight': 23, 'capacity': 10, 'Concentration': 4.9275}),
    ('3', '6', {'weight': 17, 'capacity': 5, 'Concentration': 0.7789}), ('3', '4', {'weight': 23, 'capacity': 10, 'Concentration': 2.1351}), ('3', 'F1', {'weight': 16, 'capacity': 10, 'Concentration': 2.1351}),
    ('4', '7', {'weight': 25, 'capacity': 5, 'Concentration': 0}), ('4', 'F1', {'weight': 7, 'capacity': 10, 'Concentration': 2.1351}), ('4', 'G1', {'weight': 10, 'capacity': 10, 'Concentration': 0.7789}), ('4', '13', {'weight': 37, 'capacity': 10, 'Concentration': 0}),
    ('5', '7', {'weight': 13, 'capacity': 5, 'Concentration': 0}), ('5', '14', {'weight': 29, 'capacity': 10, 'Concentration': 0}), ('5', 'I1', {'weight': 17, 'capacity': 10, 'Concentration': 0.2295}), ('5', '16', {'weight': 52, 'capacity': 10, 'Concentration': 0}),
    ('6', '11', {'weight': 31, 'capacity': 5, 'Concentration': 0}), ('6', '12', {'weight': 37, 'capacity': 10, 'Concentration': 0.2295}), ('6', 'H1', {'weight': 19, 'capacity': 10, 'Concentration': 0.7789}), ('6', 'F1', {'weight': 13, 'capacity': 10, 'Concentration': 0}),
    ('7', '8', {'weight': 27, 'capacity': 10, 'Concentration': 0.7789}), ('7', 'J1', {'weight': 29, 'capacity': 10, 'Concentration': 0.2295}), ('7', 'G1', {'weight': 12, 'capacity': 10, 'Concentration': 0.7789}), ('7', '17', {'weight': 42, 'capacity': 10, 'Concentration': 0}),
    ('8', 'D1', {'weight': 23, 'capacity': 10, 'Concentration': 2.1351}), ('8', '50', {'weight': 9, 'capacity': 10, 'Concentration': 0.7789}),
    ('9', 'A1', {'weight': 11, 'capacity': 10, 'Concentration': 0.7789}), ('9', 'B1', {'weight': 20, 'capacity': 10, 'Concentration': 0}), ('9', 'E1', {'weight': 13, 'capacity': 10, 'Concentration': 0.7789}), ('9', '10', {'weight': 32, 'capacity': 10, 'Concentration': 0}), ('9', '37', {'weight': 35, 'capacity': 10, 'Concentration': 0.7789}),
    ('10', '11', {'weight': 33, 'capacity': 10, 'Concentration': 0}), ('10', '26', {'weight': 8, 'capacity': 10, 'Concentration': 0}), ('10', '27', {'weight': 23, 'capacity': 10, 'Concentration': 0}), ('10', '38', {'weight': 37, 'capacity': 10, 'Concentration': 0}), ('10', 'B1', {'weight': 15, 'capacity': 10, 'Concentration': 0.2295}),
    ('11', '25', {'weight': 16, 'capacity': 10, 'Concentration': 0}), ('11', 'H1', {'weight': 13, 'capacity': 10, 'Concentration': 0.2295}),
    ('12', '25', {'weight': 9, 'capacity': 10, 'Concentration': 0}), ('12', '13', {'weight': 15, 'capacity': 10, 'Concentration': 0}),
    ('13', '14', {'weight': 7, 'capacity': 10, 'Concentration': 0}),
    ('14', '15', {'weight': 17, 'capacity': 10, 'Concentration': 0}), ('14', 'I1', {'weight': 17, 'capacity': 10, 'Concentration': 0.2295}),
    ('15', '16', {'weight': 30, 'capacity': 10, 'Concentration': 0}), ('15', '32', {'weight': 22, 'capacity': 10, 'Concentration': 0}),
    ('16', '21', {'weight': 12, 'capacity': 10, 'Concentration': 0}), ('16', '33', {'weight': 27, 'capacity': 10, 'Concentration': 0}),
    ('17', '50', {'weight': 49, 'capacity': 10, 'Concentration': 0}), ('17', '18', {'weight': 22, 'capacity': 10, 'Concentration': 0}), ('17', 'J1', {'weight': 16, 'capacity': 10, 'Concentration': 0.2295}),
    ('18', '19', {'weight': 10, 'capacity': 10, 'Concentration': 0}), ('18', '21', {'weight': 44, 'capacity': 10, 'Concentration': 0}),
    ('19', '20', {'weight': 21, 'capacity': 10, 'Concentration': 0}), ('19', '23', {'weight': 34, 'capacity': 10, 'Concentration': 0}),
    ('20', '22', {'weight': 29, 'capacity': 10, 'Concentration': 0}),
    ('21', '22', {'weight': 18, 'capacity': 10, 'Concentration': 0}),
    ('22', '24', {'weight': 18, 'capacity': 10, 'Concentration': 0}),
    ('23', '24', {'weight': 44, 'capacity': 10, 'Concentration': 0}),
    ('24', '49', {'weight': 54, 'capacity': 10, 'Concentration': 0}),
    ('25', '29', {'weight': 22, 'capacity': 10, 'Concentration': 0}),
    ('26', '40', {'weight': 36, 'capacity': 10, 'Concentration': 0}), ('26', '41', {'weight': 42, 'capacity': 10, 'Concentration': 0}),
    ('27', '43', {'weight': 30, 'capacity': 10, 'Concentration': 0}), ('27', '44', {'weight': 39, 'capacity': 10, 'Concentration': 0}),
    ('28', '45', {'weight': 33, 'capacity': 10, 'Concentration': 0}),
    ('29', '30', {'weight': 14, 'capacity': 10, 'Concentration': 0}),
    ('30', '31', {'weight': 12, 'capacity': 10, 'Concentration': 0}),
    ('31', '32', {'weight': 24, 'capacity': 10, 'Concentration': 0}), ('31', '46', {'weight': 30, 'capacity': 10, 'Concentration': 0}),
    ('32', '47', {'weight': 32, 'capacity': 10, 'Concentration': 0}),
    ('33', '47', {'weight': 43, 'capacity': 10, 'Concentration': 0}), ('33', '48', {'weight': 39, 'capacity': 10, 'Concentration': 0}),
    ('34', '35', {'weight': 42, 'capacity': 10, 'Concentration': 4.9275}), ('34', '50', {'weight': 31, 'capacity': 10, 'Concentration': 2.1351}),
    ('35', '36', {'weight': 21, 'capacity': 10, 'Concentration': 4.9275}),
    ('36', '37', {'weight': 16, 'capacity': 10, 'Concentration': 2.1351}),
    ('37', '38', {'weight': 26, 'capacity': 10, 'Concentration': 0.7789}),
    ('38', '39', {'weight': 37, 'capacity': 10, 'Concentration': 0.2295}),
    ('39', '40', {'weight': 10, 'capacity': 10, 'Concentration': 0}),
    ('40', '41', {'weight': 36, 'capacity': 10, 'Concentration': 0}),
    ('41', '42', {'weight': 13, 'capacity': 10, 'Concentration': 0}),
    ('42', '43', {'weight': 28, 'capacity': 10, 'Concentration': 0}),
    ('43', '44', {'weight': 26, 'capacity': 10, 'Concentration': 0}),
    ('44', '45', {'weight': 7, 'capacity': 10, 'Concentration': 0}),
    ('45', '51', {'weight': 35, 'capacity': 10, 'Concentration': 0}),
    ('46', '47', {'weight': 12, 'capacity': 10, 'Concentration': 0}), ('46', '51', {'weight': 20, 'capacity': 10, 'Concentration': 0}),
    ('47', '48', {'weight': 45, 'capacity': 10, 'Concentration': 0}),
    ('48', '49', {'weight': 18, 'capacity': 10, 'Concentration': 0}),
    ('45', '51', {'weight': 35, 'capacity': 10, 'Concentration': 0}),

]

G.add_edges_from(edges)

# 设置疏散原点、目的地和安全时限
S = ['A1', 'B1', 'E1', 'C1', 'D1']
D = ['39', '10', '11', '12', 'J1']

Ts = 200  # 当时限小于200时才会被归类为是一个安全路线，被计入有效路径以及输出

for t_1 in range(0, 3):
    evacuate(G, S, D, Ts)

    # 执行 Adust 算法
    adjusted_data = adjust()

    # 输出结果



