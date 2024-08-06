import os
import json
import random
import numpy as np
import pandas as pd
import tflearn
from nltk.stem.lancaster import LancasterStemmer
import nltk    # NATURAL LANGUAGE TOOLKIT
nltk.download("punkt")  # REQUIRED IF NOT DONE PREVIOUSLY
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# SETS DEFAULT LISTS FOR THE DATA IN DATA.JSON

words = []              # A collection of all words in 'patterns'
documents = []          # a collection of all
classes = []            # a collection of the 'tags' in data.json
training_data = []      # a collection of data used for training (used later)

with open('data.json') as json_data:
    data = json.load(json_data)


# INITIALIZES THE DEFAULT LISTS WITH VALUES NEEDED TO SORT DATA
def initialize_collections(data):
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            word = nltk.word_tokenize(pattern)
            words.extend(word)
            documents.append((word, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

initialize_collections(data)

# INITIALIZES THE STEMMER THAT WILL BE USED THE PROVIDE STEMS OF EACH WORD IN WORDS
stemmer = LancasterStemmer()

# CREATES A LIST OF STEMS FROM THE WORDS IN 'WORDS'
words_lowercase = [stemmer.stem(word.lower()) for word in words]

# REPLACES 'WORDS' LIST WITH A SORTED LIST OF "STEMMED" WORDS IN THE WORDS LIST
words = sorted(list(set(words_lowercase)))

# CREATES A LIST OF DATA THE LENGTH OF 'CLASSES' FILLED WITH ZEROS (OFF)
empty_output = [0] * len(classes)

def train_data(documents):
    for doc in documents:
        bag_of_words = []
        pattern_words = doc[0]  # index 0 is the pattern words, index 1 is the tag associated

        # takes the stem of the words in pattern words, and makes them lowercase
        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

        for word in words:
            # appends a 0 or 1 (yes or no) to bag_of_words which corresponds with the index of each word
            # this will indicate if a word stem is present and associated with a tag
            bag_of_words.append(1) if word in pattern_words else bag_of_words.append(0)

        output_row = list(empty_output)
        output_row[classes.index(doc[1])] = 1  # Toggles a 0 to a 1 based on the index what tag is being examined

        # creates an associative relationship between the words in the list, and the tag using the above statements
        # to represent all data exclusively using binary 1's and 0's
        training_data.append([bag_of_words, output_row])

train_data(documents)

random.shuffle(training_data)  # shuffles data for increased efficiency

training_series = pd.Series(training_data)

train_X = list(training_series.apply((lambda x: x[0])))  # Creates a list of rows
train_Y = list(training_series.apply((lambda x: x[1])))  # Creates a list of columns

neural_network = tflearn.input_data(shape=[None, len(train_X[0])])

neural_network = tflearn.fully_connected(neural_network, 8)
neural_network = tflearn.fully_connected(neural_network, 8)
neural_network = tflearn.fully_connected(neural_network, len(train_Y[0]), activation='softmax')
neural_network = tflearn.regression(neural_network)


model = tflearn.DNN(neural_network)

# THESE 2 LINES CAN BE COMMENTED OUT AFTER SAVING THE CHATBOT. CHECK DIRECTORY FOR chatbot_dnn.tflearn FILES
# model.fit(train_X, train_Y, n_epoch=24000, batch_size=16, show_metric=True)
# model.save("chatbot_dnn.tflearn")

model.load("chatbot_dnn.tflearn")

def process_question(question):
    # creates tokens for each word in the question
    question_tokenized = nltk.word_tokenize(question)

    # creates word stem for each token and converts to lowercase
    question_stemmed = [stemmer.stem(word.lower()) for word in question_tokenized]

    # makes a word bag the size of words and initializes all values to zero
    bag = [0] * len(words)

    for stem in question_stemmed:
        for index, word in enumerate(words):
            if word == stem:
                # if a word == a stem, changes the bag value at the stems location to 1
                bag[index] = 1

    return np.array(bag)

question = "do I need to enter my home address?"
# print(process_question(question))
prediction = model.predict([process_question(question)])
# print(prediction)

def categorize(prediction):
    prediction_top = [[index, result] for index, result in enumerate(prediction) if result > 0.59]
    prediction_top.sort(key=lambda x: x[1], reverse=True)

    result = []

    if not prediction_top:
        result.append(["not_sure"])

    for predict in prediction_top:
        result.append((classes[predict[0]], predict[1]))
    return result


question = "hello"
predict = model.predict([process_question(question)])


def ask_chatbot(question):
    if question == "":
        return

    prediction = model.predict([process_question(question)])
    result = categorize(prediction[0])

    for intent in data["intents"]:
        if intent["tag"] == result[0][0]:
            response = random.choice(intent['responses'])
            return[response, result[0][0]]
