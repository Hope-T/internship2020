# internship2020
Hone presentation, research, and technical writing skills; 
utilize virtual machines, Ubuntu, and Github; 
code Python programs focusing on natural language processing to explore patterns in documented attack/hacking methods; 
code Python programs to perform association rule mining; 
investigate Protege, DOG4DAG, VOWL, and other ontology tools.

# Before Running
Ensure that python3 and NLTK is installed.
There is extensive documentation in each of the files.

# Running prototypeParseText.py
This file was the basis for the later file, parseText.py.
It tests out various actions on a smaller text file.
It is essentially the exploratory phase, in which I learned how to code in Python and how to use NLTK.
The program focuses on tagging parts of speech.
Please type "python3 prototypeParseText.py" into the terminal.

# Running parseText.py
This file is the previous file, on a large and usable scale.
Tagging the words lets the program extract tools, nouns, compound nouns (labeled as noun phrases), and noun-verb-noun phrases.
Please type "python3 parseText.py" into the terminal.

# Running associations.py
This file focuses on association rule mining.
More specifically, the program calculates the lift and confidence between word A (the target word) and every other word in the file.
The purpose is to see which words have the highest associations with each other.
To run through the entire text file (capec-booklit.txt), go to line 39 and remove the bounds in the for-loop.
The program may take a few minutes to run.
Please type "python3 associations.py" into the terminal.
