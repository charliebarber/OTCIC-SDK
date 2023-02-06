from random import randint
from flask import Flask, request
import sys
import os
sys.path.append('../python')
from otcic import main

app = Flask(__name__)

main.setup()

@app.route("/rolldice")
def roll_dice():
    return str(do_roll())

def do_roll():
    return randint(1, 6)


