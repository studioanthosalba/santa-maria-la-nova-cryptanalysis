import string
import re
import math
import unicodedata
import os
import NLP
import pandas as pd

shift = 1
#THIS SMALL FUNCTIONS PERFORMS A CESAR ATTACK ON THE ORIGINAL STRING FILE
def caesar(plainText, shift):
  plainText = open(plainText, "rt", encoding="utf-8")
  cipherText = ""
  plainText = plainText.read()
  for ch in str(plainText):
    if ch.isalpha():
      stayInAlphabet = ord(ch) + shift 
      if stayInAlphabet > ord('z'):
        stayInAlphabet -= 26
      finalLetter = chr(stayInAlphabet)
      cipherText += finalLetter
  print("Your " + "(Shift " + str(shift) + ") ciphertext is: ", cipherText + "\n")
  return cipherText

#while shift<27:
#    caesar("stringaoriginale.txt", shift)
#    shift +=1



#THIS SMALL FUNCTIONS CREATES A NEW STRING IN WHICH LETTERS ARE SKIPPED
def skipletters(skip, text):
    text = open(text, "rt", encoding="utf-8")
    text = text.read()
    out = ""
    count = 0
    for letter in text:
        count += 1
        if count == skip:
            out = out + letter
            count = 0
    out = out + "\n"
    print(out)


#THIS FUNCTION SORTS ALPHABETICALLY THE LETTERS OF ALL WORDS IN THE TEXT.
#THE AIM OF THIS OPERATION IS TO DETECT ANAGRAMS

def SortText(text):
    text = open(text, "rt", encoding="utf-8")
    #output file to write the result to
    sortedtext = open("sortedwords_anagram.txt", "wt",  encoding="utf-8")
    #sortedtextgr = open("sortedwords_anagramgreek.txt", "wt",  encoding="utf-8")
    text = text.read()
    sortedString = ""
    #wordarr = []
    #len2 = []
    #len3 = []
    #len4 = []
    #len5 = []
    #len6 = []
    #len7 = []
    #len8 = []
    #len9 = []
    #len10 = []
    #len11 = []
    #len12 = []
    #len13 = []
    #len14 = []
    #len15 = []
    #len16 = []
    #len17 = []
    #len18 = []
    #len19 = []
    text = text.split()
    for word in text:
        word = sorted(set(word))
        wordsort = ''.join(word)
        sortedString = sortedString + " " + wordsort
    sortedtext.write(sortedString)
    #for word in text:
    #    if len(word) == 2:
    #        len2.append(word)
    #    if len(word) == 3:
    #        len3.append(word)
    #    if len(word) == 4:
    #        len4.append(word)
    #    if len(word) == 5:
    #        len5.append(word)
    #    if len(word) == 6:
    #        len6.append(word)
    #    if len(word) == 7:
    #        len7.append(word)
    #    if len(word) == 8:
    #        len8.append(word)
    #    if len(word) == 9:
    #        len9.append(word)
    #    if len(word) == 10:
    #        len10.append(word)
    #    if len(word) == 11:
    #        len11.append(word)
    #    if len(word) == 12:
    #        len12.append(word)
    #    if len(word) == 13:
    #        len13.append(word)
    #    if len(word) == 14:
    #        len14.append(word)
    #    if len(word) == 15:
    #        len15.append(word)
    #    if len(word) == 16:
    #        len16.append(word)
    #    if len(word) == 17:
    #        len17.append(word)
    #    if len(word) == 18:
    #        len18.append(word)
    #    if len(word) == 19:
    #        len19.append(word)
    #print(len2)
    #print(len3)
    #print(len4)
    #print(len5)
    #print(len6)
    #print(len7)
    #print(len8)
    #print(len9)
    #print(len10)
    #print(len11)
    #print(len12)
    #print(len13)
    #print(len14)
    #print(len15)
    #print(len16)
    #print(len17)
    #print(len18)
    #print(len19)
    #text.close()
    sortedtext.close()
    print(sortedString)  

