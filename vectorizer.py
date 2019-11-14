from gensim.models import Word2Vec
import tempfile

class sentenceGenerator: # use limit for sampling
    def __init__(self, f, limit=None):
        self.f=f
        self.li = limit

    def __iter__(self):
        c=0
        for l in open(self.f):
            if self.li and c>=self.li:
                break
            c+=1
            yield l.split()


fname = '/home/sus118/rdoc_w2v/data/one-abstract-per-line.txt'
sg=sentenceGenerator(fname)
model = Word2Vec(sg, size=200, window=5, min_count=3, sg=1, hs=1, workers=6)
# word_vectors = model.wv

with tempfile.NamedTemporaryFile(prefix='gensim-model-', delete=False) as tmp:
    temporary_filepath = tmp.name
    model.save(temporary_filepath)