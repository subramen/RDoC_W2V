from nltk import word_tokenize
from nltk.corpus import stopwords
import io
import pandas as pd
import re
import numpy as np
from collections import defaultdict



def get_df_from_psv(fout=None):
    with open('data/output.psv', encoding="utf-8") as f:
        strr = f.read()
    df_str = re.sub(r'\n(?![0-9])', ' ', strr)


    df = pd.read_csv(io.StringIO(df_str), sep='|', error_bad_lines=False) #bad lines: [4399, 170914, 247161, 264812, 384966, 400521, 522365, 527597, 651243, 747036]

    # at least one row had the title in label col. 
    df.art_arttitle = np.where(df.art_arttitle.isnull() & df.label.notnull(), df.label, df.art_arttitle)

    df.columns = ['pmid', 'title', 'abstract', 'label']
    df.abstract = df.abstract.fillna('')

    # combine sectioned abstracts
    s=df.pmid.value_counts()
    mult_pmid = df[df.pmid.isin(s.index[s>1])]
    single_pmid = df[~df.pmid.isin(s.index[s>1])]
    mult_pmid2 = mult_pmid.groupby(['pmid']).abstract.transform(lambda x: ' '.join(x))
    mult_pmid['abstract'] = mult_pmid2
    mult_pmid = mult_pmid.drop_duplicates(subset=['pmid','abstract'])
    data_df = single_pmid.append(mult_pmid)

    data_df['content'] = np.where(data_df.title!=data_df.abstract, data_df.title+' '+data_df.abstract, data_df.abstract)

    if not fout:
        import datetime
        fout = "data/datadf_"+str(datetime.datetime.now()).replace(' ','_').replace(':','')+".pkl"
    data_df.to_pickle(fout)

    return data_df



def remove_stopwords(s):
	# nltk_stopwords = ['i',  'me',  'my',  'myself',  'we',  'our',  'ours',  'ourselves',  'you',  "you're",  "you've",  "you'll",  "you'd",  'your',  'yours',  'yourself',  'yourselves',  'he',  'him',  'his',  'himself',  'she',  "she's",  'her',  'hers',  'herself',  'it',  "it's",  'its',  'itself',  'they',  'them',  'their',  'theirs',  'themselves',  'what',  'which',  'who',  'whom',  'this',  'that',  "that'll",  'these',  'those',  'am',  'is',  'are',  'was',  'were',  'be',  'been',  'being',  'have',  'has',  'had',  'having',  'do',  'does',  'did',  'doing',  'a',  'an',  'the',  'and',  'but',  'if',  'or',  'because',  'as',  'until',  'while',  'of',  'at',  'by',  'for',  'with',  'about',  'against',  'between',  'into',  'through',  'during',  'before',  'after',  'above',  'below',  'to',  'from',  'up',  'down',  'in',  'out',  'on',  'off',  'over',  'under',  'again',  'further',  'then',  'once',  'here',  'there',  'when',  'where',  'why',  'how',  'all',  'any',  'both',  'each',  'few',  'more',  'most',  'other',  'some',  'such',  'no',  'nor',  'not',  'only',  'own',  'same',  'so',  'than',  'too',  'very',  's',  't',  'can',  'will',  'just',  'don',  "don't",  'should',  "should've",  'now',  'd',  'll',  'm',  'o',  're',  've',  'y',  'ain',  'aren',  "aren't",  'couldn',  "couldn't",  'didn',  "didn't",  'doesn',  "doesn't",  'hadn',  "hadn't",  'hasn',  "hasn't",  'haven',  "haven't",  'isn',  "isn't",  'ma',  'mightn',  "mightn't",  'mustn',  "mustn't",  'needn',  "needn't",  'shan',  "shan't",  'shouldn',  "shouldn't",  'wasn',  "wasn't",  'weren',  "weren't",  'won',  "won't",  'wouldn',  "wouldn't"]
    nltk_stopwords = stopwords.words('english')
    STOPWORDS = nltk_stopwords+["'s", "’s"]+[x.capitalize() for x in nltk_stopwords]
    
    s = re.sub(r'([a-zA-Z])[\-\/]([a-zA-Z])', r'\1 \2', s) # split hyphenated and slashed words
    s = re.sub(r'[^A-Za-z\s]+', '', s)
    tokens = word_tokenize(s)
    okstr = ' '.join([x for x in tokens if x in ['(',')'] or x not in STOPWORDS and len(x)>1])
    return okstr



def abbr_expander(s):   
    res = re.findall(r'\(\s?[A-Z]\s?[A-Za-z]+\s?\)', s) # Misses acronyms with hyphen
    outs = s
    retstr = ''
    for abbr in res:
        ix = s.index(abbr)
        abbr_clean = re.sub(r'[^A-Za-z]', '', abbr) # keep only letters, discard all other chars
        abbr_len = len(re.sub(r'[a-z]','',abbr_clean)) # Number of capital letters ~ number of tokens to look back for expansion
        if abbr_clean[-1]=='s': abbr_len-=1 # Singularing a plural acronym
        # When looking for expansion candidates, consider (-) and (/) as word-breaks
        expanded = ' '.join(s[ix-1::-1][::-1].rstrip().split(' ')[-abbr_len:]) # identify possible candidates for expansion from preivous abbr_len words
        # ABBR_LIST[abbr_clean].append(expanded)
        outs = outs.replace(' '+abbr, '') # Remove first instance of abbreviation before expanding other instances
        if abbr_clean[-1]=='s':
            outs = outs.replace(abbr_clean[:-1], expanded)
        else:
            outs = outs.replace(abbr_clean, expanded) 
        
    return outs


def clean_line_generator(df_pkl=None):
    if not df_pkl:
        data_df = get_df_from_psv()
    else:
        data_df = pd.read_pickle(df_pkl)
    data_df = data_df[data_df.content.notnull()]
    with open('/home/sus118/rdoc_w2v/data/one-abstract-per-line.txt', 'w') as f:
        count = 0
        for abst in iter(data_df.content):
            if not abst:
                continue
            abst = abbr_expander(abst)
            # Make post-period uppercase chars lower
            abst = re.sub(r"(?<=\. )[A-Z]",lambda t:t.group().lower(), abst)
            abst = remove_stopwords(abst)
            f.write(abst+'\n')
            count+=1
            if count%10000==0:
                print(f'{count} done')
    

if __name__=="__main__":
    clean_line_generator('/home/sus118/rdoc_w2v/data/datadf_2019-11-12_174955.984110.pkl')