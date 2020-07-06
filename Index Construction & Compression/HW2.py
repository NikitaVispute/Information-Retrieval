#NIKITA VISPUTE
#NET ID: NXV170005
#Information Retrieval CS 6322.001
# Homework 2


#import library
import os
import re
import sys
import time
import glob
import nltk
import pickle
nltk.download('stopwords')
from nltk.corpus import stopwords
from _collections import defaultdict
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer    #for lemmatization
from nltk import PorterStemmer                     #for stemming

sys.stdout = open('HW2.txt', 'w')   #open output file 

if(len(sys.argv)!=2):    
    sys.exit("Insufficient arguments, enter the Cranfield path location")
else:
    Cranfield_path = sys.argv[1] + "/*"    #Go to the Cranfield path and then read files one by one
files = glob.glob(Cranfield_path)

def preprocess(rawtext):
    htmltext = re.sub(r'<.*?>', '',rawtext)                         #Remove the SGML tags
    text = re.sub(r'[-/,():?;+^=%#&~$!@*_}{]|[0-9]',' ',htmltext)   #Replaces special characters and digits space
    text = re.sub(r'[^\w\s]','',text)                               #Removes punctuation marks
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

def Tokenize(file):
    fh=open(file,"r")
    filetext = fh.read()
    fh.close()
    preptext = preprocess(filetext)
    tokentext = preptext.split()     #split the processed text into words/tokens
    return tokentext
    	
class IndexEntry:           #initializing Index entries
    def __init__(self, term, docfrequency, termfrequency, post_list):
        self.term = term
        self.docfreq = 	docfrequency
        self.totTermFreq = termfrequency
        self.postingList = 	post_list

class PostingList:  #initializing postings lists entries
    def __init__(self,docid,freq,maxTermFreq,doclen):
        self.docId = docid
        self.termFreq = freq
        self.maxTermFreq = maxTermFreq
        self.docLen = doclen 
    def __iter__(self):
        return self.__dict__.iteritems()
	
def getMaxTermFreqDocLen(dictf):            
    docLen = 0                              #the total number of word occurrences in the document        
    maxTermFreq = 0                         #the frequency of the most frequent term or stem in that document
    for items in dictf:
        termFreq = dictf[items]
        docLen += termFreq
        if not items in stopwords:
            if termFreq > maxTermFreq:
                maxTermFreq = termFreq
    return maxTermFreq,docLen	
	
class CreateIndex():                
    def __init__(self):
    	self.dictionary = {}	
    def insertindex(self,docId, token, termFreq, maxTermFreq, docLen):
        entry = self.dictionary.get(token)
        if entry is None:
            postingList = []
            entry = IndexEntry(token,0,0,postingList)
            self.dictionary[token] = entry       			
        entry.docfreq +=1
        postEntry = PostingList(docId,termFreq,maxTermFreq,docLen)
        entry.postingList.append(postEntry)
        entry.totTermFreq+= termFreq		
        
UnComp_IndexVersion1 = CreateIndex()
Uncomp_IndexVersion2 = CreateIndex()

stopwords = set(stopwords.words('english'))             #using the stopwords from the nltk library

      
def GenerateLemmas():        
        lematizer = WordNetLemmatizer()
        docid = 0
        for file in files:
            docid = docid + 1	
            dictWord = {}        
            listOfWords = Tokenize(file)
            for word in listOfWords:
                tWord = lematizer.lemmatize(word)
                dictWord[tWord] = dictWord.get(tWord,0)+ 1
        
            mxtf, dolen = getMaxTermFreqDocLen(dictWord)
            for items in dictWord:
                termFreq = dictWord[items]
                if not items in stopwords :    
                    UnComp_IndexVersion1.insertindex(docid,items,termFreq,mxtf,dolen)
        del dictWord
        
