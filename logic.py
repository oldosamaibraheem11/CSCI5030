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


app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'Osamas-MacBook-Pro.local'
# app.config['MYSQL_USER'] = 'Osama'
# app.config['MYSQL_PASSWORD'] = 'CSCI5030SLU2021'
# app.config['MYSQL_DATABASE_DB'] = 'wordsense'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'CSCI5030SLU2021'
app.config['MYSQL_DATABASE_DB'] = 'wordsense'

mysql = MySQL(app)
conn = mysql.connect()
cursor = conn.cursor()

english_pos_mapping = {
    "NN":"Noun", 
    "NN$":"Noun",
    "NNS":"Noun",
    "NNS$":"Noun",
    "NP":"Noun",
    "NP$":"Noun",
    "NPS":"Noun",
    "NPS$":"Noun",
    "NR":"Noun",
    "NRS":"Noun",
    "VB":"Verb",
    "VBD":"Verb",
    "VBG":"Verb",
    "VBN":"Verb",
    "VBP":"Verb",
    "VBZ":"Verb",
    "PN":"Pronoun",
    "PN$":"Pronoun",
    "PP$":"Pronoun",
    "PP$$":"Pronoun",
    "PPL":"Pronoun",
    "PPLS":"Pronoun",
    "PPO":"Pronoun",
    "PPS":"Pronoun",
    "PPSS":"Pronoun",
    "WP$":"Pronoun",
    "WPO":"Pronoun",
    "WPS":"Pronoun",
    "JJ":"Adjective",
    "JJR":"Adjective",
    "JJS":"Adjective",
    "JJT":"Adjective",
    "RB":"Adverb",
    "RBR":"Adverb",
    "RBT":"Adverb",
    "RN":"Adverb",
    "RP":"Adverb",
    "WRB":"Adverb",
    "CC":"Conjunction",
    "CS":"Conjunction",
    "AT":"Article",
    "UH":"Interjection"
}

def tuple2list(ExTuple):
    ExList = list(itertools.chain(*ExTuple))
    return ExList 

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
        return data
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

def CreateIndexing(sentence, line_id, dictionary):
    word_list = sentence.split()
    # number of parts formed for each tagged word in the corpus(word/pos)
    tagged_word_parts = 2   
    for word in word_list:
        # skip untagged words
        if(len(word.split('/')) != tagged_word_parts):
            continue
        subtag = (word.split('/')[1]).upper()
        # ignore -TL suffix in subtags since they are just to indicate that the word occurs in title
        subtag = subtag.split('-TL')[0]
        if(subtag in logic.english_pos_mapping):
            generalized_pos = logic.english_pos_mapping[subtag]
        else:
            generalized_pos = subtag        
        word = (word.split('/')[0] + "/" + generalized_pos).lower()
        dictionary[word].append(line_id)        
    return dictionary

def StoreIndexing(dictionary):
    file = open("indexing.txt", "w")
    file.write(dictionary)
    file.close()

def GetIndexing():
    dictionary = {}
    if(os.path.exists("indexing.txt")):
        file = open("indexing.txt", "r")
        dictionary = json.loads(file.read())
    return dictionary
    
def isCorpusLoaded(corpus):
    query = f"select count(*) from {corpus}"
    count_list = SQLQuery(query)
    if(count_list[0] == 0):
        return False
    else:
        return True
