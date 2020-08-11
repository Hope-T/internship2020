#for parsing numbers
import re
#for deleting file
import os

#nltk
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk import RegexpParser

#delete files that aren't in desired category
#each unneeded ID is in its own list, in the unneeded list,
#so it is f[0]

#BUT, we don't want to delete files belonging to other categories, so
#only delete the files generated with this specific category
def deleteUnneeded(unneeded, category):
	for f in unneeded:
		try:
			os.remove(str(category.strip() + f[0]))
		except OSError as error:
			print("Couldn't find file " + str(f[0]))

def clearFile(toClear):
	open(toClear, 'w').close()

def tagWords(toRead):
	
	#prepare file
	f = open(toRead, 'r')
	raw = f.read()
	raw = word_tokenize(raw)

	#POS-tagging
	raw = pos_tag(raw)
	return raw
	

#find nouns and verbs phrases
def findNV(toRead, category):
	words = tagWords(toRead)

	#find names of new tools (nouns) and verbs
	tools = []
	verbs = []

	for word,POS in words:

		#include all nouns (NN, NNS, NNP, NNPS)
		if POS[0:1] == 'N' and not "CAPEC" in word:
			if not word in tools:
				tools.append(word)

		#include all verbs
		elif POS[0:1] == 'V':
			if not word in verbs:
				verbs.append(word)

	newOutput = open(category.strip() + 'Nouns.txt','a')
	for tool in tools:
		newOutput.write(tool + ", ")

	newOutput.close()

	newOutput = open(category.strip() + 'Verbs.txt', 'a')
	for verb in verbs:
		newOutput.write(verb + ", ")
	newOutput.close()

#compound nouns
def findNounPhrases(toRead, category):
	words = tagWords(toRead)

	#create file
	newFile = open(category.strip() + 'NounPhrases.txt','a')

	#? is include, if it exists
	#* is include it (however many)
	#+ is at least one
	patterns= r"""
 	NP:
     	{<VBD><N.*>+}
     	{<VBG><N.*>+}
     	{<VBN><N.*>+}


	"""
	chunker = RegexpParser(patterns)
	tree = chunker.parse(words)

	#subtree.leaves() returns list
	for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
		newFile.write("\n")
		newFile.write("\n")
		for leaf in subtree.leaves():		
			newFile.write(str(leaf))
  
	newFile.close()

def findNVN(toRead, category):
	words = tagWords(toRead)

	#create file
	newFile = open(category.strip() + 'Phrases.txt','a')

	#? is include, if it exists
	#* is include it (however many)
	#+ is at least one
	patterns= r"""
 	P:{<N.*><V.*><CC?><DT?><N.*>}
   	{<N.*><V.*><N.*>}
   	{<V.*><DT?><N.*>}
	

	"""
	chunker = RegexpParser(patterns)
	tree = chunker.parse(words)

	for subtree in tree.subtrees(filter=lambda t: t.label() == 'P'):
		newFile.write("\n")
		newFile.write("\n")
		for leaf in subtree.leaves():		
			newFile.write(str(leaf))

	newFile.close()

def findTools(toRead, category):
	words = tagWords(toRead)

	#open file
	newFile = open(category.strip() + 'Tools.txt','a')

	#? is include, if it exists
	#* is include it (however many)
	#+ is at least one
	patterns= r"""
	TG: {<N.><JJ><IN><N.*><CC>?<N.?>+}


	"""
	chunker = RegexpParser(patterns)
	tree = chunker.parse(words)

	for subtree in tree.subtrees(filter=lambda t: t.label() == 'TG'):
		newFile.write("\n")
		newFile.write("\n")
		for leaf in subtree.leaves():		
			newFile.write(str(leaf))

	newFile.close()


def parseSpecificText(category):
	IDset = []
	unneeded = []
	#file to read
	text = open('capec-booklit.txt', 'r')

	#keywords that separate each method 
	startingPoint = 'CAPEC-'
	endingPoint = 'Back to top'
	domain = 'Domains of Attack'
	flag = 0

	for line in text:
		if startingPoint in line:
			#each new section begins with CAPEC-xxx:
			if ':' in line:
				flag = 1

				#re.findall() extracts numbers from string
				#puts numbers into list
				myID = re.findall("(\d+)", line)

				#create separate file for the method
				f = open(str(category.strip() + myID[0]),"w+")
		
		
		elif endingPoint in line:
			#reset for next method
			f.close()
			flag = 0
		
		elif flag == 1:
			f.write(line)

			#finding method's domain of attack
			if domain in line:
				if category in line:
					IDset.append(myID)
				else:
					unneeded.append(myID)
				

	text.close()
	deleteUnneeded(unneeded, category)
	
	clearFile(category.strip() + 'Nouns.txt')
	clearFile(category.strip() + 'Verbs.txt')
	clearFile(category.strip() + 'NounPhrases.txt')
	clearFile(category.strip() + 'Phrases.txt')
	clearFile(category.strip() + 'Tools.txt')


	print("There are " + str(len(IDset)) + " attack methods for: " + category)
	print("There are " + str(len(unneeded)) + " attacks that aren't in the domain of: " + category)
	
	

	
	print("Extracting nouns to " +category+ "Nouns.txt and verbs to " + category + "Verbs.txt")
	#only extract from desired category
	for ID in IDset:
		findNV(category.strip()+ID[0], category)

	print("Extracting noun phrases to " + category + "NounPhrases.txt")
	#only extract from desired category
	newFile = open(category + 'NounPhrases.txt','a')
	newFile.write("Noun phrases\n")
	newFile.close()
	for ID in IDset:
		findNounPhrases(category+ID[0], category)

	print("Extracting noun-verb-noun phrases to " + category + "Phrases.txt")
	newFile = open(category + 'Phrases.txt','a')
	newFile.write("Noun-verb-noun phrases\n")
	newFile.close()
	for ID in IDset:
		findNVN(category+ID[0], category)

	print("Extracting tools to " + category + "Tools.txt")
	newFile = open(category + 'Tools.txt','a')
	newFile.write("Tools\n")
	newFile.close()
	for ID in IDset:
		findTools(category+ID[0], category)

	print()
	print("Process complete.")
	
	

#main method
CAPEC_categories = ["Software", "Hardware", "Communications", "Supply Chain", "Social Engineering", "Physical Security"]

for category in CAPEC_categories:
	parseSpecificText(category)




