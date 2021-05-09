use wordsense;

DELETE from lang_ref where lang_desc = "Spanish";
DELETE from lang_ref where lang_desc = "Irish";
DELETE from lang_ref where lang_desc = "Arabic";
DELETE from lang_ref where lang_desc = "Hindi";
DELETE from lang_ref where lang_desc = "Chinese";
DELETE from lang_ref where lang_desc = "Urdu";

DROP TABLE IF EXISTS Page_Translation;

create table Page_Translation (
	Lang_ID int NOT NULL,
	Language_Page LONGTEXT NOT NULL,
    Language_Translation LONGTEXT NOT NULL,
    POS_Translation LONGTEXT NOT NULL,
    Error_Translation LONGTEXT NOT NULL,
	PlaceHolder_Translation LONGTEXT NOT NULL,
	Results_Error_Translation LONGTEXT NOT NULL,
	Translate_Page_Translation LONGTEXT NOT NULL,
    Results_Translation LONGTEXT NOT NULL,
    Submit_Translation LONGTEXT NOT NULL,
    number_of_cluster LONGTEXT NOT NULL,
    cluster_Translation LONGTEXT NOT NULL,
    FWA_Translation LONGTEXT NOT NULL,
    FWD_Translation LONGTEXT NOT NULL,
    PWA_Translation LONGTEXT NOT NULL,
    PWD_Translation LONGTEXT NOT NULL);
    
insert into Page_Translation ( Lang_ID, Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation,
 FWA_Translation, FWD_Translation, PWA_Translation, PWD_Translation)
values (1,
"English",
"Language",
"Part of Speech",
"Error",
"Enter the word",
"Word not in corpus",
"Translate page",
"Results",
"Submit",
"Number of clusters",
"Cluster",
"Following Word Ascending",
"Following Word Descending",
"Preceding Word Ascending",
"Preceding Word Descending");

/* Populate Italian data into table */  
insert into Page_Translation (Lang_ID, Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation,
FWA_Translation, FWD_Translation, PWA_Translation, PWD_Translation)
values ( 2,
"Italian",
"Linguaggio",
"Parte del discorso",
"Errore",
"Inserisci la parola",
"Parola non nel corpus",
"Traduci pagina",
"Risultati",
"Invia",
"Numero di cluster",
"Grappolo",
"A seguito di parola ascendente",
"Parola che segue discendente",
"Parola precedente ascendente",
"Parola precedente discendente");


/* Populate German data into table */    
insert into Page_Translation (Lang_ID, Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation,
FWA_Translation, FWD_Translation, PWA_Translation, PWD_Translation)
 values (3,
 "German",
 "Sprache",
 "Teile der Rede",
 "Fehler",
 "Geben Sie das Wort ein",
 "Wort nicht im Korpus",
 "Seite übersetzen",
 "Ergebnisse",
 "Einreichen",
 "Anzahl der Cluster",
 "Cluster",
 "Dem Wort aufsteigend folgen",
 "Folgendes Wort absteigend",
 "Vorangehendes Wort aufsteigend",
 "Vorhergehendes Wort absteigend");
 
 alter table page_translation ADD FOREIGN KEY(Lang_ID) REFERENCES lang_ref(Lang_ID);