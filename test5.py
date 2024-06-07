
from tabulate import tabulate, Table

s = "Source"
d_choose = "Destination"
path = ["A", "B", "C"]
dist = 10

table = Table()
table.add_row(["", "", "", "Path from", s, "to", d_choose])
table.add_row(["", "", "", "Route", "->".join(path), "Time", dist])

table[0, 0:4].merge()
table[0, 4:8].merge()

headers = ["", "", "", "", "", "", "", ""]

table_str = tabulate(table, headers, tablefmt="fancy_grid")
print(table_str)