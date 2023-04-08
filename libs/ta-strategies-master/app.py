import pyximport

pyximport.install(setup_args={"script_args": ["--verbose"]})

import time
from flask import Flask
from flask_cors import CORS, cross_origin

import modules.utils as utils
import definitions

def run_strs():
    import modules.strategies.run as exec
    return exec


# 1h tf
timeframe = 3600

exec = run_strs()
# for sec in range(timeframe , 0 , -1):
#     # run_strs()
#     time.sleep(1)


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
@cross_origin()
def index():
    data = utils.df_to_json(exec.df_final)
    return data


@app.route("/ohlcv")
@cross_origin()
def ohlcv():
    data = utils.df_to_json(exec.df_data)
    return data


@app.route("/exchanges")
@cross_origin()
def exchanges():
    f = open(definitions.PUBLIC_FOLDER + "exchanges.json", "r")
    data = f.readline()
    f.close()
    return data

@app.route("/widgetConf")
@cross_origin()
def widgetConf():
    return exec.defaults.active_config

@app.route("/divergence")
@cross_origin()
def divergence():
    import json
    to_send = {
        "zigzagThreshs":exec.defaults.ZIGZAG_THRESH,
        "data":exec.divergences_data
    }
    to_send = json.dumps(to_send)
    return to_send


@app.route("/strs")
@cross_origin()
def strs():
    import json
    to_send = json.dumps(exec.to_send)
    return to_send