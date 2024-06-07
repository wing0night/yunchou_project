from tabulate import tabulate

s = "Source"
d_choose = "Destination"
path = ["A", "B", "C"]
dist = 10
path_str = ' -> '.join(path)
data = [
    ["", f"Path from {s} to {d_choose}", f"{path_str}", f"Time: {dist}"],
]
t = 1
headers = [f"Round: {t}", "route", "path", "Time"]

table = tabulate(data, headers, tablefmt="fancy_grid")
print(table)