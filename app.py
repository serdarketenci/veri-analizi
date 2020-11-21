from flask import Flask, render_template, request
import tensorflow as tf
import pickle
from keras.models import load_model
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.backend import clear_session
import pandas as pd
import urllib.request  as urllib2
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

clear_session()

app = Flask(__name__)

# load the Model from file
nlp_model = load_model('lstm_nlp1.h5')

global graph
graph = tf.get_default_graph()

# load tokenizer
with open('turkish_tokenizer.pickle', 'rb') as handle:
    turkish_tokenizer = pickle.load(handle)

def predict(texts):
	tokens = turkish_tokenizer.texts_to_sequences(texts)
	tokens_pad = pad_sequences(tokens, maxlen=59)
	with graph.as_default():
		prediction = nlp_model.predict(tokens_pad)[0][0]
	return prediction

def getCommentsFromUrl(url):

	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
	html = opener.open(url + '/yorumlar').read()
	soup = BeautifulSoup(html)
	elements = soup.findAll("div", {"class": "rnr-com-tx"})
	comments = []
	for element in elements:
		comments.append(element.get_text())
	return comments

def cal_average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t

    avg = sum_num / len(num)
    return avg

@app.route('/', methods=['GET', 'POST'])
def home():
	in_text = request.values.get('text_input')
	arr = [in_text]
	# if input is provided process else show default page
	if request.method == 'POST':
		_comments = getCommentsFromUrl(in_text)
		sum = []
		comments = []
		for comment in _comments:
			prec = predict(comment)
			sum.append(prec)
			comments.append({
				'Comment': comment,
				'Prediction':prec
			})

		result = cal_average(sum)

		return render_template('home.html', result=result, comments=comments, text=in_text)
	else:
		return render_template('home.html')


if __name__ == '__main__':
	app.run(debug=False)