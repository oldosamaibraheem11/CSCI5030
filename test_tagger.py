import csv
import tagger

def runTest():
	testResultsFile='tagger_test_results.txt'
	testPOSDictFile='deu_2019_10K_words_pos_base.txt'	
	
	with open (testResultsFile, 'r', encoding="utf8") as g:
		reader = csv.reader(g,delimiter='\t')
		for row in reader:
			word=row[0]
			expectedTag=row[1]
			newWordPOS = tagger.getWordPOS(testPOSDictFile, word)
			if newWordPOS=='':
				print('Fail: Word not in tag dictionary')
				print(word + ' ' + newWordPOS)
			if newWordPOS!=expectedTag and newWordPOS!='':
				print('Fail: Word not tagged correctly')
				print(word + ' ' + newWordPOS)


runTest()