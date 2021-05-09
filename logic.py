# This file will hold useful functions
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import logic
import itertools
import json
import csv
import os.path
import json
import re


app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'Osamas-MacBook-Pro.local'
# app.config['MYSQL_USER'] = 'Osama'
# app.config['MYSQL_PASSWORD'] = 'CSCI5030SLU2021'
# app.config['MYSQL_DATABASE_DB'] = 'wordsense'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'CSCI5030SLU2021'
app.config['MYSQL_DATABASE_DB'] = 'wordsense'


# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'CSCI5030@SLU2021'
# app.config['MYSQL_DATABASE_DB'] = 'wordsense'

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_USER'] = 'pnkls'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'wordsense'

mysql = MySQL(app)
conn = mysql.connect()
cursor = conn.cursor()

english_pos_mapping = {
    "NOUN":"Noun","PROPN":"Noun","VERB":"Verb","AUX":"Verb",
    "PRON":"Pronoun","ADJ":"Adjective","ADP":"Adposition","ADV":"Adverb","CONJ":"Conjunction","SCONJ":"Conjunction",
    "INTJ":"Interjection","PART":"Particle","PUNCT":"Punctuation","NUM":"Numeral","DET":"Determiner","SYM":"Symbol","X":"other"
}
german_pos_mapping = {
    "NOUN":"Substantiv","PROPN":"Substantiv","VERB":"Verb","AUX":"Verb",
    "PRON":"Pronomen","ADJ":"Adjektiv","ADP":"Adposition","ADV":"Adverb","CONJ":"Konjunktion","SCONJ":"Konjunktion",
    "INTJ":"Interjektion","TEIL":"Partikel","PUNCT":"Interpunktion","NUM":"Ziffer","DET":"Bestimmer","SYM":"Symbol","X":"andere"
}
italian_pos_mapping = {
    "NOUN":"sostantivo","PROPN":"sostantivo","VERBO":"verbo","AUX":"verbo",
    "PRON":"pronome","ADJ":"aggettivo","ADP":"adposition","ADV":"avverbio","CONJ":"congiunzione","SCONJ":"congiunzione",
    "INTJ":"interiezione","PARTE":"particella","PUNCT":"punteggiatura","NUM":"numerale","DET":"determinante","SYM":"simbolo","X":"altro"
}

pos_ignore = ["NUM","SYM","PUNCT","X"]

def tuple2list(ExTuple):
    ExList = list(itertools.chain(*ExTuple))
    return ExList 

def VectorData(statment):
    try:
        cursor.execute(statment)
        conn.commit()
        data = cursor.fetchall()
        status = "OKAY"
        purpose = "PRODUCTION"
        SQL_log(statment,status,purpose)
        return data
    except:
        status = "ERROR"
        purpose = "PRODUCTION"
        SQL_log(statment,status,purpose)



def SQLQuery(statment):
    try:
        cursor.execute(statment)
        conn.commit()
        data = logic.tuple2list(cursor.fetchall())
        status = "OKAY"
        purpose = "PRODUCTION"
        SQL_log(statment,status,purpose)
        return data
    except:
        status = "ERROR"
        purpose = "PRODUCTION"
        SQL_log(statment,status,purpose)
    

def SQLInsertQuery(statment):
    try:
        cursor.execute(statment)
        conn.commit()
        status = "OKAY"
        purpose = "PRODUCTION"
        SQL_log(statment,status,purpose)
    except:
        status = "ERROR"
        purpose = "PRODUCTION"
        SQL_log(statment,status,purpose)

def GetLanguageId(language):
    language_id_list = logic.SQLQuery("select Lang_ID from lang_ref where Lang_Desc = '" + language + "'")
    if len(language_id_list) == 0:
        return -1
    else:
        return language_id_list[0]

def SQL_log(statment,status,purpose): # this funcation write to a log everytime a SQL query is ran. This is helpful to see changes to the database. 
    now = datetime.now()
    row = [statment, now.strftime("%d/%m/%Y, %H:%M:%S"),status,purpose]
    headers = ["SQL Statment","Date & Time","Status","Purpose"]
    if os.path.isfile('SQL-Scripts/sql_log.csv'):
        with open('SQL-Scripts/sql_log.csv', 'a') as csvfile:  
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows([row])
    else:
        with open('SQL-Scripts/sql_log.csv', 'a') as csvfile:  
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows([headers])
            csvwriter.writerows([row])

def CreateIndexing(language, sentence, line_id, dictionary):
    if line_id > 0:
        word_list = sentence.split()
        # number of parts formed for each tagged word in the corpus(word/pos)
        tagged_word_parts = 2
        if(language.lower() == "english"):
            mapping = logic.english_pos_mapping
        elif(language.lower() == "german"):
            mapping = logic.german_pos_mapping
        elif(language.lower() == "italian"):
            mapping = logic.italian_pos_mapping
        for word in word_list:
            # skip untagged words
            if(len(word.split('/')) != tagged_word_parts):
                continue
            subtag = (word.split('/')[1]).upper()
            if(subtag in pos_ignore):
                continue
            if(subtag in mapping):
                generalized_pos = mapping[subtag]
            else:
                generalized_pos = subtag        
            word = (word.split('/')[0] + "/" + generalized_pos).lower()
            dictionary.setdefault(word, []).append(line_id)
        
    return dictionary

def StoreIndexing(language, dictionary):
    filename = 'indexing.txt'
    if language.lower() == "english":
        filename = 'englishindexing.txt'
    elif language.lower() == "german":
        filename = 'germanindexing.txt'
    elif language.lower() == "italian":
        filename = 'italianindexing.txt'
    file = open(filename, "w")
    file.write(dictionary)
    file.close()

def GetIndexing(language):
    dictionary = {}
    if language.lower() == "english":
        if(os.path.exists("englishindexing.txt")):
            file = open("englishindexing.txt", "r")
            dictionary = json.loads(file.read())
    elif language.lower() == "german":
        if(os.path.exists("germanindexing.txt")):
            file = open("germanindexing.txt", "r")
            dictionary = json.loads(file.read())
    elif language.lower() == "italian":
        if(os.path.exists("italianindexing.txt")):
            file = open("italianindexing.txt", "r")
            dictionary = json.loads(file.read())
    return dictionary
    
def isCorpusLoaded(corpus):
    query = f"select count(*) from {corpus}"
    count_list = SQLQuery(query)
    if(count_list[0] == 0):
        return False
    else:
        return True

def sortlist(word,biglist,selection):
    if 'Following' in selection:
        mover = 1
    else:
        mover = -1
    if "Ascending" in selection:
        a_z = False
    else:
        a_z = True
    sortdic = {}
    for string in biglist:
        formattedstring = string.lower()
        stringfinder = re.findall(f"[\w']+|[.,!?;]", formattedstring)
        for words in stringfinder:
            if word in words:
                index = stringfinder.index(words)
        try:
            sortword = stringfinder[int((index)+mover)]
        except:
            sortword = stringfinder[int((index))]
        sortdic[string] = sortword
        sortdic = dict(sorted(sortdic.items(), key=lambda item: item[1],reverse=a_z))
    return list(sortdic.keys())

def sortsents(word,biglist,selection):
    nestednewlist = []
    for smalllist in biglist:
        newlist = sortlist(word,smalllist,selection)
        nestednewlist.append(newlist)
    return nestednewlist