def GenerateStems():
    stmr = PorterStemmer()
    docid = 0
    for file in files:
        docid = docid + 1
        listOfStemWords = Tokenize(file)    
        stemWord = {}        
        for w in listOfStemWords:
            tempStem = stmr.stem(w) 
            stemWord[tempStem]= stemWord.get(tempStem,0)+1
        
        mxtf, dolen = getMaxTermFreqDocLen(stemWord)
        
        for items in stemWord:
            termFreq = stemWord[items]    
            if not items in stopwords :    
                Uncomp_IndexVersion2.insertindex(docid,items,termFreq,mxtf,dolen)
        
        del stemWord

startLemma = time.time()
GenerateLemmas()
endLemma = time.time()
print("Time taken to create uncompressed Index Version 1 using lemmas "+str(endLemma-startLemma))


startstems = time.time()
GenerateStems()
endstems = time.time()
print("Time taken to create uncompressed Index Version 2 using stems "+str(endstems-startstems))      

print("\n\n####################################################################################################################")               	

print ("\nDictionary of Lemmas (Max 3 postings lists per term displayed)")
print ('\n\n{0:15}  {1:20}'.format("Lemma","Doc-freq")+" PostingList (DocID, TF, Max_tf, Doc_len)  ")
for Lemma in sorted(UnComp_IndexVersion1.dictionary):
    entry = UnComp_IndexVersion1.dictionary.get(Lemma)
    df = entry.docfreq
    sys.stdout.write ("\n"+'{0:15}  {1:20}'.format(Lemma,str(df)),)
    for dlist in entry.postingList[:3]:
        n_docid = dlist.docId
        n_tf = dlist.termFreq
        n_max_tf = dlist.maxTermFreq
        n_len = dlist.docLen        
        sys.stdout.write("("+str(n_docid)+","+str(n_tf)+","+str(n_max_tf)+","+str(n_len)+")",)

print("\n\n####################################################################################################################") 
    
print ("\n\nDictionary of Stems (Max 3 postings lists per term displayed)")
print ('{0:15}  {1:20}'.format("Stems","Doc-freq")+" PostingList (DocID, TF, Max_tf, Doc_len) ")
for stem in sorted(Uncomp_IndexVersion2.dictionary):
    entry = Uncomp_IndexVersion2.dictionary.get(stem)
    df = entry.docfreq   
    sys.stdout.write ("\n"+'{0:15}  {1:20}'.format(stem,str(df)),)
    for dlist in entry.postingList[:3]:
        n_docid = dlist.docId
        n_tf = dlist.termFreq
        n_max_tf = dlist.maxTermFreq
        n_len = dlist.docLen        
        sys.stdout.write ("("+str(n_docid)+","+str(n_tf)+","+str(n_max_tf)+","+str(n_len)+")",)  
        
print("\n\n####################################################################################################################")

    
with open('Index_Version1.uncompress', 'wb') as outfile1:
    pickle.dump(UnComp_IndexVersion1.dictionary, outfile1, pickle.HIGHEST_PROTOCOL)
    
with open('Index_Version2.uncompress', 'wb') as outfile2:
    pickle.dump(Uncomp_IndexVersion2.dictionary, outfile2, pickle.HIGHEST_PROTOCOL)   


