import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# Libraries needed for Tensorflow processing
import tensorflow as tf
import numpy as np
import tflearn
import random
import json
import time

# import our chat-bot intents file
with open('deneme.json') as json_data:
    intents = json.load(json_data)

intents

words = []
classes = []
documents = []
ignore = ['?']
# loop through each sentence in the intent's patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each and every word in the sentence
        w = nltk.word_tokenize(pattern)
        # add word to the words list
        words.extend(w)
        # add word(s) to documents
        documents.append((w, intent['tag']))
        # add tags to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Perform stemming and lower each word as well as remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore]
words = sorted(list(set(words)))

# remove duplicate classes
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)

# create training data
training = []
output = []
# create an empty array for output
output_empty = [0] * len(classes)

# create training set, bag of words for each sentence
for doc in documents:
    # initialize bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stemming each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is '1' for current tag and '0' for rest of other tags
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffling features and turning it into np.array
random.shuffle(training)
training = np.array(training)

# creating training lists
train_x = list(training[:,0])
train_y = list(training[:,1])

# resetting underlying graph data
tf.reset_default_graph()

# Building neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Defining model and setting up tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

# Start training
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')

import pickle
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )

# restoring all the data structures
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

with open('deneme.json') as json_data:
    intents = json.load(json_data)

# load the saved model
model.load('./model.tflearn')

def clean_up_sentence(sentence):
    # tokenizing the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stemming each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# returning bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenizing the pattern
    sentence_words = clean_up_sentence(sentence)
    # generating bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

ERROR_THRESHOLD = 0.30
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # a random response from the intent
                    return (random.choice(i['responses'])) #returnden sonra print koy

            results.pop(0)
           

"""classify('What are you hours of operation?')

response('What are you hours of operation?')

response('What is menu for today?')

#Some of other context free responses.
response('Do you accept Credit Card?')

response('Where can we locate you?')

response('That is helpful')

response('Bye')"""
"""
response("merhaba bot")
response("gorusuruz")
response("tesekkurler")
response("bakiyem")
response("are u open today")"""
#Adding some context to the conversation i.e. Contexualization for altering question and intents etc.
# create a data structure to hold user context
"""context = {}

ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        return print(random.choice(i['responses']))

            results.pop(0)
    else:
      return print("Sorry, I didn't understand")        

response('Can you please let me know the delivery options?')

response('What is menu for today?')

context

response("Hi there!", show_details=True)

response('What is menu for today?')"""

from selenium import webdriver

chrome_browser = webdriver.Chrome(executable_path='C:/Users/Yetkin/Downloads/chromedriver_win32/chromedriver')
chrome_browser.get('https://web.whatsapp.com')

time.sleep(15)
user_name = 'Refresh'
for_refresh = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
"""mssge = chrome_browser.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div[21]/div/div/div/div[1]/div/span[1]/span')
print(mssge.text)"""
while True:
    if(chrome_browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/*/div/div/div[2]/div[2]/div[2]')):  
        try:
            user_to_send = chrome_browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/*/div/div/div[2]/div[2]/div[2]')
            user_to_send.click()
            time.sleep(10)

            mssge = chrome_browser.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/*/*/div/div/div/div[1]/div/span[1]/span')
            mssge = mssge.text
            mssge = response(mssge)
            time.sleep(10)

            message_box = chrome_browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            message_box.send_keys(mssge)
            time.sleep(10)

            send_button = chrome_browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
            send_button.click()
            time.sleep(1)

            for_refresh.click()
        except:
            pass    
    else:
        pass

#//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[2]/div[2]/span[1]/div/span (gelen mesaj)
#//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/span/span