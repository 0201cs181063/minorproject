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
from nltk.corpus import stopwords
import numpy as np
import networkx as nx
import regex
from flask import Flask, request, jsonify, render_template
import nltk

from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig
# import pickle

# test=joblib.load(('file.pkl'));

# import gzip, pickle
# with open('file.pkl', 'rb') as ifp:
#     test=(pickle.load(ifp))
#     test.close()
# test = pickle.load(open('file.pkl', 'rb'))
# with gzip.open('file.pkl', 'rb') as ifp:
#     test=(pickle.load(ifp))

def read_article(data):

    article = data.split(". ")
    sentences = []
    for sentence in article:
        review = regex.sub("[^A-Za-z0-9]",' ', sentence)
        sentences.append(review.replace("[^a-zA-Z]", " ").split(" "))        
    sentences.pop()     
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words) #makes a vector of len all_words
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - nltk.cluster.util.cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)
    
    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
#     print("\n\n---------------\nIndexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize texr
    # print("\n")
    # print("*"*140)
    # print("\n\nSUMMARY: \n---------\n\n", ". ".join(summarize_text))
    a = ". ".join(summarize_text)
    return a

#----------FLASK-----------------------------#

# app = Flask(__name__)
# @app.route('/templates', methods =['POST'])
# def original_text_form():
# 		text = request.form['input_text']
# 		number_of_sent = request.form['num_sentences']
# # 		print("TEXT:\n",text)
# 		summary = generate_summary(text,int(number_of_sent))
# # 		print("*"*30)
# # 		print(summary)
# 		return render_template('index1.html', title = "Summarizer", original_text = text, output_summary = summary, num_sentences = 5)

# @app.route('/')
# def homepage():
# 	title = "TEXT summarizer"
# 	return render_template('index1.html', title = title)

# if __name__ == "__main__":
# 	app.debug = True
# 	app.run()
# app = Flask(__name__)

# @app.route('/')
# def man():
#     return render_template('index.html')

#@app.route('/', methods=['POST'])
#def man():
 #
 #    return render_template('about.html')
app = Flask(__name__)

@app.route('/')
def man():
    return render_template('home.html')
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
    summarized_text1 = []
#     pprint(summarize(result, word_count=20))
#    
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
#     summarized_text1 = []
#     url = "https://textanalysis-text-summarization.p.rapidapi.com/text-summarizer"
#     payload = {
# #       \"url\": \"http://en.wikipedia.org/wiki/Automatic_summarization\",
#       "text": result,
#       "sentnum": 8
#     }
#     headers = {
#         'content-type': "application/json",
#         'x-rapidapi-key': "3345d8c834msh75cec25088f47c7p140295jsndc688f6ab9e8",
#         'x-rapidapi-host': "textanalysis-text-summarization.p.rapidapi.com"
#         }
    summary = generate_summary( transcript,int(6))
    summarized_text1.append(summary)
#     response = requests.request("POST", data=summarized_text1)

#     response = requests.request("POST", url, data=payload, headers=headers)














#     url = "https://aylien-text.p.rapidapi.com/summarize"

#     headers = {
#         'x-rapidapi-key': "3345d8c834msh75cec25088f47c7p140295jsndc688f6ab9e8",
#         'x-rapidapi-host': "aylien-text.p.rapidapi.com"
#         }
#     response = requests.request("GET", url, headers=headers, params=result)
#     summarized_text1.append(response)
#     url = "https://textanalysis-text-summarization.p.rapidapi.com/text-summarizer-text"

#     payload = "text=Automatic%20summarization%20is%20the%20process%20of%20reducing%20a%20text%20document%20with%20a%20computer%20program%20in%20order%20to%20create%20a%20summary%20that%20retains%20the%20most%20important%20points%20of%20the%20original%20document.%20As%20the%20problem%20of%20information%20overload%20has%20grown%2C%20and%20as%20the%20quantity%20of%20data%20has%20increased%2C%20so%20has%20interest%20in%20automatic%20summarization.%20Technologies%20that%20can%20make%20a%20coherent%20summary%20take%20into%20account%20variables%20such%20as%20length%2C%20writing%20style%20and%20syntax.%20An%20example%20of%20the%20use%20of%20summarization%20technology%20is%20search%20engines%20such%20as%20Google.%20Document%20summarization%20is%20another.&sentnum=5"
#     headers = {
#         'content-type': "application/x-www-form-urlencoded",
#         'x-rapidapi-key': "3345d8c834msh75cec25088f47c7p140295jsndc688f6ab9e8",
#         'x-rapidapi-host': "textanalysis-text-summarization.p.rapidapi.com"
#         }
#     summarized_text1 = []
#     response = requests.request("POST", url, data=payload, headers=headers)
#     summarized_text1.append(response.text)
    return render_template('about.html', data= summarized_text1)
    



if __name__ == "__main__":
    app.run(debug=True)


