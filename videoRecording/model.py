from spellchecker import SpellChecker
from autocorrect import Speller
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
model = load_model('modelFYP1.29.05.h5')
spell = SpellChecker()

def check(sentence):
    spell=SpellChecker()
    correct=""
    words=spell.split_words(sentence)
    for word in words:
        correct = correct + " " + spell.correction(word)
    print("Output ",correct)
    sen = correct
    correct=""
    ch=Speller(lang='en')
    words=spell.split_words(sen)
    correct=ch(sen)

    print("Auto Corrected",correct)
    return correct

def modelRun():
    new = pd.read_csv('sign_mnist_test.csv')
    new_test = np.array(new, dtype='float32')
    new_test = new_test.reshape((-1, 28, 28, 1))
    predicted_classes = model.predict_classes(new_test)
    return  predicted_classes


def output():
    classes=modelRun()
    dictt = {'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5','g':'6','h':'7',
    'i':'8','j':'9','k':'10','l':'11','m':'12','n':'13','o':'14','p':'15','q':'16',
    'r':'17','s':'18','t':'19','u':'20','v':'21','w':'22','x':'23','y':'24','z':'25'
    }
    key_list = list(dictt.keys())
    val_list = list(dictt.values())
    output=""
    for i in classes:
        j= str(i)
        index = val_list.index(j)
        output= output + key_list[index]

    output = check(output)
    output = output + " "
    file = open("output.txt","a+")    
    file.write(output)
    file.close()