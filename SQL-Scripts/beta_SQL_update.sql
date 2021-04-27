use wordsense;

drop table if exists german_index;
drop table if exists french_index;
drop table if exists english_index;

alter table english_corpus modify column line_text longtext;
alter table french_corpus modify column line_text longtext;
alter table german_corpus modify column line_text longtext;

insert into Speech_Parts (Lang_ID, Part_Desc, Last_Update)
values ((
    select distinct lang_id 
    from Lang_ref 
    where Lang_Desc = "Deutsche"),"Conjunction",Now()),
((
    select distinct lang_id 
    from Lang_ref 
    where Lang_Desc = "Deutsche"),"Präposition",Now())