#THIS FUNCTION LOOPS THROUGH A TXT FILE TO FIND A WORD MATCHING WITH THE ONE INPUTTED WORD AS PARAMETER
#I.E.: WORD=POLO ___ FILE= BEBE; MARMELADE; MOUSE; POSTER; FATA ---> RESULT: FATA
def matchWord(word, file):
    m = open(file, "rt", encoding="utf-8")
    #output file to write the result to
    mw = open("matchWord.txt", "a",  encoding="utf-8")
    #mwf = open("matchWordFile.txt", "a")
    m = m.read().split()
    superword=""
    superwordfile = ""
    superchar = ['1','2','3','4','5','6','7','8','9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'L', 'M']
    for char in word:
        superword = superword + superchar[list(word).index(char)]
    print(superword)
    #for each word in the input file
    for wort in m:
        for char in wort:
            superwordfile = superwordfile + superchar[list(wort).index(char)]
        with open("matchWordFile.txt", "a", encoding="utf-8") as mwf:
           mwf.write(superwordfile + '\t' + str(wort)  + '\n') #+ ' ' + wort 
        superwordfile = ""
    mwf = open("matchWordFile.txt", "rt", encoding="utf-8")
    mwf = mwf.read().split()
    for wort in mwf:
        if wort == superword:
            next_word = mwf[mwf.index(wort) + 1]
            mw.write(wort + '\t' + next_word + '\n')
            mwf.remove(wort)
    mw.close()


#THIS FUNCTION LOOPS THROUGH A TXT FILE TO FIND A WORD MATCHING WITH THE ONE INPUTTED WORD AS PARAMETER
#I.E.: WORD=POLO ___ FILE= BEBE; MARMELADE; MOUSE; POSTER; FATA ---> RESULT: FATA
#IN THIS VERSION OF THE PREVIOUS FUNCTION, WE ASSUME THAT THE SCRIPT CONTAIN NO SPACE
def matchWordscrco(word, file):
    m = open(file, "rt", encoding="utf-8")
    #output file to write the result to
    mw = open("matchWordscrco.txt", "a",  encoding="utf-8")
    #mwf = open("matchWordFile.txt", "a")
    m = m.read()
    superword=""
    superwordfile = ""
    superchar = ['1','2','3','4','5','6','7','8','9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'L', 'M']
    n = len(word)
    wordlist = [m[i:i+n] for i in range(len(m)-n+1)]
    for char in word:
        superword = superword + superchar[list(word).index(char)]
    print(superword)
    #for each word in the input file
    for wort in wordlist:
        for char in wort:
            superwordfile = superwordfile + superchar[list(wort).index(char)]
        with open("matchWordFile.txt", "a", encoding="utf-8") as mwf:
           mwf.write(superwordfile + '\t' + str(wort)  + '\n') #+ ' ' + wort 
        superwordfile = ""
    mwf = open("matchWordFile.txt", "rt", encoding="utf-8")
    mwf = mwf.read().split()
    for wort in mwf:
        if wort == superword:
            next_word = mwf[mwf.index(wort) + 1]
            mw.write(wort + '\t' + next_word + '\n')
            mwf.remove(wort)
    mw.close()


#THIS FUNCTION LOOPS THROUGH A PARTICULAR WORD LIST SEEKING FOR A PATTERN. IT TAKES THE NUMBER OF CHRACTERS AND THE PATTERN AS PARAMETERS. 'K' means consonant, 'Y' vowel and 'U' all different letters

def patternsearch(wordlength, corpus, pattern, cont = False):  #the developer must be careful here to align the boolean value to the actual segmentation of the inputted corpus
    global patternsearcht 
    if cont == False:
        wordlist = []
        wordlist = allwordslength(wordlength, corpus)
        patternsearcht = open("patternsearch.txt", "a",  encoding="utf-8")
        output = ""
        if corpus == "greekcorpus.txt" or corpus == "copticbible.txt":
            if pattern == 'KK':
                for word in list(wordlist):
                    if re.search(r'([^αευιοηω])\1',word):   
                        output = output + " , " + str(word)
            elif pattern == 'YY':
                for word in list(wordlist):
                    if re.match(r'([αευιοηω])\1',word):     
                        output = output + " , " + word
            elif pattern == 'U':
                for word in list(wordlist):
                    if re.match(r'^(?:([Α-Ωα-ω])(?!.*\1))*$',word):    
                        output = output + " , " + word
            elif pattern == 'DEFED':
                for word in list(wordlist):
                    if len(word) == 5 and isPalindrome(word):    #workaround for greek DEFED
                        output = output + " , " + word
            elif pattern == 'TOAT':
                for word in list(wordlist):
                    if re.match(r'\b(?=.{4})(?=(?:[\u0370-\u03ff]))(.)(.)[\u0370-\u03ff]\1\b',word):    #deprecated
                        output = output + " , " + word
            elif pattern == 'RTOA':
                for word in list(wordlist):
                    if re.match(r'[\u0370-\u03ff\t]{4}',word):    #workaround for greek RTOA
                        output = output + " , " + word
            print("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output)
            patternsearcht.write("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output + "\n")
        else: #corpus == "latincorpus.txt":
            if pattern == 'KK':
                for word in list(wordlist):
                    if re.search(r'([^aeiou])\1',word):   
                        output = output + " , " + str(word)
            elif pattern == 'YY':
                for word in list(wordlist):
                    if re.match(r'([aeiou])\1',word):     
                        output = output + " , " + word
            elif pattern == 'U':
                for word in list(wordlist):
                    if re.match(r'^(?:([A-Za-z])(?!.*\1))*$',word):    
                        output = output + " , " + word
            elif pattern == 'DEFED':
                for word in list(wordlist):
                    if re.match(r'\b(?=.{5})(?=(?:[a-z]))(.)(.)[a-z]\2\1\b', word):    
                        output = output + " , " + word
            elif pattern == 'TOAT':
                for word in list(wordlist):
                    if re.match(r'\b(?=.{4})(?=(?:[a-z]))(.)(.)[a-z]\1\b',word):    
                        output = output + " , " + word
            elif pattern == 'RTOA':
                for word in list(wordlist):
                    if re.match(r'\b(?=.{4})(?=(?:[a-z]))(.)(.)[a-z]\b',word):    
                        output = output + " , " + word
            print("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output)
            patternsearcht.write("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output + "\n")
    elif cont == True:
        patternsearcht = open("patternsearch.txt", "a",  encoding="utf-8")
        output = ""
        wordlist = []
        if corpus == "greekcorpus.txt" or corpus == "copticbible.txt":
            corpus = corpus.read()
            if pattern == 'KK':
                n = 2
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.search(r'([^αευιοηω])\1',word):   
                        output = output + " , " + str(word)
            elif pattern == 'YY':
                n = 2
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.match(r'([αευιοηω])\1',word):     
                        output = output + " , " + word
            elif pattern == 'DEFED':
                n = 5
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if len(word) == 5 and isPalindrome(word):    #workaround for greek DEFED
                        output = output + " , " + word
            elif pattern == 'TOAT':
                n = 4
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.match(r'\b(?=.{4})(?=(?:[\u0370-\u03ff]))(.)(.)[\u0370-\u03ff]\1\b',word):    #deprecated
                        output = output + " , " + word
            elif pattern == 'RTOA':
                n = 4
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.match(r'[\u0370-\u03ff\t]{4}',word):    #workaround for greek RTOA
                        output = output + " , " + word
            print("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output)
            patternsearcht.write("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output + "\n")
        else: #corpus == "latincorpus.txt":
            corpus = open(corpus, "rt",  encoding="utf-8")
            corpus = corpus.read()
            if pattern == 'KK':
                n = 2
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.search(r'([^aeiou])\1',word):   
                        output = output + " , " + str(word)
            elif pattern == 'YY':
                n = 2
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.match(r'([aeiou])\1',word):     
                        output = output + " , " + word
            elif pattern == 'DEFED':
                n = 5
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.match(r'\b(?=.{5})(?=(?:[a-z]))(.)(.)[a-z]\2\1\b', word):    
                        output = output + " , " + word
            elif pattern == 'TOAT':
                n = 4
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.match(r'\b(?=.{4})(?=(?:[a-z]))(.)(.)[a-z]\1\b',word):    
                        output = output + " , " + word
            elif pattern == 'RTOA':
                n = 4
                wordlist = [corpus[i:i+n] for i in range(len(corpus)-n+1)]
                for word in list(wordlist):
                    if re.match(r'\b(?=.{4})(?=(?:[a-z]))(.)(.)[a-z]\b',word):    
                        output = output + " , " + word
            print("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output)
            patternsearcht.write("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output + "\n")
        


#MAKETRANS IS THE FUNCITON OF STRING PACKAGE WHICH MAKES CHARS REPLACEMENT EASIER (PREVIOUSLY ADOPTED METHOD
#OF CONVERSION TO GREEK ALPHABET CAN BE HENCEFORTH DISMISSED)
alphabet = "abcdefghijklmnopqrstuvwxyz"
def encrypt(msg, key):
   return msg.translate(string.maketrans(alphabet, key))

def keySwap(key, a, b):
   return key.translate(string.maketrans(a+b, b+a))

#N-GRAM DECRYPTION METHOD BORROWED FROM  j2kun/cryptanalysis-n-grams (first attempt)

#PSEUDOCODE FOR STEEP ASCENT, TO GRASP ITS INTUITION

#def steepestAscent(posn, evaluatePosn, generateNeighbors, numSteps):
#   val = evaluatePosn(posn)
#   neighbors = generateNeighbors(posn)
 
#   for i in numSteps:
#     next = neighbors.next()
#     nextVal = evaluatePosn(next)
 
#     if nextVal &gt; val:
#        val = nextVal
#        posn = next
#        neighbors = generateNeighbors(next)
 
#   return posn

def steepestAscent(msg, key, decryptionFitness, numSteps):
   decryption = decrypt(msg, key)
   value = decryptionFitness(decryption)
   neighbors = iter(neighboringKeys(key, decryption))
 
   for step in range(numSteps):
      nextKey = neighbors.next()
      nextDecryption = decrypt(msg, nextKey)
      nextValue = decryptionFitness(nextDecryption)
 
      if nextValue > value:
         key, decryption, value = nextKey, nextDecryption, nextValue
         neighbors = iter(neighboringKeys(key, decryption))
         print((decryption, key))
 
   return decryption

def letterNGrams(msg, n):
   return [msg[i:i+n] for i in range(len(msg) - (n-1))]

#bigramLetterProb = OneGramDist('count-2l.txt')

def neighboringKeys(key, decryptedMsg):
   bigrams = sorted(letterNGrams(decryptedMsg, 2),
                    key=bigramLetterProb)[:30]
 
   for c1, c2 in bigrams:
      for a in shuffled(alphabet):
         if c1 == c2 and bigramLetterProb(a+a) >  bigramLetterProb(c1+c2):
            yield keySwap(key, a, c1)
         else:
            if bigramLetterProb(a+c2) > bigramLetterProb(c1+c2):
               yield keySwap(key, a, c1)
            if bigramLetterProb(c1+a) > bigramLetterProb(c1+c2):
               yield keySwap(key, a, c2)
 
   while True:
      yield keySwap(key, random.choice(alphabet),
                         random.choice(alphabet))

def shuffled(s):
   sList = list(s)
   random.shuffle(sList)
   return ''.join(sList)
 
def preprocessInputMessage(chars):
   return ''.join(re.findall('[a-z]+', chars.lower()))
 
def crackSubstitution(msg, numSteps = 5000, restarts = 30):
   msg = preprocessInputMessage(msg)
   startingKeys = [shuffled(alphabet) for i in range(restarts)]
   localMaxes = [steepestAscent(msg, key, trigramStringProb, numSteps)
                 for key in startingKeys]
 
   for x in localMaxes:
      print(segmentWithProb(x))
 
   prob, words = max(segmentWithProb(decryption) for decryption in localMaxes)
   return ' '.join(words)


#THIS FUNCTION RETURNS THE INDEX OF COINCIDENCE OF AN INPUT FILE

alph = "abcdefghijklmnopqrstuvwxyz"

def isLetter(char):
	return (char in alph)

def countLetters(text):
	count = 0
	for i in text:
		if(isLetter(i)):
			count += 1
	return count

def getIOC(file):
    letterCounts = []
    text = open(file, "rt", encoding="utf-8")
    text = text.read()	
	# Loop through each letter in the alphabet - count number of times it appears
    for i in range(len(alph)):
        count = 0
        for j in text:
            if j == alph[i]:
                count += 1
        if count > 0:
            letterCounts.append(count)
	# Loop through all letter counts, applying the calculation (the sigma part)
    total = 0
        

    for i in range(len(letterCounts)):
        ni = letterCounts[i]
        total += ni * (ni - 1)
    N = countLetters(text)
    c = len(letterCounts)
    total = float(total) / ((N * (N - 1)/c))
    print(total)
    return total

#IL CORPUS DI INPUT DELLA FUNZIONE SUCCESSIVA É CREATO SELEZIONANDO FILE CHE HANNO IOC PIÚ SIMILE A QUELLO DELL'EPIGRAFE
#ATTRAVERSO QUESTA FUNZIONE:

def generateIOCcorpus(encry_file, corpusdirectory):
    print("How would you like to name the output-file?")
    cont = input()
    stringioc = getIOC(encry_file)
    finalcorpus = ""
    for filename in os.listdir(corpusdirectory):
        f = os.path.join(corpusdirectory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            corpusioc = getIOC(f)
            if abs(corpusioc - stringioc) <= 0.05:
                a = open(f, "rt", encoding="utf-8")
                finalcorpus += a.read()
    e = open("IOCcorpus" + cont + ".txt", "wt",  encoding="utf-8")
    e.write(finalcorpus)
    e.close

#THIS FUNCTION TAKES A CORPUS AS INPUT (AS  THE ONE GENERATED IN THE PREVIOUS FUNCTION)
# AND GENERATES A TXT FILE CONTAINING THE LOGARITHMIC 
#VALUES FOR ALL N-GRAMS IN THE FORMAT REQUESTED BY AZDECRYPT (5-Grams):
#"EXAMPL123XAMPL009AMPLE007"

def ngramsAZ(corpus, n, case = "lower"):
    f = open(corpus, "rt", encoding="utf-8")
    f = f.read()
    e = open(str(n) + "gramsAZ" + str(corpus) + case, "wt",  encoding="utf-8")
    r = str([f[i:i+n] for i in range(len(f) - (n-1))]).split(',')
    df1 = pd.Series(r).value_counts().sort_index().reset_index().reset_index(drop=True)
    df1.columns = ['Element', 'Frequency']
    df1 =  df1.sort_values(by = 'Frequency', ascending=False)
    df1 = dict(zip(df1.Element, df1.Frequency))
    df1 = sorted(df1.items(), key=lambda item: item[1], reverse=True)
    AZdecryptstr = ""
    for key in df1:
        log_ngram = round(math.log(int(key[1]))*10)
        if case == "lower":
            AZdecryptstr += str(key[0]) + str(log_ngram).zfill(3)
        else:
            AZdecryptstr += str(key[0]).upper() + str(log_ngram).zfill(3)

    AZdecryptstr = AZdecryptstr.replace("'", "").replace(" ", "")
    e.write(AZdecryptstr)
    e.close
   
    

#THIS FUNCTION ATTEMPTS THE FINAL SOLUTION OF THE CIPHER BY GENERALIZING PREVIOUSLY IMPLEMENTED APPROACHES
#TO THE SCRIPTIO CONTINUA - LONGEST WORD APPROACH- PALINDROMES (third attempt)

#def decipherepigraph():
