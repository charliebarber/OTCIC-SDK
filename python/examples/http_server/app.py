from random import randint
from flask import Flask, request
import sys
import os
import otcic

app = Flask(__name__)

table: list[list[int]] = []

@otcic.ram_trace
def make_row():
    print("Row")
    row = []
    for i in range(2**16):
        v = randint(1, 6)
        row.append(v)
    return row

@otcic.all_trace
def do_roll():
    print(sys.getsizeof(table))
    value = randint(1, 3)
    if value == 3 and len(table) < 17:
        row = make_row()
        table.append(row)
        return "Table ADD: {}".format(row[0])

    else:
        r0 = randint(0, len(table) - 1)
        row = table[r0]

        if len(row) == 0:
            table.pop(r0)
            return "Table POP: row {}".format(r0)

        else:
            r1 = randint(0, len(row) - 1)
            if value == 2:
                v = row.pop(r1)
                return "Table POP: {}".format(v)
        
            else:
                row[r1] += 1
                return "Table MOD: {}".format(row[r1])

@app.route("/rolldice")
@otcic.all_trace
def roll_dice():
    s = do_roll()
    print(s)
    return s

otcic.setup("flask-server")
