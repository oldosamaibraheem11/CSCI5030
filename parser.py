# Author: Pankil Shah
# Created on: 03/13/2021
# Description: Parse a corpus and dump the sentences into the database 

# NLTK is the library used for working with human language data for applying in statistical natural language processing (NLP)
import nltk.data
import logic
import datetime
import sys
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import json
nltk.download('punkt')

# Example path: 'E:\\SLU\\Sem1\\Principles of SD\\Project Material\\brown'
path = input("Enter path of the corpus directory: ")
language = input("Enter language: ")
language_id = str(logic.GetLanguageId(language))
if language_id == "-1":
    sys.exit("Language not found in the database.")
# list of all file names in the corpus directory
file_name_list = []
for file_name in listdir(path):
    if isfile(join(path, file_name)):
        file_name_list.append(file_name)

line_id = 1
document_id = 1
values = ""
dictionary = defaultdict(list)
for file_name in file_name_list:
    # ignore the files CONTENTS and README
    if (file_name != "CONTENTS") and (file_name != "README"):
        file_path = path + '/' + file_name
        with open(file_path, 'r') as file:
            text = file.read().replace('\n', '')
        sent_detector = nltk.data.load('tokenizers/punkt/' + language.lower() + '.pickle')
        sentence_list = sent_detector.tokenize(text.strip())
        for sentence in sentence_list:
            # form the values string required in insert query
            values += "(" + language_id + ", " + str(document_id) + ", " + "'" + file_name + "', " + "\"" + sentence + "\", " + "'" + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "'),"
            dictionary = logic.CreateIndexing(sentence, line_id, dictionary)
            line_id += 1
# remove last comma from values string    
values = values[:-1]
corpus_table = language.lower() + "_corpus"
query = "insert into " + corpus_table + " (Lang_ID, Doc_ID, Doc_Name, Line_Text, Last_Update) values " + values
if(not logic.isCorpusLoaded(corpus_table)):
    logic.SQLInsertQuery(query)
document_id += 1
logic.StoreIndexing(json.dumps(dictionary), 'indexing.txt')