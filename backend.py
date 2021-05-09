from flask import Flask, render_template, request, redirect, jsonify
from flaskext.mysql import MySQL
from datetime import datetime
import logic
import json
from collections import defaultdict
import kmeans
app = Flask(__name__)

activesession = {}

@app.route('/', methods =["GET", "POST"])
def homepage():
    sentence_List = []
    sentence_List_clustered = []
    language_list = []
    clusterlist =[]
    part_of_speech_list = []
    page_language_list = []
    error = ""
    # Get the indexing in memory so that we have it until the application is closed
    english_dictionary = logic.GetIndexing("english")
    german_dictionary = logic.GetIndexing("german")
    italian_dictionary = logic.GetIndexing("italian")
    dictionary = {}
    if request.method == "POST":
        language_selected = request.form.get('language')
        activesession['searchlanguage'] = language_selected
        if language_selected.lower() == "english":
            dictionary = english_dictionary
        elif language_selected.lower() == "german":
            dictionary = german_dictionary
        elif language_selected.lower() == "italian":
            dictionary = italian_dictionary
        if(len(dictionary) == 0):
            error = "Indexing file is not present"
        Lang_ID = logic.GetLanguageId(language_selected)
        part_of_speech_selected = request.form.get('partOfSpeech')
        word_selected = (request.form.get('word') + '/' + request.form.get('partOfSpeech')).lower()
        activesession['Word_Selected'] = request.form.get('word')
        if(not logic.isCorpusLoaded(language_selected + "_corpus")):
            error = "Corpus is not loaded into the database"
        if word_selected in dictionary:
            # ignore first and last characters i.e. '[' and ']' to get the list of line ids as a string like "1,3,6,7,...""
            line_ids= str(dictionary[word_selected])[1:][:-1]
            activesession["line_ids"] = line_ids
            sentence_List = logic.SQLQuery(f"select Line_Text from {language_selected}_corpus where Line_id in ({line_ids})")
            clusteramount = request.form["clusteramount"]
            clusterlist = list(range(1,int(clusteramount)+1))
            sentence_List_clustered = kmeans.KMeansClustering(int(clusteramount),line_ids,language_selected)
            if isinstance(sentence_List_clustered, list):
                activesession["sentence_list"] = sentence_List_clustered
                SortSelection = "Following,Ascending"
                sentence_List_clustered = logic.sortsents(request.form.get('word'),sentence_List_clustered,SortSelection)
            else:
                error = sentence_List_clustered
                sentence_List_clustered = []
        if len(sentence_List) == 0:
            error = "Error: Word not in corpus"
    language_list = logic.SQLQuery("SELECT Lang_Desc FROM Lang_Ref;")
    part_of_speech_list = logic.SQLQuery("SELECT Part_Desc FROM Speech_Parts WHERE Lang_ID = 1;")
    page_language_list = logic.SQLQuery("select Language_Page from Page_Translation;")
    word_translated_list = logic.SQLQuery("select * from Page_Translation WHERE Language_Page = 'english';")
    return render_template('index.html', language_list = language_list, part_of_speech_list=part_of_speech_list, sentence_List_clustered=sentence_List_clustered, error=error,page_language_list=page_language_list,word_translated_list=word_translated_list)

@app.route('/Query', methods =["GET", "POST"])
def Query():
    language_list = logic.SQLQuery("SELECT Lang_Desc FROM Lang_Ref;")
    language_selected = request.form.get('language')
    Lang_ID = logic.GetLanguageId(language_selected)
    part_of_speech_list = logic.SQLQuery(f"SELECT Part_Desc FROM Speech_Parts WHERE Lang_ID = '{Lang_ID}';")
    return render_template('partofspeech.html', part_of_speech_list=part_of_speech_list )

@app.route('/Page', methods =["GET", "POST"])
def Page():
    page_language_selected = request.form.get('language')
    word_translated_list = logic.SQLQuery(f"select * from Page_Translation WHERE Language_Page = '{page_language_selected}';")
    return jsonify(word_translated_list)

@app.route('/Sort', methods =["GET", "POST"])
def Sort():
    SortSelection = request.form.get('language')
    word = activesession['Word_Selected'].lower()
    sent_list = activesession["sentence_list"]
    nested_list = logic.sortsents(word,sent_list,SortSelection)
    return render_template('clusters.html', sentence_List_clustered=nested_list)

@app.route('/Vec', methods =["GET", "POST"])
def Vec():
    error = ""
    clusteramount = request.form.get('language')
    word = activesession['Word_Selected']
    line_ids = activesession["line_ids"]
    language_selected = activesession['searchlanguage']
    sentence_List_clustered = kmeans.KMeansClustering(int(clusteramount),line_ids,language_selected)
    if isinstance(sentence_List_clustered, list):
        activesession["sentence_list"] = sentence_List_clustered
        SortSelection = "Following,Ascending"
        sentence_List_clustered = logic.sortsents(word,sentence_List_clustered,SortSelection)
    else:
        error = sentence_List_clustered
        sentence_List_clustered = []
    return render_template('clusters.html', sentence_List_clustered=sentence_List_clustered, error=error)

if __name__ == '__main__':
    app.run(debug = True)