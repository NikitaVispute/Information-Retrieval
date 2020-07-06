# Author: Nikita Vispute
# Net Id: NXV170005
# CS 6322.001 Information Retrieval
# Homework 1

import re
import operator
import sys
import time
import glob
from nltk.stem import PorterStemmer

#---------------------TOKENIZATION-------------------------------------------------

if(len(sys.argv)!=2):    
    sys.exit("Insufficient arguments, enter the Cranfield path location")
else:
    Cranfield_path = sys.argv[1] + "/*"    #Go to the Cranfield path and then read files one by one
files = glob.glob(Cranfield_path)

def preprocess(rawtext):
    htmltext = re.sub(r'<.*?>', '',rawtext)                         #Remove the SGML tags
    text = re.sub(r'[-/,():?;+^=%#&~$!@*_}{]|[0-9]',' ',htmltext)   #Replaces special characters and digits space
    text = re.sub(r'[^\w\s]','',text)                               #Removes punctutation marks
    text = re.sub(r"\\'s",'',text)                                  #Removes word possessives and contractions 
    text = re.sub(r"\\'",'',text)                                   #Removes apostrophes in words ending with apostrophes  
    cleantext  = re.sub(r"\s+"," ", text)                           #Removes extra spaces
    preptext = cleantext.lower()                                    #Converts all text to lower case
    return preptext

def map_book(tokens):   #creating a map for the tokens by storing the tokens as key and their frequency as its value
    hash_map = {}

    if tokens is not None:
        for word in tokens:
            if word in hash_map:        #if word already exists in map , increment its frequency value by 1
                hash_map[word] = hash_map[word] + 1
            else:                       #if the word does not exist in map, create a new one with frequency 1
                hash_map[word] = 1

        return hash_map
    else:
        return None


tokenonlyonce = 0;            #initialization of counter for tokens that have frequency as only 1
alltokens = []                #initialization of array to store all the tokens in the Cranfield collection 
NumberOfFiles = 0             #initialization of counter for total number of files in the Cranfield collection
totaltokens = 0               #initialization of counter for total number of tokens in the Cranfield collection

start = time.time()           #time at the start of the tokenizer call
    
for file in files:
    NumberOfFiles = NumberOfFiles + 1
    fh = open(file,"r")
    filetext = fh.read()              #read each file from the Cranfield dir and store it in filetext
    fh.close()
    preptext = preprocess(filetext)   #pre-process the filetext by calling the preprocess function
    token_text = preptext.split()     #split the processed text into words/tokens
    alltokens = alltokens + token_text

if NumberOfFiles == 0:
    print('No file found to tokenize,enter correct path')
    sys.exit()

tokens = map_book(alltokens)    #creating a map for alltokens by calling map_book function -> identifying all unique tokens and their frequency
unique = set(tokens)            #all unique tokens in the Cranfield collection

end = time.time()               #time at the end of the tokenizer call

#computing tokenonlyonce counter - tokens having frequency: 1
for uword in tokens:
    totaltokens = totaltokens + tokens[uword]
    if tokens[uword] is 1:        #if frequency of a token is 1, increment the onlyonce counter
        tokenonlyonce = tokenonlyonce+1

#To find frequent tokens
sorted_map = None
sorted_map = sorted(tokens.items(), key=operator.itemgetter(1), reverse=True)

#Average number of words per document
avg_words_doc = round((totaltokens/NumberOfFiles),2)

print("\n##----------------TOKENIZATION---------------------##")
print("\n1. Number of tokens in the Cranfield Text Collection: ",totaltokens)
print("2. Number of unique words in the Cranfield Text Collection:",len(unique))
print("3. Number of words that occur only once in the Cranfield Text Collection:",tokenonlyonce)

print("\n4. 30 most frequent words in the Cranfield Text Collection:")
print ('TOKEN ' +'       \t FREQUENCY')
for i in range(30):
  print (''+sorted_map[i][0]+'       \t '+ '{0:>5}'.format(str(sorted_map[i][1])))
print('\n')

print("Total files tokenized: ", NumberOfFiles)
print ("5. Average number of words per document:" + str(avg_words_doc))
print("\nTime taken to tokenize the Cranfield Text Collection: ", round((end - start),2),"s")

#--------------------STEMMING---------------------------------------------------------
ps = PorterStemmer()
stems = {}
totalstems = 0                #initialization of counter for total number of stems in the Cranfield collection
for w in tokens:    
    stm = ps.stem(w)          #Applying the nltk library Porter Stemmer algorithm to the tokens
    totalstems = totalstems + tokens[w]
    if stm in stems:
        stems[stm] += tokens[w]
    else:
        stems[stm] = tokens[w]

#Computing stems that occur only once (frequency:1)
stemonlyonce = 0              #initialization of counter for tokens that have frequency as only 1
for st in stems:
    if stems[st] == 1:        #if frequency of a stem is 1, increment the stemonlyonce counter
        stemonlyonce += 1

#To find frequent stems
sorted_map = None
sorted_stems = sorted(stems.items(), key=operator.itemgetter(1), reverse=True)

#Average number of stems per document
avg_stems_doc = round((totalstems/NumberOfFiles),2)

print("\n##----------------STEMMING--------------------------------------##")

print("\n1. Number of distinct stems in the Cranfield Text Collection: ",len(stems))
print("2. Number of stems that occur only once in the Cranfield Text Collection: ",stemonlyonce)

print("\n3. 30 most frequent stems in the Cranfield Collection:")
print ('STEM ' +'       \t COUNT')
for i in range(30):
    print (''+sorted_stems[i][0]+'       \t '+ '{0:>5}'.format(str(sorted_stems[i][1])))
print('\n')
print('4. Average Number of stems per document: ', avg_stems_doc)
