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
#     summary = generate_summary(transcript,8)
#     summarized_text1 = []
#     summarized_text1.append(summary)
    return render_template('about.html', data= transcript)
  
if __name__ == "__main__":
	app.debug = True
	app.run()
