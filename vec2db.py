import logic
from gensim.models import Word2Vec
import numpy
import datetime

def SetUpDB(language):
    try:
        logic.SQLQuery(f"ALTER TABLE {language}_corpus ADD vector DOUBLE;")
    except:
        pass

language = input("What language will you be training? ")
SetUpDB(language)
model = input('What is the name of the model you would like to use? ')
model = Word2Vec.load(f"models/{model}.model")

data_lists = logic.VectorData(f"SELECT * FROM {language}_corpus;")
values = ""
for lists in data_lists:
    lineID = lists[0]
    languageID = lists[1]
    docID = lists[2]
    docName = lists[3]
    sentence = lists[4]
    sentenceVectorList = list()
    for words in sentence.split():
        try:
            vector = model.wv[f'{words}']
            sentenceVectorList.append(vector.mean())
        except:
            pass
    sentenceVectorList = numpy.array(sentenceVectorList)
    if(len(sentenceVectorList) == 0):
        sentenceVector = "null"
    else:
        sentenceVector = sentenceVectorList.mean()
    lastUpdate = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    values += f"({languageID}, {docID}, '{docName}', '{sentence}', '{lastUpdate}', {sentenceVector}),"
values = values[:-1]
truncateQuery = f"truncate {language}_corpus"
logic.SQLInsertQuery(truncateQuery)
insertQuery = f"insert into {language}_corpus (Lang_ID, Doc_ID, Doc_Name, Line_Text, Last_Update, vector) values {values}"
logic.SQLInsertQuery(insertQuery)