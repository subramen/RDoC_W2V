import io
import pandas as pd
import re
import numpy as np
from str_helper import *

def get_df_from_psv(psql_out='data/output.psv', fout=None):
	"""
	Read PSQL output into pandas
	"""
	with open(psql_out, encoding="utf-8") as f:
		strr = f.read()

	df_str = re.sub(r'\n(?![0-9])', ' ', strr) # Regex to handle erratic newlines
	
	df = pd.read_csv(io.StringIO(df_str), sep='|', error_bad_lines=False) 

	# at least one row had the title in label col. 
	df.art_arttitle = np.where(df.art_arttitle.isnull() & df.label.notnull(), df.label, df.art_arttitle)

	df.columns = ['pmid', 'title', 'abstract', 'label']
	df.abstract = df.abstract.fillna('')

	# Sectioned abstracts occur across multiple rows. identify them by multiple occurrences of the same PMID, and then combine.
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



def get_df(df_pkl=None):
	"""
	Helper to read psql output or pickle 
	"""
	if not df_pkl:
		data_df = get_df_from_psv()
	else:
		data_df = pd.read_pickle(df_pkl)
	data_df = data_df[data_df.content.notnull()]
	return data_df




def clean_line_generator_v1(df_pkl=None):
	"""
	Gensim's API reads in the input one document per line. 
	Pre-process each row and persist to file on disk.
	"""
	data_df = get_df(df_pkl)
	
	with open('/home/sus118/rdoc_w2v/data/one-abstract-per-line.txt', 'w') as f:
		count = 0
		for abst in iter(data_df.content):
			if not abst:
				continue
			abst = clean_sent(abst)
			f.write(abst+'\n')
			count+=1
			if count%10000==0:
				print(f'{count} done')



def clean_line_generator_v2(df_pkl=None, fn='untitled'):
	"""
	Gensim's API reads in the input one document per line. 
	Pre-process each row and persist to file on disk.
	"""
    data_df = get_df(df_pkl)                                                                                                                                                 docs = data_df.content.values                                                                                                                                                       cleaned = list(map(clean_sent, docs))
    filt = filter_bottom_tfidf(cleaned)
	with open(f'/home/sus118/rdoc_w2v/data/{fn}.txt', 'w') as f:
                f.writelines(s + '\n' for s in filt)                 
	

if __name__=="__main__":
	clean_line_generator_v1('/home/sus118/rdoc_w2v/data/datadf_2019-11-12_174955.984110.pkl')