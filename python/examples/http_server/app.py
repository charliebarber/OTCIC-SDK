import random as r
from flask import Flask, request
import sys
import otcic

app = Flask(__name__)

table: list[list[int]] = []
filename = "table.txt"
with open(filename, "w") as file:
    file.write("Table\n")


def expensive_function():
    return (r.random() ** r.randint(1, 3)) / (r.random() + 1)


def table_sizeof(table: list[list[int]]):
    return sys.getsizeof(table) + sum(map(sys.getsizeof, table))


@otcic.ram_trace
def make_row():
    row = []
    for i in range(2**16):
        v = expensive_function()
        if v > 0:
            v = v ** 0.5
        row.append(v)
    return row


@otcic.ram_trace
def do_roll():
    print("Table size:", table_sizeof(table))
    if len(table) < 16:
        row = make_row()
        with open(filename, "a") as file:
            file.write("{}\n".format(row[0]))
        table.append(row)
        msg = "Table ADD: {}".format(row[0])

    else:
        d = r.randint(1, 16)
        for _ in range(d):
            table.pop(0)
        msg = "Table DEL: {}".format(d)

    for row in table:
        for n in range(len(row)):
            v = row[n]
            v = (v + expensive_function()) % v

    return msg


@app.route("/rolldice")
@otcic.ram_trace
def roll_dice():
    s = do_roll()
    print(s)
    return s


otcic.setup("flask-server", "example python cpu")
