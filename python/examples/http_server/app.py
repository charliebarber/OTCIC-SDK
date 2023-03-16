import random as r
from flask import Flask, request
from functools import wraps
import sys
import otcic
import multiprocessing

TABLE_MAX = 16
ROW_LENGTH = 2**16
CHUNK_SIZE = 2**4

Row = list[int]
Table = list[Row]

app = Flask(__name__)

table: Table = []
filename = "table.txt"

with open(filename, "w"): pass

def overwrite_table():
    with open(filename, "w") as file:
        lines = ["Table"]
        lines.extend([",".join([str(n) for n in row]) for row in table])
        file.write("\n".join(lines))

def expensive_function(_=None) -> float:
    return (r.random() * r.randint(1, 3)) / (r.random() + 1)

def table_sizeof(table: Table) -> int:
    return sys.getsizeof(table) + sum(map(sys.getsizeof, table))

def print_table():
    print("Table size:", table_sizeof(table))


@otcic.ram_trace
def make_row() -> Row:
    return list(map(expensive_function, range(ROW_LENGTH)))
    # with multiprocessing.Pool() as pool:
    #     return pool.map(expensive_function, range(ROW_LENGTH), CHUNK_SIZE)


def table_template(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print_table()
        msg = func(*args, **kwargs)
        overwrite_table()
        print(msg)
        return msg
    return wrapper


@app.route("/add")
@otcic.ram_trace
@table_template
def add_table() -> str:
    if len(table) < TABLE_MAX:
        row = make_row()
        table.append(row)
        return "Table ADD: {}".format(row[0])
    return "Table ADD: Max Limit Reached"

@app.route("/del")
@otcic.ram_trace
@table_template
def del_table() -> str:
    if len(table) > 0:
        d = r.randint(0, len(table) - 1)
        table.pop(d)
        return "Table DEL: {}".format(d)
    return "Table DEL: Empty"

@app.route("/mod")
@otcic.ram_trace
@table_template
def table_mod() -> str:
    if len(table) > 0:
        for row in table:
            for n in range(len(row)):
                row[n] = (row[n] + expensive_function()) % 16
        return "Table MOD: {}".format(row[0])
    return "Table MOD: Empty"


otcic.setup("flask-server")
