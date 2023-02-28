from random import randint
from flask import Flask, request
import sys
import os
import otcic

print(dir(otcic))

app = Flask(__name__)

@app.route("/rolldice")
@otcic.all_trace
def roll_dice():
    return str(do_roll())

def do_roll():
    return randint(1, 6)

otcic.setup("flask-server")