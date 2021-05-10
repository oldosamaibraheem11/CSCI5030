"""
Created on Fri Apr 23 01:11:10 2021
@author: FaizanSyed
"""
import logic
import re


def KW(word_selected, line_text , surrounding_word, wordamount):
    
 
    sentencedic = dict()
    sentlist = []
    
    for x in range(0,len(line_text)):
        sentencedic[word_selected] = line_text[x]
        wordlist = sentencedic[word_selected].split()
        
    idx = 0
    for i in range(0,len(line_text)):
        if word_selected in line_text[i]:
            result = line_text[i].index(word_selected)
            sentence_split = re.findall(f"[\w']+|[.,!?;]", line_text[i])
            for words in sentence_split:
                if word_selected in words:
                    keywordindex = sentence_split.index(words)
            string = sentence_split
            if wordamount == -1:
                ngrams=[]
                surrounding_word = len(string)
                for i in range(len(string)-(surrounding_word-1)):
                    ngrams.append(string[i:i+(surrounding_word)])

                    if word_selected in ngrams[i]:
                        keynumber = ngrams[i].index(word_selected)
                kwicdict = {}

                for n in ngrams:
                    if n[keynumber] not in kwicdict:
                        kwicdict[n[keynumber]] = [n]
                    else:
                        kwicdict[n[keynumber]].append(n)
                try:
                    count= 0 
                    for n in kwicdict[word_selected]:

                        outstring1 = ' '.join(n[:keynumber])
                        outstring2 = "<b><span style='color:red;'>"+word_selected+"</span></b>"
                        outstring3 = ' '.join(n[keynumber+1:])
                        idx = idx+1
                        table_row_num = str(idx)

                        sentlist.append('<tr ><td style = padding-top:30px;>'+table_row_num+"."+ " &nbsp; " +outstring1+ " &nbsp; " + outstring2 + " &nbsp;"+outstring3+'</td></tr>  ')
                        
                except:
                    pass
            else:
                ngrams=[]
                for i in range(len(string)-(surrounding_word-1)):
                    ngrams.append(string[i:i+(surrounding_word)])

                keynumber = int((surrounding_word-1)/2)
                kwicdict = {}
                
                for n in ngrams:
                    if n[keynumber] not in kwicdict:
                        kwicdict[n[keynumber]] = [n]
                    else:
                        kwicdict[n[keynumber]].append(n)
                try:

                    for n in kwicdict[word_selected]:
                        outstring1 =' '.join(n[:keynumber])
                        outstring2 = word_selected
                        outstring3 = ' '.join(n[(keynumber+1):])
                        idx = idx+1
                        table_row_num = str(idx)
                        sentlist.append('<tr><td>'+table_row_num+"."+'</td>'+'<td style="text-align:right;">'+outstring1+'</td><td style="text-align:left; font-weight: bold;color: rgb(255,20,20);">'+ " &nbsp; " + outstring2 + " &nbsp;"+'</td><td style="text-align:left;">'+outstring3+'</td></tr>')
                except:
                    pass
        

    return sentlist


def KWlist(word_selected , biglist,surrounding_word,wordamount):
    sentence_list_cluster=[]

    for small_list in biglist:
        new_list = KW(word_selected, small_list,surrounding_word,wordamount)
        sentence_list_cluster.append(new_list)

    return sentence_list_cluster 
