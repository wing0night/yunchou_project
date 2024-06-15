def adjust(data):
    """
    实现 Adust 算法

    Args:
        data: 一个列表, 每个元素是一个字典, 包含 'rfk', 'Tfk_v_road', 'Mf', 'Bk' 四个键值对

    Returns:
        一个列表, 包含经过 Adust 算法处理后的字典
    """

    # Step 1: 按 Tfk_v_road 由小到大排序
    data.sort(key=lambda item: item['Tfk_v_road'])

    # Step 2 & 3: 循环处理每个字典
    i = 0
    while i < len(data):
        f1 = data[i]['rfk'][0]  # 获取人群节点
        k1 = data[i]['rfk'][1]  # 获取出口节点
        Mf1 = data[i]['Mf']  # 获取人群节点人数
        Bk1 = data[i]['Bk']  # 获取出口节点理论疏散人数

        # Step 2: 人群节点人数小于出口理论疏散人数
        if Mf1 < Bk1:
            # 删除人群节点为 f1 的所有字典
            data = [item for item in data if item['rfk'][0] != f1]

            # 更新出口节点 k1 剩余疏散人数
            for item in data:
                if item['rfk'][1] == k1:
                    item['Bk'] = Bk1 - Mf1
                    break

            # 重复 Step 1
            data.sort(key=lambda item: item['Tfk_v_road'])
            i = 0  # 从头开始重新遍历

        # Step 3: 人群节点人数大于出口理论疏散人数
        else:
            # 删除出口节点为 k1 的所有字典
            data = [item for item in data if item['rfk'][1] != k1]

            # 更新人群节点 f1 剩余人数
            for item in data:
                if item['rfk'][0] == f1:
                    item['Mf'] = Mf1 - Bk1
                    break

            # 重复 Step 1
            data.sort(key=lambda item: item['Tfk_v_road'])
            i = 0  # 从头开始重新遍历

        i += 1  # 移动到下一个字典

    return data

# 示例数据
data = [
    {'rfk': ('f1', 'k1'), 'Tfk_v_road': 10, 'Mf': 50, 'Bk': 100},
    {'rfk': ('f2', 'k2'), 'Tfk_v_road': 20, 'Mf': 80, 'Bk': 60},
    {'rfk': ('f3', 'k1'), 'Tfk_v_road': 30, 'Mf': 30, 'Bk': 50},
    {'rfk': ('f4', 'k2'), 'Tfk_v_road': 40, 'Mf': 20, 'Bk': 40},
]

# 执行 Adust 算法
adjusted_data = adjust(data.copy())

# 输出结果
print("Adjusted Data:")
for item in adjusted_data:
    print(item)
