from flask import Flask, render_template, request
import numpy as np
import json
import urllib
import urllib.request
import youtube_transcript_api
import jinja2
from googletrans import Translator

from pprint import pprint
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig
import pickle
# import gzip, pickle

test = pickle.load(open('file.pkl', 'rb'))
# with gzip.open('file.pkl', 'rb') as ifp:
#     test=(pickle.load(ifp))

app = Flask(__name__)

@app.route('/')
def man():
    return render_template('index.html')

#@app.route('/', methods=['POST'])
#def man():
 #
 #    return render_template('about.html')

@app.route('/about')
def man1():
    return render_template('about.html')

h=""

@app.route('/aboutform', methods=['POST'])
def trans():
    transL=Translator()
    lang = request.form['len']
    text1=h
    if lang=='Hindi':
        v='hi'
    if lang=='German':
        v='de'
    if lang=='French':
        v='fr'
    if lang=='English':
        v='en'
    
    print(text1)
    m=transL.translate(text1, dest=v)
    r=[]
    print(m.text)
    r.append(m.text)
    return render_template('about.html', data=r)

@app.route('/about', methods=['POST'])
def home():
    try:
        youtube_video = request.form['a']
        video_id = youtube_video.split("=")[1]
    except Exception as a:
        array1=[]
        array1.append("invalid link or transcript unavailable")
        return render_template('about.html', error=array1)

    try:
        YouTubeTranscriptApi.get_transcript(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        array=[]
        array.append("invalid link or transcript unavailable")
        return render_template('about.html', error=array)



    result = ""
    for i in transcript:
        result += ' ' + i['text']

    num_iters = int(len(result)/3000)
    summarized_text = []
    summarized_text1 = []
    trial_sum=""
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 3000
        end = (i + 1) * 3000
        out = test(result[start:end],max_length=50)
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)
        trial_sum = trial_sum + out
    global h
    h=trial_sum
    summarized_text1.append(trial_sum)
    
    return render_template('about.html', data=summarized_text1)
    



if __name__ == "__main__":
    app.run(host="0.0.0.0")


