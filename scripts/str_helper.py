from nltk import word_tokenize, pos_tag, FreqDist
from nltk.corpus import stopwords
import io
import pandas as pd
import re
import numpy as np
import math


def split_words_aggro(abst):
    """
    Aggresive tokenization; splits on any non-words
    """
    return re.sub(r'([a-zA-Z])[^a-zA-Z]+([a-zA-Z])', r'\1 \2', abst) 

def split_words(abst):
    """
    Tokenization only on delimiters: '-', ',', '/'
    """
    return re.sub(r'([a-zA-Z])[\-\/]([a-zA-Z])', r'\1 \2', abst) 

def remove_stopwords(s):
# 	nltk_stopwords = ['i',  'me',  'my',  'myself',  'we',  'our',  'ours',  'ourselves',  'you',  "you're",  "you've",  "you'll",  "you'd",  'your',  'yours',  'yourself',  'yourselves',  'he',  'him',  'his',  'himself',  'she',  "she's",  'her',  'hers',  'herself',  'it',  "it's",  'its',  'itself',  'they',  'them',  'their',  'theirs',  'themselves',  'what',  'which',  'who',  'whom',  'this',  'that',  "that'll",  'these',  'those',  'am',  'is',  'are',  'was',  'were',  'be',  'been',  'being',  'have',  'has',  'had',  'having',  'do',  'does',  'did',  'doing',  'a',  'an',  'the',  'and',  'but',  'if',  'or',  'because',  'as',  'until',  'while',  'of',  'at',  'by',  'for',  'with',  'about',  'against',  'between',  'into',  'through',  'during',  'before',  'after',  'above',  'below',  'to',  'from',  'up',  'down',  'in',  'out',  'on',  'off',  'over',  'under',  'again',  'further',  'then',  'once',  'here',  'there',  'when',  'where',  'why',  'how',  'all',  'any',  'both',  'each',  'few',  'more',  'most',  'other',  'some',  'such',  'no',  'nor',  'not',  'only',  'own',  'same',  'so',  'than',  'too',  'very',  's',  't',  'can',  'will',  'just',  'don',  "don't",  'should',  "should've",  'now',  'd',  'll',  'm',  'o',  're',  've',  'y',  'ain',  'aren',  "aren't",  'couldn',  "couldn't",  'didn',  "didn't",  'doesn',  "doesn't",  'hadn',  "hadn't",  'hasn',  "hasn't",  'haven',  "haven't",  'isn',  "isn't",  'ma',  'mightn',  "mightn't",  'mustn',  "mustn't",  'needn',  "needn't",  'shan',  "shan't",  'shouldn',  "shouldn't",  'wasn',  "wasn't",  'weren',  "weren't",  'won',  "won't",  'wouldn',  "wouldn't"]
    nltk_stopwords = stopwords.words('english')
    STOPWORDS = nltk_stopwords+["'s", "’s"]+[x.capitalize() for x in nltk_stopwords]
    tokens = word_tokenize(s)
    okstr = ' '.join([x for x in tokens if x in ['(',')'] or x not in STOPWORDS and len(x)>1])
    return okstr

def remove_punct(s):
    s = re.sub(r'[^A-Za-z\-\s]+', '', s)
    return s


def filter_pos_tags(s):
    OUT = ['VBD', 'IN', 'VBP', 'RB', 'MD', 'VB', 'VBZ', 'VBG']
    return ' '.join([w for w,t in pos_tag(word_tokenize(s)) if t not in OUT])


def tokenize(s):
    return word_tokenize(s)


def abbr_expander(s):   
    """
    Simple abbreviation handler. Underlying assumption is that the first occurrence of an abbreviation will be preceded by its full form.
    Function parses text to identify candidate expansions, and expands all other occurrences of that abbreviation in the document.
    """

    res = re.findall(r'\(\s?[A-Z]\s?[A-Za-z]+\s?\)', s) # Misses acronyms with hyphen
           
    outs = s
    for abbr in res:
        ix = s.index(abbr)
        abbr_clean = re.sub(r'[^A-Za-z]', '', abbr) # keep only letters, discard all other chars
        abbr_len = len(re.sub(r'[a-z]','',abbr_clean)) # Number of capital letters ~ number of tokens to look back for expansion
        if abbr_clean[-1]=='s': abbr_len-=1 # Singularing a plural acronym
        # When looking for expansion candidates, consider (-) and (/) as word-breaks
        candidate_l = split_words_aggro(s[ix-1::-1][::-1].rstrip()).split(' ')[-abbr_len:] # identify possible candidates for expansion from preivous abbr_len words
        expansion_l = [] 
        
        aix=0
        wix=0
        # print(abbr_clean, candidate_l)
        while aix<len(abbr_clean) and wix<len(candidate_l):
            if abbr_clean[aix].lower()==candidate_l[wix][0].lower():
                expansion_l.append(candidate_l[wix])
                aix+=1
                wix+=1
            elif abbr[aix].lower() in candidate_l[max(0,wix-1)].lower():
                aix+=1
            else:
                wix+=1

        if len(expansion_l)>0.4*abbr_len:
            expanded = ' '.join(expansion_l)
            outs = outs.replace(' '+abbr, '') # Remove first instance of abbreviation before expanding other instances
            if abbr_clean[-1]=='s':
                outs = outs.replace(abbr_clean[:-1], expanded)
            else:
                outs = outs.replace(abbr_clean, expanded) 
            # print(abbr,expanded)

    return outs



def clean_sent(abst):
    abst = split_words(abst)
    abst = abbr_expander(abst)    
    abst = re.sub(r"(?<=\. )[A-Z]",lambda t:t.group().lower(), abst) # Make post-period and first word uppercase chars lower
    abst = abst[0].lower()+abst[1:]
    abst = remove_punct(abst)
    return abst


def sim(v1, v2):
    return 1-cosine(v1,v2)


def idf(doclist):
    N = len(doclist)
    vocab = list(FreqDist(word_tokenize(' '.join(doclist))).keys())
    idfd={}
    for w in vocab:
        idfd[w] = math.log(N/max(1,sum([1 for d in doclist if w in d])), 10)
    return idfd


def tfidfDist(doclist):
    idf_lookup = idf(doclist)
    docs_tfidf = []
    for doc in doclist:
        token_fd = list(FreqDist(word_tokenize(doc)).items())
        tfidf = [(w, freq*idf_lookup[w]) for w,freq in token_fd]
        docs_tfidf.append(sorted(tfidf, key=lambda x:x[1], reverse=True))
    return docs_tfidf


def filter_bottom_tfidf(doclist, cutoff_pcile=0.2):
    """
    Remove `cutoff_pcile`% words having lowest TF-IDF scores
    """
    tfidf_vals = tfidfDist(doclist)
    filt_docs=[]

    for c,doc in enumerate(doclist):
        tf = tfidf_vals[c]
        allowed = [w for w,n in tf[:math.ceil((1-cutoff_pcile)*len(tf))]]
        filt_docs.append(' '.join([w for w in word_tokenize(doc) if w in allowed]))

    return filt_docs