# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 01:11:10 2021

@author: FaizanSyed
"""
#pip install string-color

from stringcolor import * 
import logic

def KW(keyindex, line_text ,Surrounding_word):    
    
    
    #keyindex = "one/cd"
    #line_text = logic.SQLQuery("select line_text from english_corpus where line_id in (2819, 4702, 4704, 5756, 5758, 5760, 5783, 5788, 5791, 5792, 5896, 5898, 5924, 5931, 18992);")
    sentencedic = dict()
    #print(line_text)
    sentlist = []

    for x in range(0,len(line_text)):
        sentencedic[keyindex] = line_text[x]
        wordlist = sentencedic[keyindex].split()
    
    "I have a Primary number two three"
    for i in range(0,len(line_text)):
    
        if keyindex in line_text[i]:
            result = line_text[i].index(keyindex)
            split_text = line_text[i].split()
            keywordindex = int(split_text.index(keyindex))
            string = split_text
         #   print(string)
        
            ngrams = [string[i:i+((Surrounding_word*2)+1)] for i in range(len(string)-5)]
           # print(string[i+5:i+10])
            
        
            kwicdict = {}
            for n in ngrams:
                if keyindex not in kwicdict:
                    kwicdict[keyindex] = [n]
                else:
                    kwicdict[keyindex].append(n)
        
            for n in kwicdict[keyindex]:
                outstring = ' '.join(n[:Surrounding_word]).rjust(50)
                outstring += str(cs( keyindex , "DarkViolet2" )).center(len(keyindex)+20)
                outstring += ' '.join(n[Surrounding_word+1:])
                sentlist.append(outstring)
            #print(cs(outstring, "DarkViolet2", "lightgrey6"))
            for sents in sentlist:
                print(sents)
#black/jj
#one/cd
#from/in
#two/cd
#with/in
#into/in
#the/at
#of/in




Kwic_check= KW("black/jj" ,logic.SQLQuery("select line_text from english_corpus where line_id in (2819, 4702, 4704, 5756, 5758, 5760, 5783, 5788, 5791, 5792, 5896, 5898, 5924, 5931, 18992);"),5)

