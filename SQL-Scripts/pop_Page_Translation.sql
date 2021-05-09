use wordsense;

/* This is a good step to include in the case the existing table is corrupted in some way */
DROP TABLE IF EXISTS Page_Translation;


create table Page_Translation (
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
    cluster_Translation LONGTEXT NOT NULL);


/* Populate English data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
values ("English",
"Language",
"Part of Speech",
"Error",
"Enter the word",
"Word not in corpus",
"Translate page",
"Results",
"Submit",
"Number of clusters",
"Cluster");

/* Populate French data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
values ("French",
"Langue",
"Parties du discours",
"Erreur",
"Entrez le mot",
"Mot pas dans le corpus",
"Traduire la page",
"Résultats",
"Soumettre",
"Nombre de clusters",
"Groupe");

/* Populate Spanish data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
values ("Spanish",
"Idioma ",
"Partes de la oración",
"Error",
"Ingrese la palabra",
"Palabra no en corpus",
"Traducir página",
"Resultados",
"Enviar",
"Numero de clusters",
"Grupo");

/* Populate Irish data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
values ("Irish",
"Teanga",
"codanna den chaint",
"Earráid",
"Iontráil an focal",
"Focal nach bhfuil sa chorpas ",
"Aistrigh leathanach",
"Torthaí",
"Cuir isteach",
"Líon na mbraislí",
"Braisle");

/* Populate Arabic data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
values ("Arabic",
"لغة",
"أجزاء من الكلام",
"خطأ",
"أدخل الكلمة",
"كلمة ليست في المدونة",
"ترجمة الصفحة",
"نتائج",
"يقدم",
"عدد العناقيد",
"تجمع");

/* Populate Hindi data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
values ("Hindi",
"भाषा",
"शब्दभेद",
"त्रुटि",
"शब्द दर्ज करें",
"शब्द कॉर्पस में नहीं",
"अनुवाद पृष्ठ",
"परिणाम",
"प्रस्तुत",
"गुच्छों की संख्या",
"समूह");

/* Populate  Chinese data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
values ("Chinese",
"语言",
"词性",
"错误",
"输入单词",
"单词不在语料库中",
"翻译页面",
"结果",
"提交",
"集群數",
"簇");

/* Populate German data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
 values ("German",
 "Sprache",
 "Teile der Rede",
 "Fehler",
 "Geben Sie das Wort ein",
 "Wort nicht im Korpus",
 "Seite übersetzen",
 "Ergebnisse",
 "Einreichen",
 "Anzahl der Cluster",
 "Cluster");
 
 /* Populate Urdu data into table */    
insert into Page_Translation (Language_Page, Language_Translation, POS_Translation, Error_Translation, PlaceHolder_Translation,Results_Error_Translation,Translate_Page_Translation,Results_Translation,Submit_Translation,number_of_cluster,cluster_Translation)
 values ("Urdu",
 "زبان",
 "تقریر کے کچھ حصے",
 "غلطی",
 "لفظ داخل کریں",
 "لفظ کارپس میں نہیں",
 "زبان کا انتخاب کریں",
 "نتیجہ",
 "جمع کرائیں",
 "گروپوں کی تعداد",
 "جھرمٹ");