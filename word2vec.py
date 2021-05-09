from gensim.models import Word2Vec
from gensim.test.utils import datapath
from gensim import utils
import logging
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MyCorpus(object):
    def __init__(self,path):
        self.path = path
    def __iter__(self):
        CorpusPath = datapath(self.path)
        for line in open(CorpusPath):
            yield utils.simple_preprocess(line)
PathToFile = input("Enter the path to the corpus: ")
CorpusName = input("What is the name of your corpus (this will be the name of model)? ")
AllSentences = MyCorpus(PathToFile)
model = Word2Vec(sentences=AllSentences, window=5, min_count=2, workers=8,size=248, iter=25)
model.save(f"models/{CorpusName.lower()}.model")

