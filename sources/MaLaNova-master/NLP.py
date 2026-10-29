
from WordLength import *
from Palindromes import *
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
import xml.dom.minidom
from nltk.corpus import udhr
import re
import random
from nltk import word_tokenize
import numpy as np
import unicodedata
import os
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

#THIS FUNCTION STRIPS AN INPUT TEXT FILE OF ANY NUMBER AND PUNTUACTION

def strip_nochar(file):
   typefile = open(file, "rt", encoding="utf-8")
   typefile = typefile.read()
   strippedstring = re.sub(r'[^\w\s]', '', typefile)
   strippedstring = re.sub("(\s\d+)","", strippedstring) 
   #outfile = "strippednochar"+str(file)
   with open(file, "w",  encoding="utf-8") as f:  
        f.write(strippedstring)

#THIS FUNCTION STRIPS A STRING OF ANY DIACRITICS SIGNS

def strip_accents(file):
   typefile = open(file, "rt", encoding="utf-8")
   typefile = typefile.read()
   strippedstring = ''.join(c for c in unicodedata.normalize('NFD', typefile)
                  if unicodedata.category(c) != 'Mn')
   #outfile = "stripped"+str(file)
   with open(file, "w",  encoding="utf-8") as f:  
        f.write(strippedstring)

#THIS FUNCTION REMOVES ALL SPACES FROM A FILE

def scrcont(file, filedir):
   typefile = open(file, "rt", encoding="utf-8")
   typefile = typefile.read()
   newdir = os.path.join(filedir, "scrcont"+str(file).replace('C:\\Users\\Palma\\Desktop\\MariaLaNova\\oldhungariancorpus\\','')) 
   with open(newdir, "w",  encoding="utf-8") as f:  
       for line in typefile:
            f.write(line.replace(' ', ''))
 
#THIS SMALL FUNCTION REMOVES ALL SPACES IN AN INPUT TEXT OUTPUTTING THE TRIMMED STRING

def RemoveSpaces(epigraph):
    epigraph = open(epigraph, "rt", encoding="utf-8")
    epigraph = epigraph.read()
    trimmedString = epigraph.replace(' ', '').replace('\n','').replace('\t','')
    print(trimmedString)

#THIS FUNCTION ITERATES OVER ALL FILES IN A DIRECTORY AND STRIP IT OF ALL UNWANTED DIACRITICS SIGNS:
#IT ALSO REMOVE ALL SPACES

def cleandirectory(directory, cont = True):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            strip_accents(f)
            strip_nochar(f)
            if cont == True:
                scrcont(f, 'C:\\Users\\Palma\\Desktop\\MariaLaNova\\oldhungariancorpus\\oldhungariancleancont')
            else:
                filedir = 'C:\\Users\\Palma\\Desktop\\MariaLaNova\\oldhungariancorpus\\oldhungarianclean'
                typefile = open(f, "rt", encoding="utf-8")
                typefile = typefile.read()
                newdir = os.path.join(filedir, "clean"+str(f).replace('C:\\Users\\Palma\\Desktop\\MariaLaNova\\oldhungariancorpus\\','')) 
                with open(newdir, "w",  encoding="utf-8") as f:  
                    for line in typefile:
                        f.write(line)
            

#THIS FUNCTION GENERATES AN ARRAY OF CHARACTER FREQUENCY SORTED DESCENT

def charsfreq(file):
    typefile = open(file, "rt", encoding="utf-8")
    typefile = typefile.read()
    res = {}
    for keys in typefile:
        if re.match(r'[^\W\d_]',keys):
            res[keys] = res.get(keys, 0) + 1
    # printing result 
    print ("Count of all characters in file is : \n" +  str(res))
    sort = sorted(res.values(), reverse=True)
    summa = sum(sort)
    print(summa)
    print(sort)
    return sort

