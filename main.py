import xgboost as xgb
import numpy as np
import pandas as pd
import re
import os
import json
import numpy.random as random
from gensim.models import FastText
from img2vec_pytorch import Img2Vec
from PIL import Image

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ft_titles = FastText.load("./model/ft_titles.bin")
ft_tags = FastText.load("./model/ft_tags.bin")
img2vec = Img2Vec()
xgb_reg = xgb.Booster()
xgb_reg.load_model("./model/xgb.json")

intervals = 100

with open('./model/adtl_data.json', 'r') as openfile:
    json_object = json.load(openfile)
    mean_log_views = json_object["mean_log_views"]
    std_log_views = json_object["std_log_views"]

@app.route('/home')
def home():
    return 'Welcome'

def process_title(title):
    title = str(title)
    # title = re.sub(r"&.*?;", " ", title)
    title = re.sub(r"[!\"#\＄%&\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~]", " ", title)
    title = title.lower()
    title = title.split(" ")
    title = list(filter(None, title))
    return title

def process_tags(tags):
    if(tags == None or tags == ""):
        return []
    tags = str(tags)
    tags = tags.lower()
    tags = re.sub(r"[!\"#\＄%&\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~]", " ", tags)
    tags = tags.split(",")
    tags = [tag.strip() for tag in tags]
    tags = list(filter(None, tags))
    return tags

def convertToVec(ft, wordlist):
    if (len(wordlist) == 0):
        return np.zeros(ft.vector_size)
    else:
        return np.mean([ft.wv[word] for word in wordlist], axis=0)

@app.route('/')
def home_page():
    return "Hello Friendly User!"

@app.route('/get-data', methods = ['POST'])
def get_data():
    if request.method == 'POST':
        time = int(request.form.get('timeTotal'))

        df = pd.DataFrame()
        df['timeElapsed'] = np.linspace(0, time, intervals)
        df = pd.concat([df, pd.DataFrame( np.repeat(int(request.form.get('category' )), intervals, axis=0), index=df.index, columns=["categoryId"])]     , axis=1)
        df = pd.concat([df, pd.DataFrame( np.repeat(int(request.form.get('avgViews' )), intervals, axis=0), index=df.index, columns=["avgViewsPerVid"])] , axis=1)
        df = pd.concat([df, pd.DataFrame( np.repeat(int(request.form.get('subs'     )), intervals, axis=0), index=df.index, columns=["subscriberCount"])], axis=1)
        df = pd.concat([df, pd.DataFrame( np.repeat(int(request.form.get('numVideos')), intervals, axis=0), index=df.index, columns=["videoCount"])]     , axis=1)
        df['categoryId'].astype("category")

        title_vectors = convertToVec(ft_titles, process_title(request.form.get('title')))
        title_vectors = np.repeat([title_vectors], intervals, axis=0)
        title_vec_cols = ["titleVec" + str(num) for num in range(300)]
        df = pd.concat([df, pd.DataFrame(title_vectors, index=df.index, columns=title_vec_cols)], axis=1)

        tags_vectors = convertToVec(ft_tags, process_tags(request.form.get('tags')))
        tags_vectors = np.repeat([tags_vectors], intervals, axis=0)
        tags_vec_cols = ["tagsVec" + str(num) for num in range(300)]
        df = pd.concat([df, pd.DataFrame(tags_vectors, index=df.index, columns=tags_vec_cols)], axis=1)
        df["tagCount"] = len(process_tags(request.form.get('tags')))

        img = Image.open(request.files['thumbnail'].stream).convert('RGB')
        thumbnail_vectors = np.array(img2vec.get_vec(img))
        thumbnail_vectors = np.repeat([thumbnail_vectors], intervals, axis=0)
        vector_size_thumbnail = len(thumbnail_vectors[0])
        thumbnail_vec_cols = ["thumbnailVec" + str(num) for num in range(vector_size_thumbnail)]
        df = pd.concat([df, pd.DataFrame(thumbnail_vectors, columns=thumbnail_vec_cols)], axis=1)

        x_labels = ["categoryId", "tagCount", "avgViewsPerVid", "subscriberCount", "videoCount", "timeElapsed"] + title_vec_cols + tags_vec_cols + thumbnail_vec_cols
        x = df.loc[:, x_labels]

        dmatrix = xgb.DMatrix(data=x, enable_categorical=True)
        pred = np.maximum.accumulate(np.exp(xgb_reg.predict(dmatrix) * std_log_views + mean_log_views))
        
        return json.dumps(np.transpose([df['timeElapsed'], pred]).tolist())

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))