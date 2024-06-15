
'''string = "D1 -> 8 -> 7 -> 5 -> 14 -> 13 -> 12"

# 使用正则表达式提取箭头和空格以外的部分
import re
result = re.findall(r'\w+', string)

# 打印结果
print(result)  # 输出：['D1', '8', '7', '5', '14', '13', '12']'''

result = ['D1', '8', '7', '5', '14', '13', '12']
print(type(result[0]))