class CompressedIndex:
    def __init__(self, dictionary, isBlock):
        self.k = 4
        self.dictionaryString = ""
        self.termFreqBlock = {}
        self.docFreqBlock = {}
        self.gammaEncodingList = []
        self.termFreqBlock = {}
        self.docFreqBlock = {}
        self.tempIndexList = []
        self.blockedCompress = defaultdict()
        self.frontCodingCompress = defaultdict()
        if (isBlock):
            self.BlockedCompression(dictionary)
        else:
            self.FrontCoding(dictionary)
            
        
    def CalculateUnaryCode(self, length):
        unaryValue = ""
        for i in range(0,length):
            unaryValue += str(1)
        return unaryValue + str(0)
	  
    def CalculateGammaCode(self, num):
        binaryRep = str(bin(num))[2:]
        offset = binaryRep[1:]
        unaryValue = self.CalculateUnaryCode(len(offset))
        gammaCode = unaryValue + offset
        return gammaCode
    
    def CalculateDeltaCode(self, num):
        binaryRep = str(bin(num))[2:]
        gammaCode = self.CalculateGammaCode(len(binaryRep))
        offset = binaryRep[1:]
        deltaCode = gammaCode + offset
        return deltaCode


    #store dictionary as a string 
    #Each term is preceded by a byte encoding its length that indicates how many bytes to skip to reach subsequent terms.
    #BlockedStorage: compress the dictionary by grouping terms in the string into of size k
    #and keeping a term pointer only for the first term of each block 
    def CompressPostingList(self, indexEntry):        
        prevDocId = 0
        for entry in indexEntry.postingList:
            gap = entry.docId - prevDocId
            gammaCode = self.CalculateGammaCode(gap)
            self.gammaEncodingList.append(gammaCode)
            prevDocId = entry.docId
                    		
    def BlockedCompression(self, dictionary):
        blocksize = self.k		
        for i,term in enumerate(sorted(dictionary.keys())):
            if blocksize != 0:
                self.dictionaryString += str(len(term)) + term
                entry = dictionary.get(term)
                self.CompressPostingList(entry)				
                self.termFreqBlock[blocksize] = self.CalculateGammaCode(entry.totTermFreq)
                self.docFreqBlock[blocksize] = self.CalculateGammaCode(entry.docfreq)
                self.blocksize = blocksize - 1
							 
            if blocksize == 0 or i == len(dictionary)-1:
                self.tempIndexList.append(self.gammaEncodingList)
                self.tempIndexList.append(self.termFreqBlock)
                self.tempIndexList.append(self.docFreqBlock)
                self.blockedCompress[self.dictionaryString] = self.tempIndexList 
                self.dictionaryString = ""
                self.tempIndexList = []
                self.gammaEncodingList = []
                self.termFreqBlock = {}
                self.docFreqBlock = {}

    def commonPrefix(self,m):
        s1 = min(m)
        s2 = max(m)
        for i, c in enumerate(s1):
            if c != s2[i]:
                return s1[:i]
        return s1

    def FrontCoding(self, dictionary):
        k=8
        count=0
        code = ""
        comPref = ""
        termFreqList = {}
        deltaEncodingList = []
        freqencodingList = []
        docFreqBlock = {}
        termList= []
        tempIndexList = []
               
        for i,term in enumerate(sorted(Uncomp_IndexVersion2.dictionary.keys())):
            if count < k:
                termList.append(term)
                count += 1
            
            if count == k or i == len(Uncomp_IndexVersion2.dictionary)-1 :    
                comPref = self.commonPrefix(termList)
                if comPref:
                    code += "["
                    for j,word in enumerate(termList):
                        if word.startswith(comPref):
                            if j == 0:
                                code += str(len(word)) + comPref + "*" + word[len(comPref):]
                            if j > 0:
                                code += str(len(word[len(comPref):])) + "$" + word[len(comPref):]                 
                        else:
                            if j == 0:
                                code += str(len(word)) + comPref + "*" +  word[:]
                            if j > 0:
                                code += str(len(word[:])) + "$" + word[:]
                        
                        entry = Uncomp_IndexVersion2.dictionary.get(word)
                        prevId = 0
                        pEntry = PostingList(0,0,0,0)
                        
                        for Entry in entry.postingList:
                            docId = self.CalculateGammaCode(pEntry.docId - prevId)
                            deltaEncodingList.append(docId)
                            prevId = pEntry.docId
                            freqencodingList.append(pEntry.termFreq)
                            freqencodingList.append(pEntry.docLen)
                            freqencodingList.append(pEntry.maxTermFreq)
                    
                        termFreqList[j] = self.CalculateDeltaCode(entry.totTermFreq)
                        docFreqBlock[j] = self.CalculateDeltaCode(entry.docfreq)
                   
                    code += "]"
                    tempIndexList.append(deltaEncodingList) 
                    tempIndexList.append(termFreqList)
                    tempIndexList.append(docFreqBlock)
                    tempIndexList.append(freqencodingList)
                    self.frontCodingCompress[code] = tempIndexList 
                    count=0
                    deltaEncodingList = []
                    termFreqList = {}
                    docFreqBlock = {}
                    code = ""
                    tempIndexList = []
                    termList = []
                    
        return  

