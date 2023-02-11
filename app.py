import re
import unicodedata
import string
import random
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.probability import ConditionalFreqDist

from flask import Flask, request, jsonify
import sys, os
from flask import Flask
app = Flask(__name__)# URL Routing — Home Page


def filter(text):
    # normalize text
    text = (unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore'))
    # replace html chars with ' '
    text = re.sub('<.*?>', ' ', text)
    # remove punctuation
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    # only alphabets and numerics
    text = re.sub('[^a-zA-Z]', ' ', text)
    # replace newline with space
    text = re.sub("\n", " ", text)
    # lower case
    text = text.lower()
    # split and join the words
    text = ' '.join(text.split())
    return text

def clean(text):
    tokens = nltk.word_tokenize(text)
    wnl = nltk.stem.WordNetLemmatizer()

    output = []
    for words in tokens:
        # lemmatize words
        output.append(wnl.lemmatize(words))

    return output

def n_gram_model(text):
    trigrams = list(nltk.ngrams(text, 3, pad_left=True, pad_right=True,
                    left_pad_symbol='<s>', right_pad_symbol='</s>'))

    # make conditional frequencies dictionary
    cfdist = ConditionalFreqDist()
    for w1, w2, w3 in trigrams:
        cfdist[(w1, w2)][w3] += 1

    # transform frequencies to probabilities
    for w1_w2 in cfdist:
        total_count = float(sum(cfdist[w1_w2].values()))
        for w3 in cfdist[w1_w2]:
            cfdist[w1_w2][w3] /= total_count

    return cfdist


def predict(model, user_input):
    user_input = filter(user_input)
    user_input = user_input.split()
    # import pdb;pdb.set_trace()

    w1 = len(user_input) - 2
    w2 = len(user_input)
    prev_words = user_input[w1:w2]

    # display prediction from highest to lowest maximum likelihood
    prediction = sorted(dict(model[prev_words[0], prev_words[1]]), key=lambda x: dict(
        model[prev_words[0], prev_words[1]])[x], reverse=True)
    print("Trigram model predictions: ", prediction)

    word = []
    weight = []
    for key, prob in dict(model[prev_words[0], prev_words[1]]).items():
        word.append(key)
        weight.append(prob)
    # pick from a weighted random probability of predictions
    next_word = random.choices(word, weights=weight, k=1)
    # add predicted word to user input
    user_input.append(next_word[0])
    return ' '.join(user_input)

file = open('./report.txt','r')
text = ""
while True:
	line = file.readline()
	text += line
	if not line:
		break
# import pdb;pdb.set_trace()
# pre-process text
print("Filtering...")
words = filter(text)
print("Cleaning...")
words = clean(words)
# make language model
print("Making model...")
model = n_gram_model(words)


# Create a route to our index page at the root url, return a simple greeting
@app.route("/",methods=["GET"])
def indexPage():
	return open("index.html","r").read()

@app.route("/word/",methods=["POST"])
def wordSearch():
	data = request.json
	results = []
	result = predict(model, data['search_text'])
	if True:
		for x in range(7):
			results.append(result)
			result = predict(model, result)
	else:
		results.append(result)
	return jsonify(results)

# Main Function, Runs at http://0.0.0.0:8000
if __name__ == "__main__":
    app.run(port=3000, debug=True)

