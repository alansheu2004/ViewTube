import xgboost as xgb
import numpy as np
import pandas as pd
import request

from flask import Flask

app = Flask(__name__)
model_xgb_2 = xgb.Booster()

@app.before_first_request
def my_func():
    model_xgb_2.load_model("xgb.json")

@app.route('/', methods = ['GET'])
def request():
    return '<p>Wow</p>'

if __name__ == '__main__':
    app.run(debug=True)