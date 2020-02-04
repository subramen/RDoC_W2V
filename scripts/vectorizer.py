from gensim.models import Word2Vec

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
            
            

def get_model(n=None):
    fname = '/home/sus118/rdoc_w2v/data/one-abstract-per-line.txt'
    print(f"Starting model generation on {n} sentences")
    sg=sentenceGenerator(fname,n)
    model = Word2Vec(sg, size=200, window=5, min_count=3, sg=1, hs=1, workers=6)
    model.save(f'/home/sus118/rdoc_w2v/models/w2v_{n}.model')
    print("Done")

if __name__=="__main__":
    import sys
    if len(sys.argv)>1:
        get_model(sys.argv[1])
    else:
        get_model()