isBlock = 1;
starttime = time.time()
CompressedIndex_Version1 = CompressedIndex(UnComp_IndexVersion1.dictionary,isBlock)
endtime = time.time()

print("\nTime taken to create compressed Index Version 1 using lemmas: "+str(endtime-starttime))

with open('Index_Version1.compressed', 'wb') as outfile3:
    pickle.dump(CompressedIndex_Version1.blockedCompress, outfile3, pickle.HIGHEST_PROTOCOL)
    
isBlock = 0;
starttime = time.time()
CompressedIndex_Version2 = CompressedIndex(Uncomp_IndexVersion2.dictionary,isBlock)
endtime = time.time()

print("Time taken to create compressed Index Version 2 using stems "+str(endtime-starttime))

with open('Index_Version2.compressed', 'wb') as outfile4:
    pickle.dump(CompressedIndex_Version2.frontCodingCompress, outfile4, pickle.HIGHEST_PROTOCOL)

print("\n\n##########################################################################################################")  
  
print ("Size of the Index version 1 uncompressed (in bytes): " + str(os.path.getsize("Index_Version1.uncompress")))
print ("Size of the Index version 2 uncompressed (in bytes): " + str(os.path.getsize("Index_Version2.uncompress")))
print ("Size of the Index version 1 compressed (in bytes): " + str(os.path.getsize("Index_Version1.compressed")))
print ("Size of the Index version 2 compressed (in bytes): " + str(os.path.getsize("Index_Version2.compressed")))


print("\n\n##########################################################################################################")

print ("\nNumber of inverted lists in Index version 1: " + str(len(UnComp_IndexVersion1.dictionary)))
print ("\nNumber of inverted lists in Index version 2: " + str(len(Uncomp_IndexVersion2.dictionary)))  

print("\n\n##########################################################################################################")

questionwords = ["Reynolds", "NASA", "Prandtl", "flow", "pressure", "boundary", "shock"]
print ('\n{0:7}  {1:7}  {2:7}  {3:7}'.format("Term ","Document-Frequency ","Total-Term-Freq ","Inverted List Length"))
for word in questionwords:
    stmr = PorterStemmer()
    word = word.lower()
    tempStem = stmr.stem(word)    
    entry = Uncomp_IndexVersion2.dictionary.get(tempStem)
    print('{0:15}  {1:15}  {2:15}  {3:37}'.format(word,str(entry.docfreq),str(entry.totTermFreq),str(sys.getsizeof(entry.postingList)))) 
    
print("\n\n############################################################################################################") 
  
print ('\n{0:10}  {1:15}'.format("Term","Document-Frequency"))
entry = Uncomp_IndexVersion2.dictionary.get("nasa")
df = entry.docfreq
print ('{0:10}  {1:15}'.format("nasa",str(df)))
print ("Posting Lists of NASA:")
print ('{0:10}  {1:15}  {2:15}  {3:15}'.format("Doc-ID","Term-Freq", "Max-Term","Doc Len"))
for dlist in entry.postingList[:3]:
    number_of_docid = dlist.docId
    term_freq = dlist.termFreq
    maxTermFreq = dlist.maxTermFreq
    ttf = entry.totTermFreq
    doclen = dlist.docLen
    print ('{0:10}  {1:15}  {2:15}  {3:15}'.format(str(number_of_docid),str(term_freq),str(maxTermFreq),str(doclen)))

print("\n\n############################################################################################################")    

