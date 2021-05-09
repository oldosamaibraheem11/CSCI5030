use wordsense;

DROP TABLE IF EXISTS English_Corpus;

/* Set up structure of English corpus table */
create table English_Corpus (
	Line_ID INT NOT NULL AUTO_INCREMENT,
    Lang_ID INT NOT NULL,
    Doc_ID INT NOT NULL,
    Doc_Name varchar(25),
	Line_Text blob not null,
	Last_Update datetime not null,
	primary key (Line_ID),
    FOREIGN KEY (Lang_ID) REFERENCES Lang_Ref(Lang_ID));


/* This is a good step to include in the case the existing table is corrupted in some way */
DROP TABLE IF EXISTS Italian_Corpus;

/* Set up structure of French corpus table */
create table Italian_Corpus (
	Line_ID INT NOT NULL AUTO_INCREMENT,
    Lang_ID INT NOT NULL,
    Doc_ID INT NOT NULL,
    Doc_Name varchar(25),
	Line_Text blob not null,
	Last_Update datetime not null,
	primary key (Line_ID),
    FOREIGN KEY (Lang_ID) REFERENCES Lang_Ref(Lang_ID));

DROP TABLE IF EXISTS German_Corpus;

CREATE TABLE German_Corpus (
	Line_ID INT NOT NULL AUTO_INCREMENT,
    Lang_ID INT NOT NULL,
    Doc_ID INT NOT NULL,
    Doc_Name varchar(25),
	Line_Text longtext not null,
	Last_Update datetime not null,
	primary key (Line_ID),
    FOREIGN KEY (Lang_ID) REFERENCES Lang_Ref(Lang_ID));


drop table if exists german_index;
drop table if exists french_index;
drop table if exists french_corpus;
drop table if exists Italian_index;
drop table if exists English_index;

alter table English_corpus modify column line_text longtext;
alter table Italian_corpus modify column line_text longtext;
alter table German_corpus modify column line_text longtext;

UPDATE Lang_Ref SET Lang_Desc = "English" WHERE Lang_ID = 1;
UPDATE Lang_Ref SET Lang_Desc = "Italian" WHERE Lang_ID = 2;
UPDATE Lang_Ref SET Lang_Desc = "German" WHERE Lang_ID = 3;


DROP TABLE IF EXISTS Speech_Parts;

/* Set up structure of table */
create table Speech_Parts (
	Part_ID INT NOT NULL AUTO_INCREMENT,
    Lang_ID INT NOT NULL,
	Part_Desc varchar(50) not null,
	Last_Update datetime not null,
	primary key (Part_ID),
    FOREIGN KEY (Lang_ID) REFERENCES Lang_Ref(Lang_ID));


insert into Speech_Parts (Lang_ID, Part_Desc, Last_Update)
values (1,"Adjective",Now()),
	(1,"Adposition",Now()),
	(1,"Adverb",Now()),
	(1,"Conjunction",Now()),
	(1,"Determiner",Now()),
    (1,"Interjection",Now()),
    (1,"Noun",Now()),
    (1,"Particle",Now()),
    (1,"Pronoun",Now()),
    (1,"Verb",Now()),
    (2,"Adposition",Now()),
	(2,"Aggettivo",Now()),
	(2,"Avverbio",Now()),
	(2,"Congiunzione",Now()),
	(2,"Determinante",Now()),
    (2,"Interiezione",Now()),
    (2,"Particella",Now()),
    (2,"Pronome",Now()),
	(2,"sostantivo",Now()),
    (2,"verbo",Now()),
	(3,"Adjektiv",Now()),
	(3,"Adposition",Now()),
	(3,"Adverb",Now()),
	(3,"Bestimmer",Now()),
	(3,"Interjektion",Now()),
    (3,"Konjunktion",Now()),
    (3,"Partikel",Now()),
    (3,"Pronomen",Now()),
	(3,"Substantiv",Now()),
    (3,"Verb",Now());