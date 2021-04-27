import logic
from gensim.models import Word2Vec
import numpy



def SetUpDB(language):
    try:
        logic.SQLQuery(f"ALTER TABLE {language}_corpus ADD vector DOUBLE;")
    except:
        pass

language = input("What language will you be training? ")
SetUpDB(language)
model = input('What is the name of the model you would like to use? ')
model = Word2Vec.load(f"models/{model}.model")

data_lists = logic.VectorData(f"SELECT Line_ID, Line_text FROM {language}_corpus;")

for lists in data_lists:
    lineID = lists[0]
    sentence = lists[1]
    sentence = sentence.split()
    sentenceVectorList = list()
    for words in sentence:
        words = words.split("/",1)
        words = words[0]
        try:
            vector = model.wv[f'{words}']
            sentenceVectorList.append(vector.mean())
        except:
            pass
    sentenceVectorList = numpy.array(sentenceVectorList)
    sentenceVector = sentenceVectorList.mean()
    logic.SQLInsertQuery(f"UPDATE {language}_corpus SET vector = {sentenceVector} WHERE Line_id = {lineID};")