from random import randint
from flask import Flask, request
import sys
import os
# sys.path.append('..')
import otcic
# from ...python import otcic as otcic

app = Flask(__name__)

@app.route("/rolldice")
@otcic.all_trace
def roll_dice():
    return str(do_roll())

def do_roll():
    return randint(1, 6)

otcic.setup()