print ("\nTerm with the largest df from index 1 ")
maxDF = 0
MaxDfTermList = []
for entry in UnComp_IndexVersion1.dictionary:
  dictEntry = UnComp_IndexVersion1.dictionary[entry]
  if (dictEntry.docfreq == maxDF):
    MaxDfTermList.append(entry)
  elif (dictEntry.docfreq > maxDF):
    MaxDfTermList = [entry]
    maxDF = dictEntry.docfreq
print ('Largest DF terms from index 1')
print ('Freq : '+ str(maxDF) +'\nTerm : ' + str(MaxDfTermList) + '\n')

print("\n\n############################################################################################################") 

print ("\nTerm with the smallest df from index 1 ")
minDF = 100
MinDfTermList = []
for entry in UnComp_IndexVersion1.dictionary:
  dictEntry = UnComp_IndexVersion1.dictionary[entry]
  if (dictEntry.docfreq == minDF):
    MinDfTermList.append(entry)
  elif (dictEntry.docfreq < minDF):
    MinDfTermList = [entry]
    minDF = dictEntry.docfreq
print ('Smallest DF terms from index 1')
print ('Freq : '+ str(minDF) +'\nTerm : ' + str(MinDfTermList) + '\n')

print("\n\n############################################################################################################") 

print ("\nStem with the largest df from index 2 ")
maxDF = 0
MaxDfTermList = []
for entry in Uncomp_IndexVersion2.dictionary:
  dictEntry = Uncomp_IndexVersion2.dictionary[entry]
  if (dictEntry.docfreq == maxDF):
    MaxDfTermList.append(entry)
  elif (dictEntry.docfreq > maxDF):
    MaxDfTermList = [entry]
    maxDF = dictEntry.docfreq
print ('Largest DF terms from index 2')
print ('Freq : '+ str(maxDF) +'\nTerm : ' + str(MaxDfTermList) + '\n')

print("\n\n############################################################################################################") 

print ("\nStem with the smallest df from index 2 ")
minDF = 100
MinDfTermList = []
for entry in Uncomp_IndexVersion2.dictionary:
  dictEntry = Uncomp_IndexVersion2.dictionary[entry]
  if (dictEntry.docfreq == minDF):
    MinDfTermList.append(entry)
  elif (dictEntry.docfreq < minDF):
    MinDfTermList = [entry]
    minDF = dictEntry.docfreq
print ('Smallest DF terms from index 2')
print ('Freq : '+ str(minDF) +'\nTerm : ' + str(MinDfTermList) + '\n')

print("\n\n############################################################################################################") 

print ("\nLargest Max Frequency Document is:")
largestMax_Tf=0
docId=0
maxTermFreq=0
for term in UnComp_IndexVersion1.dictionary.keys():
    entry = UnComp_IndexVersion1.dictionary.get(term)
    for pEntry in entry.postingList:
        if pEntry.maxTermFreq > largestMax_Tf:
            largestMax_Tf = pEntry.maxTermFreq

for term in UnComp_IndexVersion1.dictionary.keys():
    entry = UnComp_IndexVersion1.dictionary.get(term)
    for pEntry in entry.postingList:
        if pEntry.maxTermFreq == largestMax_Tf:                        
            docId = pEntry.docId
            maxTermFreq = pEntry.maxTermFreq
            
print ("Cranfield0" +str(docId) + " - " + str(maxTermFreq))  


print("\n\n############################################################################################################") 

print ("\nDocument with largest doc-len in collection:")      
doc=0
docId=0
maxDocLen=0
for term in UnComp_IndexVersion1.dictionary.keys():
    entry = UnComp_IndexVersion1.dictionary.get(term)
    for pEntry in entry.postingList:
        if pEntry.docLen > doc:
           doc = pEntry.docLen
for term in UnComp_IndexVersion1.dictionary.keys():
    entry = UnComp_IndexVersion1.dictionary.get(term)
    for pEntry in entry.postingList:
        if pEntry.docLen == doc:            
           docId = pEntry.docId
           maxDocLen = pEntry.docLen
           
print ("Cranfield0" +str(docId) + " - " + str(maxDocLen)) 

print("\n\n############################################################################################################")                  								
sys.stdout.close()
