#Nikita Vispute
#NET ID: NXV170005
#email: nxv170005@utdallas.edu
#CS6322.001
#Homework 3


import nltk 
import glob
import re
import sys
import collections
from datetime import datetime
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import math

count=0
j=0
token=[]
index=0
ps_lem = {}
ps_stem = {}
lemmas={}
stems={}
lgap={}
sgap={}
delta={}
gamma={}
docmaxtfl=[]
doclst=[]
title = []


tf_lem= defaultdict(int)

qlist=[]

query=""

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


path=sys.argv[1]+'/*'    #path = '/people/cs/s/sanda/cs6322/Cranfield/*'
#queryfile = "hw3.queries"
queryfile = sys.argv[2]
qfile = open(queryfile,"r")   #path = '/people/cs/s/sanda/cs6322/hw3.queries*'
nterms1=0
nterms2=0
avg_dlen = 98

W1_d = {}
W2_d = {}
W1_doc = []
W2_doc = []
temp_token = []
files=glob.glob(path)
start1=datetime.now()
for file in files:
    with open(file, 'r') as f:
        index=index+1
        words=f.read()
        title.append(words[(words.index('<TITLE>') + len('<TITLE>')):words.index('</TITLE>')])
        text = re.sub(r'<.*?>',"", words)   # Removes SGML Tags
        txt = re.sub(r'[,-]'," ", text)     # Removes comma and hyphen, replaces with space
        txt1 = re.sub(r'[^\w\s]','',txt)    # Removes punctuation marks
        res = re.sub(r'[^A-Za-z]'," ",txt1) # Removes numbers and special characters
        res1=res.lower()                    # Lower-case the tokens
        tokens=res1.split()
        doclen = len(tokens)
        doclst.append((index,doclen))
        if (len(tokens) > 0):
            count += len(tokens)

        f_token = [w for w in tokens if w not in stopwords.words('english')]
        temp_token = nltk.pos_tag(f_token)

        #print(index)
        #------------Lemma-------------#
        lemma = WordNetLemmatizer()
        lem=[]
        for ft,tg in temp_token:
            lemmat1 = lemma.lemmatize(ft, get_wordnet_pos(tg)).encode('utf-8')
            lem.append(lemmat1)

        #print(lem)
        lemc = collections.Counter(lem)
        max_tflem = lemc.most_common(1)
        for key, value in max_tflem:
            max_tfl= value
            docmaxtfl.append((index,max_tfl))

        for w, tf in lemc.items():
            W1 = round((0.4 + 0.6 * math.log10(tf + 0.5) / math.log10(max_tfl + 1.0)),3)
            W1_d[w] = W1

            W2 = round((0.4 + 0.6 * (tf / (tf + 0.5 + 1.5 * (doclen / avg_dlen)))),3)
            W2_d[w] = W2

        W1_doc.append(W1_d)
        W2_doc.append(W2_d)

        W1_d = {}
        W2_d = {}

        for t, tf in lemc.items():
            ds = [index, tf, max_tfl, doclen]
            dlist = []
            if t in ps_lem:
                ps_lem[t].append(ds)
            else:
                dlist.append(ds)
                ps_lem[t] = dlist

d= {}
d = collections.OrderedDict(sorted(ps_lem.items()))

N = len(files)
avg_doclen = count / len(files)


qlines = qfile.readlines()
for i in range(len(qlines)):
    if qlines[i].startswith('Q'):
        j=i+1
        while j!=len(qlines) and qlines[j]!="\n":
            query += qlines[j]
            j = j + 1
        qlist.append(query)
        query=""

#print(qlist)
query_list=[]
temp_list=[]
query_lemlist = []
W1_q = {}
W2_q = {}
W1_queries = []
W2_queries = []
W1_cos_sim = {}
W2_cos_sim = {}
qdlist_w1 = []
qdlist_w2 = []
score_list_w1 = []
score_list_w2 = []
score = 0
cos = 0
normal1 = 0
normal2 = 0
for i in range(len(qlist)):
    qtoken=qlist[i]
    qtext = re.sub(r'[,-/]', "", qtoken)
    qwords=qtext.split()

    temp_list = [w for w in qwords if w not in stopwords.words('english')]
    query_list = nltk.pos_tag(temp_list)

    lemma = WordNetLemmatizer()
    qlem = []
    for ql,tag in query_list:
        #wntag=get_wordnet_pos(tag)
        lemmat = lemma.lemmatize(ql, get_wordnet_pos(tag)).encode('utf-8')
        qlem.append(lemmat)
    #query_lemlist.append(qlem)
    #for i in range(len(query_lemlist)):
    q_doclen = len(qlem)
    qterm_cnt = collections.Counter(qlem)
    max_tf_q = max(qterm_cnt.values())
    for qterm, tf in qterm_cnt.items():
        for t, post in d.items():
            if qterm == t:
                q_df = len(post)

        W1 = round((0.4 + 0.6 * math.log10(tf + 0.5) / math.log10(max_tf_q + 1.0)) * (math.log10(N / q_df) / math.log10(N)),3)
        W1_q[qterm] = W1

        W2 = round((0.4 + 0.6 * (tf / (tf + 0.5 + 1.5 * (q_doclen / avg_doclen))) * math.log10(N / q_df) / math.log10(N)),3)
        W2_q[qterm] = W2

    W1_queries.append(W1_q)
    W2_queries.append(W2_q)

    W1_q = {}
    W2_q = {}

