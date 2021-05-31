from flask import Flask, render_template, request
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
# import ibm_boto3
# from botocore.client import Config
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis 
import warnings
warnings.filterwarnings("ignore")
import urllib
import re
#from bs4 import BeautifulSoup
import requests
import nltk


"""
https://developer.ibm.com/technologies/data-science/patterns/text-summarization-topic-modelling-using-watson-studio-watson-nlu/

"""


app = Flask(__name__)

# The following code contains the credentials for a file in your IBM Cloud Object Storage.
# You might want to remove those credentials before you share your notebook.





# def get_file(filename):
#     '''Retrieve file from Cloud Object Storage'''
#     fileobject = cos.get_object(Bucket=credentials_1['BUCKET'], Key=filename)['Body']
#     return fileobject


def load_string(fileobject):
    '''Load the file contents into a Python string'''
    text = fileobject.read()
    return text

def load_text(file_path):
    with open(file_path, 'r') as filehandle:
        text = filehandle.read()
    return text

ml_text=load_text("cleaned2ML.txt")

'''Get the summary of the text'''

def get_summary(text, pct):
    #mText = text
    #count = len(text.split())
    while True:
        count = len(text.split())
        print(count)
        if count < 1000:
            break
        text = summarize(text,ratio=pct,split=False)
#         summary2 = ''
#         for string in summary:
#             summary2 += string + " "   
    return text

def wordCount(arraySentences):
    count = 0
    for sentence in arraySentences:
        sentenceArr = sentence.split()
        count += len(sentenceArr)
    return count

'''Get the keywords of the text'''

def get_keywords(text):
    #res = keywords(text, ratio=0.1, words=None, split=False, scores=False, pos_filter=('NN', 'JJ'), lemmatize=True, deacc=True)
    res = keywords(text, ratio=0.1, words=None, split=False, scores=False, pos_filter=('NN'), lemmatize=True, deacc=False)

    res = res.split('\n')
    return res

'''Tokenize the sentence into words & remove punctuation'''

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
        
def split_sentences(text):
    """ Split text into sentences.
    """
    sentence_delimiters = re.compile(u'[\\[\\]\n.!?]')
    sentences = sentence_delimiters.split(text)
    return sentences

def split_into_tokens(text):
    """ Split text into tokens.
    """
    tokens = nltk.word_tokenize(text)
    return tokens
    
def POS_tagging(text):
    """ Generate Part of speech tagging of the text.
    """
    POSofText = nltk.tag.pos_tag(text)
    return POSofText


@app.route("/")
def hello():
    return render_template('index.html')



@app.route("/success", methods=["GET", "POST"])
def nike():

    if request.method == "POST":
    

    # check if is pasted lecture or selected input
        is_pasted = request.form.get("selected-input")
    
    # getting textarea info with name = lecture-text in HTML form
        if is_pasted == "select":
            chosen_lecture = request.form.get("selected-lecture")
            lecture_file = "texts/" + chosen_lecture + ".txt"
            lecture_text = load_text(lecture_file)
        else:
            lecture_text = request.form.get("lecture-text")
    
        summarized_text = get_summary(lecture_text, 0.3)
    
        
    #Translation code

        # getting selected option from HTML 
        selected_language = request.form.get("selected-language")

        api_key = 'WxHv05nujh9bllvOYtucz_Xb2wBm7sZjyub6rV-r0inI'
        url = 'https://api.us-south.language-translator.watson.cloud.ibm.com/instances/91ec3ce3-377c-4f54-aac8-d32e56f207fe'
        authenticator = IAMAuthenticator(api_key)
        language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator)

        language_translator.set_service_url(url)

        answer = ""
        model_id = 'en-' + selected_language
        
        translation = language_translator.translate(text=summarized_text, model_id=model_id).get_result()

        answer = translation['translations'][0]['translation']  

        answer_list = answer.splitlines()

        print(answer_list)

        ans_fin = ""
        for sent in answer_list:
            ans_fin =  ans_fin + sent +  "\n"
        
        return render_template('answer.html', summary=ans_fin)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()