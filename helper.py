import requests
import re
import json

import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# install nltk data if needed
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

# ========== GLOBALS ==========

URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Bacteria&prop=extracts&explaintext"

FILENAME = "sents.json"

# ========== MAIN FCNS ==========


def load_or_download():
    try:
        return load_saved_data()
    except:
        return download_and_save()


def download_and_save():
    sents = download_text_from_wikipedia()
    save_to_json(sents)
    return sents


def download_text_from_wikipedia():
    r = requests.get(URL)
    data = r.json()

    # get from JSON
    text = find_key(data, "extract")

    # cleanup headers
    text = re.sub(r"==+ [A-Z][\w\s]+ ==+", "", text)
    text = re.sub(r"(see[\w\s/]+ )", "", text)
    text = text.replace(" (listen); ", "")

    # split into sentences
    sents = fix_sents(sent_tokenize(text))
    sents = sents[:-4]

    res = []
    for sent in sents:
        res.append({"sent": sent, "tokenized": word_tokenize(sent)})
    return res


# ========== HELPER FCNS ==========


def get_terms(input_text):
    """
    Given input text, extract search 'terms' made of
    single words and bigrams, excluding stop words.
    """
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(input_text)
    bigrams = list(zip(tokens, tokens[1:]))

    tokens = [w for w in tokens if not w in stop_words]
    bigrams = [
        " ".join(b)
        for b in bigrams
        if b[0] not in stop_words and b[1] not in stop_words
    ]

    terms = bigrams + tokens
    return terms


def find_key(data, key_name):
    """
    Return value of key in dictionary, wherever it is nested
    """
    if type(data) != dict:
        return
    for key in data.keys():
        if key == key_name:
            return data[key]
        else:
            res = find_key(data[key], key_name)
            if res:
                return res


def fix_sents(sents):
    """
    Assume sentences starting with lowercase letters are
    actually part of the previous sentence, and merge.
    """
    new_sents = []
    i = 1
    while i < len(sents):
        curr_s = sents[i]
        prev_s = sents[i - 1]
        if curr_s[0].islower():
            new_sents.append(" ".join([prev_s, curr_s]))
            i += 1
        else:
            new_sents.append(prev_s)
        i += 1
    return new_sents


# ========== SAVE / LOAD ==========


def load_saved_data():
    with open(FILENAME) as f:
        return json.load(f)


def save_to_json(sents):
    with open(FILENAME, "w") as f:
        json.dump(sents, f)
