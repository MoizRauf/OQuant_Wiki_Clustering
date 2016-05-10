import nltk
from stop_words import get_stop_words
from nltk import RegexpTokenizer, PorterStemmer
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import re
__author__ = 'moiz'


def tokenize_and_stem(doc):
    tokenizer = RegexpTokenizer(r'\w+')
    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    tokens = tokenizer.tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in en_stop and len(token) > 2]
    final = [p_stemmer.stem(word) for word in clean]


    return final



def tokenize(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def NERTagging(text):
    log_file = open("Dump/log/Main_output.txt", "a")
    st = StanfordNERTagger('resources/ner/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'resources/ner/stanford-ner.jar',
					   encoding='utf-8')
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    log_file.write('NER \n %s \n' % classified_text)
    print(classified_text)
    log_file.close()
    return

def POSTagging(text):
    log_file = open("Dump/log/Main_output.txt", "a")
    tokenized_text = word_tokenize(text)
    tagged_text = nltk.pos_tag(tokenized_text)
    log_file.write(
            'POS \n %s \n--------------------------\n' % tagged_text)
    print(tagged_text)
    log_file.close()
    return
