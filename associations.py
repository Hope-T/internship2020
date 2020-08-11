import nltk
from nltk.text import Text 
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

def findTopTen(top_ten, val, wordB):
	if len(top_ten) <= 10:
		top_ten.append([wordB, val])
	else:
		top_ten_values = ([row[1] for row in top_ten])
		toReplace = min(top_ten_values) 
		myIndex = top_ten_values.index(toReplace)
		top_ten[myIndex] = [wordB, val]
	
	return top_ten

def findAssociation(targetWord, pluralForm, text_analysis, filtered):
	#setup
	targetWordFreq = text_analysis[targetWord]
	totalWords = len(filtered)

	#find "support"
	print("Find support of: " + targetWord.upper())
	print("'Support' is the number of the target word divided by the number of words.")
	print("What is the percentage of the target word in the text?")
	targetSupport = targetWordFreq/totalWords
	print(targetSupport)
	print()

	#find confidence and lift between targetWord and every other word
	#initialize seenWords with "capec" because it occurs frequently
	#but isn't helpful

	seenWords = ["capec"]
	top_ten_conf = []
	top_ten_lift = []

	for word in filtered[0:100]:
		#shouldn't compare the targetWord to itself,
		#have seen the word B before,
		#and word B should be a noun

		#extract part of speech
		isNoun = nltk.pos_tag(tokenizer.tokenize(word))
		isNoun = isNoun[0][1]
		#extract first letter
		isNoun = isNoun[0:1]
		isNoun = "N" == isNoun

		notSameAsTarget = word != targetWord
		notSeenBefore = not word in seenWords
		notPluralForm = word != pluralForm
		
		if notSameAsTarget and isNoun and notSeenBefore and notPluralForm:
			wordB = word
			seenWords.append(wordB)
		
			#targetWord in n broadens scope to plural
			#find index of each targetWord occurrence
			indices = [i for i, n in enumerate(filtered) if targetWord in n]
			surroundingWords = []

			#for every time we see the targetWord, we'll take
			#an arbitrary number of words before and after it
			for index in indices:
				myChunk = []
				startingIndex = index - 5
				endingIndex = index + 6

				for i in range(startingIndex, endingIndex):
					if i >= 0 and i <= len(filtered):
						myChunk.append(filtered[i])

				surroundingWords.append(myChunk)


			#find "confidence" 
			#(Both (A and B))/(only A)
			count_of_AB = 0
		
			for chunk in surroundingWords:
				#find number of times word A, B are together
				if wordB in chunk:
					count_of_AB = count_of_AB + 1

			confidence_A_B = count_of_AB/targetWordFreq
			
			top_ten_confs = findTopTen(top_ten_conf, confidence_A_B, wordB)
			
			#"lift"
			#(Confidence (A→B))/(Support (B))
		
			#support (B)
			freq_word_B = text_analysis[wordB]
			supportB = freq_word_B/totalWords
		
			#lift
			lift = confidence_A_B/supportB

			top_ten_lift = findTopTen(top_ten_lift,lift, wordB)

	#alphabetize (sort by value instead?)
	top_ten_conf.sort()
	top_ten_lift.sort()

	print("Top Ten Confidence Numbers: ")
	print("'Confidence' is the likelihood that the words appear together.")
	for word, conf in top_ten_conf:
		print(word + " " + str(conf))
	print()
	print("Top Ten Lift Numbers: ")
	print("Seeing the words together is x.xx times more likely than seeing word B alone.")
	for word, lift in top_ten_lift:
		print(word + " " + str(lift))
	print()
	

#process file, convert to nltk object
f = open('capec-booklit.txt', 'r')
raw = f.read()

#NLTK doesn't get rid of correct stopwords unless it is lowercase
#NLTK is case-sensitive
raw = raw.lower()
#tokenize
tokenizer = nltk.RegexpTokenizer(r"\w+")
words = Text(tokenizer.tokenize(raw))

#remove stopwords ("the," "and," "a," etc.)
#stopwords are the most frequently occurring words, which isn't helpful
stop_words = set(stopwords.words('english')) 
filtered = [w for w in words if not w in stop_words]

#get the freq of the remaining words
text_analysis = FreqDist(filtered)

#results
print("Only looking at first 100 words--otherwise, the program takes a long time")
print("To traverse the entire file, remove the bounds [0:100] on line 39")
print()
findAssociation("connection", "connections", text_analysis, filtered)
findAssociation("host", "hosts", text_analysis, filtered)









