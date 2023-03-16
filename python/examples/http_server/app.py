import random as r
from flask import Flask, request
import sys
import otcic
import multiprocessing

ROW_LENGTH = 2**16
CHUNK_SIZE = 2**4

Row = list[int]
Table = list[Row]

app = Flask(__name__)

table: Table = []
filename = "table.txt"
with open(filename, "w") as file:
    file.write("Table\n")


def expensive_function(_=None) -> float:
    return (r.random() * r.randint(1, 3)) / (r.random() + 1)

def table_sizeof(table: Table) -> int:
    return sys.getsizeof(table) + sum(map(sys.getsizeof, table))


@otcic.ram_trace
def make_row() -> Row:
    #return list(map(expensive_function, range(ROW_LENGTH)))
    with multiprocessing.Pool() as pool:
        return pool.map(expensive_function, range(ROW_LENGTH), CHUNK_SIZE)


@otcic.ram_trace
def do_roll():
    print("Table size:", table_sizeof(table))
    if len(table) < 16:
        row = make_row()
        with open(filename, "a") as file:
            file.write(", ".join(["{}\n".format(item) for item in row]))
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


@app.route("/")
@otcic.ram_trace
def roll_dice():
    s = do_roll()
    print(s)
    return s


otcic.setup("flask-server")
