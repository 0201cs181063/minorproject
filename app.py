from flask import Flask, render_template, request
import numpy as np
import json
import joblib,os
import urllib
import urllib.request
import youtube_transcript_api
import jinja2
import requests
from googletrans import Translator

from pprint import pprint
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig
import pickle

# test=joblib.load(('file.pkl'));

# import gzip, pickle
# with open('file.pkl', 'rb') as ifp:
#     test=(pickle.load(ifp))
#     test.close()
# test = pickle.load(open('file.pkl', 'rb'))
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

    m=transL.translate(text1, dest=v)
    r=[]
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
#     summarized_text1 = []
#     num_iters = int(len(result)/3000)
#     summarized_text = []
#     summarized_text1 = []
#     trial_sum=""
#     for i in range(0, num_iters + 1):
#         start = 0
#         start = i * 3000
#         end = (i + 1) * 3000
#         out = test(result[start:end],max_length=50)
# #         test.close()
#         out = out[0]
#         out = out['summary_text']
#         summarized_text.append(out)
#         trial_sum = trial_sum + out
#     global h
#     h=result
#     summarized_text1.append(result)
    summarized_text1 = []
    url = "https://meaningcloud-summarization-v1.p.rapidapi.com/summarization-1.0"
#     querystring = {"sentences":result,"url":"http://en.wikipedia.org/wiki/Star_Trek"}

    headers = {
        'accept': "application/json",
        'x-rapidapi-key': "3345d8c834msh75cec25088f47c7p140295jsndc688f6ab9e8",
        'x-rapidapi-host': "meaningcloud-summarization-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=result)
    summarized_text1.append(response)
#     url = "https://textanalysis-text-summarization.p.rapidapi.com/text-summarizer-text"

#     payload = "text=Automatic%20summarization%20is%20the%20process%20of%20reducing%20a%20text%20document%20with%20a%20computer%20program%20in%20order%20to%20create%20a%20summary%20that%20retains%20the%20most%20important%20points%20of%20the%20original%20document.%20As%20the%20problem%20of%20information%20overload%20has%20grown%2C%20and%20as%20the%20quantity%20of%20data%20has%20increased%2C%20so%20has%20interest%20in%20automatic%20summarization.%20Technologies%20that%20can%20make%20a%20coherent%20summary%20take%20into%20account%20variables%20such%20as%20length%2C%20writing%20style%20and%20syntax.%20An%20example%20of%20the%20use%20of%20summarization%20technology%20is%20search%20engines%20such%20as%20Google.%20Document%20summarization%20is%20another.&sentnum=5"
#     headers = {
#         'content-type': "application/x-www-form-urlencoded",
#         'x-rapidapi-key': "3345d8c834msh75cec25088f47c7p140295jsndc688f6ab9e8",
#         'x-rapidapi-host': "textanalysis-text-summarization.p.rapidapi.com"
#         }
#     summarized_text1 = []
#     response = requests.request("POST", url, data=payload, headers=headers)
#     summarized_text1.append(response)
    return render_template('about.html', data= summarized_text1)
    



if __name__ == "__main__":
    app.run(debug=True)


