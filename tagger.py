import spacy
import csv

pathuntagged = input('Enter path to untagged corpus?')


FileData = open(pathuntagged, "r")

nlp = spacy.load("de_dep_news_trf")
    
language = input('What language are you training? ')

def replaceword(lines):
    newsent = []
    sentence = lines.split()
    sentence = sentence[1:]
    sentence = " ".join(sentence)
    linessplit = sentence.split()
    sentence = nlp(sentence)
    for word in sentence:
        wordPOS = f'{word.text}/{word.pos_}'
        newsent.append(wordPOS)
    return " ".join(newsent)
        
for lines in FileData:
    newline = replaceword(lines)
    #outputfile = open(f"{language}taggedcorpus.txt", "a")
    #outputfile.write(f'{newline}\n')
    #outputfile.close()
    with open(f"{language}taggedcorpus.csv", mode='a') as outputfile:
        output_writer = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow([lines, newline])