#THIS FUNCTION TAKES TWO ARRAYS AS INPUT AND NORMALIZE THEM
#UNDER "NORMALIZATION" HERE IS INTENDED EVENING THEM TO MAKE THEM STATISTICALLY COMPARABLE
#THE APPLIED HEURISTICS IS MULTIPLYING ALL THE THE ELEMENTS OF THE SMALLER ONE BY THE QUOTIENT OF THE FIRST ELEMENTS OF EACH

def normalizeranks(arr1, arr2):
    if arr1[0]> arr2[0]:
        quot = float(arr1[0]/arr2[0])
        arr3 = np.multiply(arr2, quot)
        arr2=arr3
    else:
        quot = float(arr2[0]/arr1[0])
        arr3 = np.multiply(arr1, quot)
        arr1=arr3
    #print(arr1)
    #print(arr2)
    print(str(arr1)+str(arr2))
    #return arr3
    return arr1, arr2

# WITH THIS FUNCTION, THE ARRAYS´ DIMENSIONS ARE EQUALIZED (THE LONGER ONE IS CHOPPED)
def normalizelen(arr1, arr2):
    if len(arr1) > len(arr2):
        pop = len(arr1) - len(arr2)
        arr1 = arr1[ : -pop]
    else:
        pop = len(arr2) - len(arr1)
        arr2 = arr2[ : -pop]
    print(str(arr1)+str(arr2))
   #return bigger
    return arr1, arr2

#THIS FUNCTION SELECTS A DEFINED NUMBER OF RANDOM CHARACTERS IN A TEXT FILE 

def randomfilestring(file, len):
    with open(file,  "rt",  encoding="utf-8") as f:
        content = f.read()
        tokens = word_tokenize(content)
        #content = content.split()
        i = 0
        password = ""
        while i < len:
            random_character = random.choice(content)
            if re.search(r'[^\W\d_]', random_character):
                password += random_character
                i +=1
    print(password)
    outfile = "password"+str(file)
    with open(outfile, "w",  encoding="utf-8") as f:  
        f.write(password)
    return password

#THIS FUNCTION TAKES A TEXT FILE AND RETURN A LIST OF TYPES
def extracTypes(file):
    typefile = open(file, "rt", encoding="utf-8")
    typefile = typefile.read()
    typefile = typefile.split()
    typefile = set(list(typefile))
    print(typefile)

