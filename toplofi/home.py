from toplofi import app
from toplofi.pamfinder import *
from flask import render_template
from flask import request, redirect


@app.route("/")
def home():
    streams = "Hello World"
    return render_template("home.html")

@app.route("/bp", methods = ['GET'])
def form():
    if(len(request.args) > 0):
        base_pair = request.args['basepair']
    else:
        base_pair = "-1"

    if base_pair.isdecimal():
        base_pair = int(base_pair)
    else:
        base_pair = -1
    if base_pair < 70000 or base_pair >130000000:
        base_pair = -1
    if base_pair == -1:
        info = -1
    else:
        info = get_crispr_info(base_pair)
    return render_template("home.html", info=info, base_pair=base_pair)

