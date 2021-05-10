from flask import Flask, render_template, request, redirect, jsonify, url_for
from flaskext.mysql import MySQL
from datetime import datetime
import logic
import json
from collections import defaultdict
import kmeans
import Kwic
app = Flask(__name__)

activesession = {}
english_dictionary = logic.GetIndexing("english")
german_dictionary = logic.GetIndexing("german")
italian_dictionary = logic.GetIndexing("italian")
@app.route('/', methods =["GET", "POST"])
def pagehome():
    return redirect(url_for('homepage'))

@app.route('/homepage', methods =["GET", "POST"])
def homepage():

    language_list = logic.SQLQuery("SELECT Lang_Desc FROM Lang_Ref;")
    part_of_speech_list = logic.SQLQuery("SELECT Part_Desc FROM Speech_Parts WHERE Lang_ID = 1;")
    page_language_list = logic.SQLQuery("select Language_Page from Page_Translation;")
    word_translated_list = logic.SQLQuery("select * from Page_Translation WHERE Language_Page = 'english';")
    return render_template('index.html', language_list = language_list, part_of_speech_list=part_of_speech_list,page_language_list=page_language_list,word_translated_list=word_translated_list)

@app.route('/search', methods =["GET", "POST"])
def search():
    error=""
    sentence_List_clustered = []
    dictionary = {}
    activesession['FullText'] = False
    if request.method == "GET":
        language_selected = request.args.get('language')
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
        part_of_speech_selected = request.args.get('partOfSpeech')
        word_selected = (request.args.get('word') + '/' + request.args.get('partOfSpeech')).lower()
        activesession['Word_Selected'] = request.args.get('word')
        if(not logic.isCorpusLoaded(language_selected + "_corpus")):
            error = "Corpus is not loaded into the database"
        if word_selected in dictionary:
            line_ids= str(dictionary[word_selected])[1:][:-1]
            activesession["line_ids"] = line_ids
            clusteramount = request.args.get('clusteramount')
            clusterlist = list(range(1,int(clusteramount)+1))
            sentence_List_clustered = kmeans.KMeansClustering(int(clusteramount),line_ids,language_selected)
            if isinstance(sentence_List_clustered, list):
                activesession["sentence_list"] = sentence_List_clustered
                SortSelection = "Following,Ascending"
                sentence_List_clustered = logic.sortsents(request.args.get('word'),sentence_List_clustered,SortSelection)
            else:
                error = sentence_List_clustered
                sentence_List_clustered = []
            sentencelength = 5
            activesession['sentlength'] = sentencelength
            sentence_List_clustered = Kwic.KWlist((request.args.get('word')),sentence_List_clustered,int(sentencelength),0)
        if len(sentence_List_clustered) == 0:
            error = "Error: Word not in corpus"
    language_list = logic.SQLQuery("SELECT Lang_Desc FROM Lang_Ref;")
    part_of_speech_list = logic.SQLQuery("SELECT Part_Desc FROM Speech_Parts WHERE Lang_ID = 1;")
    page_language_list = logic.SQLQuery("select Language_Page from Page_Translation;")
    word_translated_list = logic.SQLQuery("select * from Page_Translation WHERE Language_Page = 'english';")
    return render_template('search.html', sentence_List_clustered=sentence_List_clustered, error=error, page_language_list=page_language_list,word_translated_list=word_translated_list)




@app.route('/Query', methods =["GET", "POST"])
def Query():
    language_list = logic.SQLQuery("SELECT Lang_Desc FROM Lang_Ref;")
    language_selected = request.args.get('language')
    Lang_ID = logic.GetLanguageId(language_selected)
    part_of_speech_list = logic.SQLQuery(f"SELECT Part_Desc FROM Speech_Parts WHERE Lang_ID = '{Lang_ID}';")
    return render_template('partofspeech.html', part_of_speech_list=part_of_speech_list )

@app.route('/Page', methods =["GET", "POST"])
def Page():
    page_language_selected = request.args.get('language')
    word_translated_list = logic.SQLQuery(f"select * from Page_Translation WHERE Language_Page = '{page_language_selected}';")
    return jsonify(word_translated_list)

@app.route('/Sort', methods =["GET", "POST"])
def Sort():
    SortSelection = request.args.get('language')
    word = activesession['Word_Selected'].lower()
    sent_list = activesession["sentence_list"]
    nested_list = logic.sortsents(word,sent_list,SortSelection)
    sentencelength = activesession['sentlength']
    if activesession['FullText'] == True:
        nested_list = Kwic.KWlist(word,nested_list,0,-1)
    else:
        nested_list = Kwic.KWlist((word),nested_list,int(sentencelength),0)
    word_translated_list = logic.SQLQuery("select * from Page_Translation WHERE Language_Page = 'english';")
    return render_template('clusters.html', sentence_List_clustered=nested_list,word_translated_list=word_translated_list)

@app.route('/Vec', methods =["GET", "POST"])
def Vec():
    error = ""
    clusteramount = request.args.get('language')
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
    if activesession['FullText'] == True:
        sentence_List_clustered = Kwic.KWlist(word,sentence_List_clustered,0,-1)
    else:
        sentence_List_clustered = Kwic.KWlist((word),sentence_List_clustered,int(sentencelength),0)
    word_translated_list = logic.SQLQuery("select * from Page_Translation WHERE Language_Page = 'english';")
    return render_template('clusters.html', sentence_List_clustered=sentence_List_clustered, error=error,word_translated_list=word_translated_list)
@app.route('/FullText', methods =["GET", "POST"])
def FullText():
    activesession['FullText'] = True
    lastwordsearch = activesession['Word_Selected']
    nestedlist = activesession["sentence_list"]
    sentence_List_clustered = Kwic.KWlist((lastwordsearch),nestedlist,0,-1)
    word_translated_list = logic.SQLQuery("select * from Page_Translation WHERE Language_Page = 'english';")
    return render_template('clusters.html', sentence_List_clustered = sentence_List_clustered,word_translated_list=word_translated_list)

@app.route('/kwic', methods =["GET", "POST"])
def kwic():
    lastwordsearch = activesession['Word_Selected']
    nestedlist = activesession["sentence_list"]
    sentencelength = activesession['sentlength']
    sentence_List_clustered = Kwic.KWlist((lastwordsearch),nestedlist,int(sentencelength),0)
    word_translated_list = logic.SQLQuery("select * from Page_Translation WHERE Language_Page = 'english';")
    return render_template('clusters.html', sentence_List_clustered = sentence_List_clustered,word_translated_list=word_translated_list )

if __name__ == '__main__':
    app.run(debug = True)