#THIS FUNCTION PRODUCES A LIST OF DIPHTONGS AND RELATED FREQUENCY
def dittonghifr(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    dyphmap = {}
    if file == "latincorpus.txt":
        outfile = "dittonghilat.txt"
    elif file == "greekcorpus.txt":
        outfile = "dittonghigre.txt"
    elif file == "stringaoriginale.txt":
        outfile = "dittonghiorig.txt"
    elif file == "czc.txt":
        outfile = "dittonghiczc.txt"
    elif file == "hng.txt":
        outfile = "dittonghihng.txt"
    elif file == "bohemian.txt":
        outfile = "dittonghibohem.txt"
    else:
        outfile = "dittonghifrequency"+str(file).replace(".txt","")+".txt"
    for word in infile:
        i=0
        while i < len(word) - 1:
            dyph = word[i] + word[i+1]
            if dyph not in dyphmap:
                dyphmap.update({dyph: 1})
            else:
                dyphmap[dyph] += 1 
            i += 1
    dyphmap = dict(sorted(dyphmap.items(), key=lambda item: item[1]))
    print(dyphmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in dyphmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION GENERATES A DOCUMENT WHICH IS THE INPUT  BACKWARDS
def dokuback(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    outfile = "backwards"+str(file).replace(".txt","")+".txt"
    with open(outfile, "wt",  encoding="utf-8") as b: 
        b.write(infile[::-1])

#THIS FUNCTION RETURNS A BACKWARDS DIPHTONGS LIST OF FREQUENCIES -  THE FILE IS PROCESSED STARTING FROM THE BOTTOM

def bigramsfrback(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    dyphmap = {}
    outfile = "bigramsback"+ str(file)
    #if file == "latincorpus.txt":
    #    outfile = "dittonghilat.txt"
    #elif file == "greekcorpus.txt":
    #    outfile = "dittonghigre.txt"
    #elif file == "stringaoriginale.txt":
    #    outfile = "dittonghiorig.txt"
    #elif file == "czc.txt":
    #    outfile = "dittonghiczc.txt"
    #elif file == "hng.txt":
    #    outfile = "dittonghihng.txt"
    #elif file == "bohemian.txt":
    #    outfile = "dittonghibohem.txt"
    #else:
    #    outfile = "dittonghifrequency"+str(file).replace(".txt","")+".txt"
    for word in infile:
        i= len(word) - 1
        while i > 0:
            dyph = word[i] + word[i-1]
            if dyph not in dyphmap:
                dyphmap.update({dyph: 1})
            else:
                dyphmap[dyph] += 1 
            i -= 1
    dyphmap = dict(sorted(dyphmap.items(), key=lambda item: item[1]))
    print(dyphmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in dyphmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION TAKES A TEXT FILE AS INPUT AND OUTPUTS A LIST OF ALL DIPHTHONGS WITH THE WORD POSITION THEY APPEAR IN
def bigramspos(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    dyphmap = {}
    outfile = "bigramspos"+ str(file)
    #if file == "latincorpus.txt":
    #    outfile = "dittonghilatpos.txt"
    #elif file == "greekcorpus.txt":
    #    outfile = "dittonghigrepos.txt"
    #else:
    #    outfile = "dittonghiorigpos.txt"
    for word in infile:
        i=0
        while i < len(word) - 1:
            dyph = word[i] + word[i+1]
            if dyph not in dyphmap:
                dyphmap.update({dyph: str(i) + '/' +  str(len(word) - 1)})
            else:
                dyphmap[dyph] =  str(dyphmap[dyph]) + '-' + str(i) + '/' +  str(len(word) - 1)
            i += 1
    #dyphmap = dict(sorted(dyphmap.items(), key=lambda item: item[1]))
    print(dyphmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in dyphmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION PRODUCES A LIST OF 3-grams AND RELATED FREQUENCY
def trigramsfr(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    triphmap = {}
    outfile = "trigrams"+ str(file)
    #if file == "latincorpus.txt":
    #    outfile = "trittonghilat.txt"
    #elif file == "greekcorpus.txt":
    #    outfile = "trittonghigre.txt"
    #else:
    #    outfile = "trittonghifrequency"+str(file).replace(".txt","")+".txt"
    for word in infile:
        i=0
        while i < len(word) - 2:
            triph = word[i] + word[i+1] + word[i+2]
            if triph not in triphmap:
                triphmap.update({triph: 1})
            else:
                triphmap[triph] += 1 
            i += 1
    triphmap = dict(sorted(triphmap.items(), key=lambda item: item[1]))
    print(triphmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in triphmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION PRODUCES A LIST OF 4-grams AND RELATED FREQUENCY
def fourgramsfr(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    fourmap = {}
    outfile = "fourgrams"+ str(file)
    for word in infile:
        i=0
        while i < len(word) - 3:
            four = word[i] + word[i+1] + word[i+2] + word[i+3]
            if four not in fourmap:
                fourmap.update({four: 1})
            else:
                fourmap[four] += 1 
            i += 1
    fourmap = dict(sorted(fourmap.items(), key=lambda item: item[1]))
    print(fourmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in fourmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION PRODUCES A LIST OF THRIPHTONGS AND RELATED FREQUENCY OF A FILE READ BACKWARDS

def trigramsfrback(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    triphmap = {}
    if file == "latincorpus.txt":
        outfile = "trigramslat.txt"
    elif file == "greekcorpus.txt":
        outfile = "trigramsgre.txt"
    else:
        outfile = "trigramsfrequencyback"+str(file).replace(".txt","")+".txt"
    for word in infile:
        i=len(word) - 2
        while i > 0:
            triph = word[i] + word[i-1] + word[i-2]
            if triph not in triphmap:
                triphmap.update({triph: 1})
            else:
                triphmap[triph] += 1 
            i -= 1
    triphmap = dict(sorted(triphmap.items(), key=lambda item: item[1]))
    print(triphmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in triphmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION TAKES A TEXT FILE AS INPUT AND OUTPUTS A LIST OF ALL TRIPHTHONGS WITH THE WORD POSITION THEY APPEAR IN
def trigramspos(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    tryphmap = {}
    if file == "latincorpus.txt":
        outfile = "trigramslatpos.txt"
    elif file == "greekcorpus.txt":
        outfile = "trigramsgrepos.txt"
    else:
        outfile = "trigramsgpos"+ str(file)
    for word in infile:
        i=0
        while i < len(word) - 2:
            tryph = word[i] + word[i+1] + word[i+2]
            if tryph not in tryphmap:
                tryphmap.update({tryph: str(i) + '/' +  str(len(word) - 1)})
            else:
                tryphmap[tryph] =  str(tryphmap[tryph]) + '-' + str(i) + '/' +  str(len(word) - 1)
            i += 1
    #dyphmap = dict(sorted(dyphmap.items(), key=lambda item: item[1]))
    print(tryphmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in tryphmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION TAKES A TEXT FILE AS INPUT AND OUTPUTS A LIST OF ALL SUFFIX TRIPHTHONGS 
def trigramssuff(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    suffmap = {}
    if file == "latincorpus.txt":
        outfile = "trigramslatsuff.txt"
    elif file == "greekcorpus.txt":
        outfile = "trigramsgresuff.txt"
    else:
        outfile = "trigramsorigsuff.txt"
    for word in infile:
        leng = len(word)
        if leng > 2:
            suff = word[leng-1] + word[leng-2] + word[leng-3]
        #else:
            #suff = word
        if suff not in suffmap:
            suffmap.update({suff: 1})
        else:
            suffmap[suff] += 1 
    #dyphmap = dict(sorted(dyphmap.items(), key=lambda item: item[1]))
    print(suffmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in suffmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION TAKES A TEXT FILE AS INPUT AND OUTPUTS A LIST OF ALL PREFIX TRIPHTHONGS 
def trigramspref(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    prefmap = {}
    if file == "latincorpus.txt":
        outfile = "trigramslatpref.txt"
    elif file == "greekcorpus.txt":
        outfile = "trigramsgrepref.txt"
    else:
        outfile = "trigramsorigpref.txt"
    for word in infile:
        if len(word)>2:
            pref = word[0] + word[1] + word[2]
        #else:
            #pref = word
        if pref not in prefmap:
            prefmap.update({pref: 1})
        else:
            prefmap[pref] += 1 
    #dyphmap = dict(sorted(dyphmap.items(), key=lambda item: item[1]))
    print(prefmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in prefmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION TAKES A TEXT FILE AS INPUT AND OUTPUTS A LIST OF ALL SUFFIX TRIPHTHONGS 
def bigramssuff(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    suffmap = {}
    if file == "latincorpus.txt":
        outfile = "bigramslatsuff.txt"
    elif file == "greekcorpus.txt":
        outfile = "bigramsgresuff.txt"
    else:
        outfile = "bigramsorigsuff.txt"
    for word in infile:
        leng = len(word)
        if leng > 2:
            suff = word[leng-2] + word[leng-1]
        else:
            suff = word
        if suff not in suffmap:
            suffmap.update({suff: 1})
        else:
            suffmap[suff] += 1 
    suffmap = dict(sorted(suffmap.items(), key=lambda item: item[1]))
    print(suffmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in suffmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION TAKES A TEXT FILE AS INPUT AND OUTPUTS A LIST OF ALL PREFIX TRIPHTHONGS 
def bigramspref(file):
    infile = open(file, "rt",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    prefmap = {}
    if file == "latincorpus.txt":
        outfile = "bigramslatpref.txt"
    elif file == "greekcorpus.txt":
        outfile = "bigramsgrepref.txt"
    else:
        outfile = "bigramsorigpref.txt"
    for word in infile:
        if len(word)>2:
            pref = word[0] + word[1] 
        else:
            pref = word
        if pref not in prefmap:
            prefmap.update({pref: 1})
        else:
            prefmap[pref] += 1 
    prefmap = dict(sorted(prefmap.items(), key=lambda item: item[1]))
    print(prefmap)

    with open(outfile, "wt",  encoding="utf-8") as f: 
        for key, value in prefmap.items(): 
            f.write('%s:%s\n' % (key, value))

#THIS FUNCTION BOILS DOWN ALL THE PREVIOUS FUNCTIONS TO A SINGLE ONE. THE AMOUNT OF CHARACTERS AND THE 
#POSITION SHALL BE INPUT AS PARAMETER AS WELL
#ASSIGN "n-x" TO THE POS PARAMETER, WHERE X IS AN INTEGER, IF YOU WANT TO START FROM THE ENDING POSITION: OF COURSE IN THIS CASE THE VALUE OF X MUST BE EQUAL OR BIGGER THAN THE VALUE OF CHARS
#ASSIGN -1 TO POS IF YOU DO NOT WANT TO START FROM A POSITION BUT YOU WANT THE LOOP PASSING THROUGH ALL WORDS
#FROM THE BEGINNING

def wordChunks(file, chars, pos :str): 
    infile = open(file, "r",  encoding="utf-8")
    infile = infile.read()
    infile = infile.split()
    chunkmap = {}
    outfile = "wordChunks"+str(file)
    for word in infile:
        if str(pos)[0] == "n":
            pos = str(len(word) - int(pos[-1]))
            pos = int(pos)
        if int(pos) >= 0:
            pos = int(pos)
            if len(word) > chars + pos:
                i = pos
                j = 1
                chunk = word[i]
                while j < chars:
                    #while i + chars < len(word):
                    chunk = chunk + word[i+1]
                    i += 1
                    j += 1
                if chunk not in chunkmap:
                    chunkmap.update({chunk: 1})
                else:
                    chunkmap[chunk] += 1
            else:
                continue
        else:
            if len(word)> chars - 1:
                chunk = word[0]
                z=1
                i =0
                while i < len(word) - chars:
                    while z < chars:
                        chunk = chunk + word[z]
                        z += 1
                    if chunk not in chunkmap:
                        chunkmap.update({chunk: 1})
                    else:
                        chunkmap[chunk] += 1
                    i+=1
               
    chunkmap = dict(sorted(chunkmap.items(), key=lambda item: item[1]))
    print(chunkmap)

    with open(outfile, "a",  encoding="utf-8") as f: 
        f.write('Chunks list of length ' + str(chars) + ' and position '+ str(pos) +'\n')
        for key, value in chunkmap.items(): 
            f.write('%s:%s\n' % (key, value))
    

    

    #OUTPUT THE RESULTS TO A TXT FILE
    #output = output.split(',')
    #patternsearch = open("patternsearch.txt", "wt",  encoding="utf-8")
    #    #for each line in the input file
    #for word in output:
	   # #read replace the string and write to output file
    #    patternsearch.write(word + ' ')

    #patternsearcht.close()

#THIS FUNCTION TAKES A HTML/XML FILE AS INPUT AND PRODUCES A TEXT FILE AS OUTPUT WITHOUT TAGGING
def xmlParse(xmlfile):
    #tree = ET.parse(xmlfile)
    #root = tree.getroot()
    #path = r"C:\Users\Palma\Desktop\cantiere\epigrafesantamarialanova\epigraphsolver\"
    dom = xml.dom.minidom.parse(r"C:\Users\\Palma\\Desktop\\cantiere\\epigrafesantamarialanova\\epigraphsolver\\" + xmlfile)
    file = dom.documentElement
    seg = dom.getElementsByTagName("orth")
    file = open('copticlexicon.txt','w',  encoding="utf-8")
    for item in seg:
        sent = item.firstChild.data
        #print(sent,sep='')
        file.write(sent)

    file.close()



#LEXICAL VARIETY IN CORPUS
def typetokenratio(text):
    string = open(text, 'r',  encoding="utf-8")
    string = string.read()
    string = string.split()
    #typetokenratio = len(set(list(greek_corpus.words())[50:149]))/100
    typetokenratio = len(set(list(string)))/len(list(string))
    print("Types' amount:")
    print(len(set(list(string))))
    print("Tokens' amount:")
    print(len(list(string)))
    print("Type-token ratio:")
    print(typetokenratio) # ---> 0.85 on 100 words


#THIS FUNCTIONS PRODUCES A WORD LIST OF GIVEN LENGTH FROM A TEXT INPUT
def generateWords(text, length):
    string = open(text, 'r',  encoding="utf-8")
    string = string.read()
    output = open("generateWords"+str(length)+".txt", 'a',  encoding="utf-8")
    for char in string:
        i = 0
        word = ""
        while i < length:
            word += string[string.index(char)+i]
            i+=1
        output.write(word + "\n")
        string = string[1:]
        if len(string) < length:
            break




#THIS FUNCTION GENERATES N-GRAM FILE OF A GIVEN INPUT FILE

def  letterNGramsfile(file, n):
    msg = open(file, "rt", encoding="utf-8")
    msg = msg.read()
    e = open(str(n)+"grams"+str(file), "wt",  encoding="utf-8")
    e.write(str([msg[i:i+n] for i in range(len(msg) - (n-1))]))
    e.close()
    
#THIS FUNCTION GENERATES N-GRAM FILE OF A GIVEN INPUT FILE RANKED BY FREQUENCY

def  letterNGramsfilerank(file, n):
    msg = open(file, "rt", encoding="utf-8")
    msg = msg.read()
    e = open(str(n)+"gramsrank"+str(file), "wt",  encoding="utf-8")
    r = str([msg[i:i+n] for i in range(len(msg) - (n-1))]).split(',')
    df1 = pd.Series(r).value_counts().sort_index().reset_index().reset_index(drop=True)
    df1.columns = ['Element', 'Frequency']
    df1 =  df1.sort_values(by = 'Frequency', ascending=False)
    # Original list
    #print(f"The original list : {test_list}" )
    # printing result
    #print(f"The list frequency of elements is :\n {df1.to_string(index=False)}")
    e.write(df1.to_string(index=False))
    e.close()

# THIS FUNCTION CONVERTS A LIST TO A MAP

def ConvertList2Map(lst):
    res_dct = map(lambda i: (lst[i], lst[i+1]), range(len(lst)-1)[::2])
    return dict(res_dct)

#THIS FUNCTION TAKES A txt FILE AS INPUT AND RETURNS A FREQUENCY DICTIONARY OF THE WORDS CONTAINED THEREIN

def freqvoc(file, outfile):
    freqvoc = {}
    msg = open(file, "rt", encoding="utf-8")
    wlist = msg.read().split()
    for word in wlist:
        ps = PorterStemmer()
        stemwo = ps.stem(word)
        if stemwo in freqvoc:
            freqvoc[stemwo] += 1
        else:
            freqvoc.update({stemwo: 1}) 

    sorted_freqvoc = sorted(freqvoc.items(), key=lambda x:x[1], reverse=True)
    sorted_freqvoc = dict(sorted_freqvoc)
    print(sorted_freqvoc)
    with open(outfile, "a",  encoding="utf-8") as f: 
        for item in sorted_freqvoc.items(): 
            f.write('%s:%s\n' % (item))