for i in range(N):
    for k,v in W1_doc[i].items():
        normal1 += v**2
    normal1 = math.sqrt(normal1)
    for k,v in W1_doc[i].items():
        W1_doc[i][k] = round(v / normal1,3)
    for k,v in W2_doc[i].items():
        normal2 += v**2
    normal2 = math.sqrt(normal2)
    for k,v in W2_doc[i].items():
        W2_doc[i][k] = round(v / normal2,3)

    normal1 = 0
    normal2 = 0

for i in range(len(qlist)):
    for k,v in W1_queries[i].items():
        normal1 += v**2
    normal1 = math.sqrt(normal1)
    for k,v in W1_queries[i].items():
        W1_queries[i][k] = round(v / normal1,3)
    for k,v in W2_queries[i].items():
        normal2 += v**2
    normal2 = math.sqrt(normal2)
    for k,v in W2_queries[i].items():
        W2_queries[i][k] = round(v / normal2,3)

    normal1 = 0
    normal2 = 0

print("\nVector Representation of Queries for Weight-1")
for i in range(len(qlist)):
    print("Q"+str(i+1)+": ",W1_queries[i])

print("\nVector Representation of Queries for Weight-2")
for i in range(len(qlist)):
    print("Q"+str(i+1)+": ",W2_queries[i])

#print(query_lemlist)
print("\n\nThe top 5 documents ranked for the query under both weighting schemes:\n")
for i in range(len(qlist)):
    for j in range(N):
        for k,v in W1_queries[i].items():
            for x,y in W1_doc[j].items():
                if k == x:
                    cos = v * y
            score += cos
        qd = 'Q' + str(i+1) + ',D' + str(j+1)
        W1_cos_sim[qd] = round(score,3)
        score = 0

        for k,v in W2_queries[i].items():
            for x,y in W2_doc[j].items():
                if k == x:
                    cos = v * y
            score += cos
        qd = 'Q' + str(i+1) + ',D' + str(j+1)
        W2_cos_sim[qd] = round(score,3)
        score = 0

    print("W1: ",dict(collections.Counter(W1_cos_sim).most_common(5)))
    qdlist_w1.append(list(dict(collections.Counter(W1_cos_sim).most_common(5)).keys()))
    score_list_w1.append(list(dict(collections.Counter(W1_cos_sim).most_common(5)).values()))
    
    print("W2: ",dict(collections.Counter(W2_cos_sim).most_common(5)))
    qdlist_w2.append(list(dict(collections.Counter(W2_cos_sim).most_common(5)).keys()))
    score_list_w2.append(list(dict(collections.Counter(W2_cos_sim).most_common(5)).values()))

    W1_cos_sim = {}
    W2_cos_sim = {}

print("\n\n")

for i in range(len(qdlist_w1)):
    print("Q" + str(i+1) + " Weight-1 Characteristics:")
    print("Rank\tScore\tDocID\tQueryline")
    for j in range(5):
        qdlist_w1[i][j] = int(qdlist_w1[i][j].split('D')[1]) - 1
        print(str(j+1) + "\t" + str(score_list_w1[i][j]) + "\t" + str(qdlist_w1[i][j] + 1) + "\t" + title[qdlist_w1[i][j]])

for i in range(len(qdlist_w2)):
    print("Q" + str(i+1) + " Weight-2 Characteristics:")
    print("Rank\tScore\tDocID\tQueryline")
    for j in range(5):
        qdlist_w2[i][j] = int(qdlist_w2[i][j].split('D')[1]) - 1
        print(str(j+1) + "\t" + str(score_list_w2[i][j]) + "\t" + str(qdlist_w2[i][j] + 1) + "\t" + title[qdlist_w2[i][j]])

for i in range(len(qdlist_w1)):
    print("Doc Weight-1 vector of Q" + str(i+1))
    for j in range(5):
        print("Doc" + str(qdlist_w1[i][j] + 1) + " Vector Representation")
        print(W1_doc[qdlist_w1[i][j]])
    print("\n\n\n")

for i in range(len(qdlist_w2)):
    print("Doc Weight-2 vector of Q" + str(i+1))
    for j in range(5):
        print("Doc"  + str(qdlist_w2[i][j] + 1) + " Vector Representation")
        print(W2_doc[qdlist_w2[i][j]])
    print("\n\n\n")
    