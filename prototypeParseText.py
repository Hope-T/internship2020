import nltk
import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
#used for patterns (NVN)
from nltk import RegexpParser

#make file easier to read
def addNewLine(toEdit):
	myFile = open(toEdit,'a')
	myFile.write("\n")
	myFile.write("\n")
	myFile.close()

#I separated different attack methods by numbering them, so check to see if a line has a number (if it's a new method)
def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)


#prepare file
f = open('prototypeText.txt')
raw = f.read()
raw = word_tokenize(raw)


#clear contents of file before appending
open('filteredtext.txt', 'w').close()

#POS-tagging
raw = pos_tag(raw)
words = raw

for word,POS in words:
#word is the word, POS is the part of speech

	#if x has a number, then it's a new attack method
	if hasNumbers(word):
		addNewLine('filteredtext.txt')

	appendFile = open('filteredtext.txt','a')
	appendFile.write(word + " [" + POS + "] ")
	appendFile.close()

print("We tagged the words! Check the filteredtext file.")
print("Now, let's see the different tools we found.")

#find names of new tools
tools = []
for x,y in words:
	if y == "NNP" or y == "NNPS" or y == "NNS" or y == "NN":
		tools.append(x)

print(tools) 
print()

#find verbs
verbs =[]
for x,y in words:
	if y == "VB":
		verbs.append(x)
print(verbs)
print()

#find noun-verb-noun phrases and noun phrases

patterns= r"""
 P:{<N.*><V.*><DT><N.*>}
   {<DT><N.*><V.*><N.*>}
   {<V.*><DT><N.*>}
 NP:
     {<VBD><N.*>}
     {<VBG><N.*>}
     {<VBN><N.*>}

"""
chunker = RegexpParser(patterns)
tree = chunker.parse(raw)

print("Print the noun phrases.")
for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
    # print the noun phrase as a list of part-of-speech tagged words
    print(subtree.leaves())

print()
print("Print the noun-verb-noun phrase.")
for subtree in tree.subtrees(filter=lambda t: t.label() == 'P'):
    # print the noun phrase as a list of part-of-speech tagged words
    print(subtree.leaves())


