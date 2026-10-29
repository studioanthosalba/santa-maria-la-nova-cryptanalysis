
#THIS PROJECT AIMS TO SOLVE ALL ENCRYPTED SHORT TEXTS WITH UNKNOWN ALPHABETS 
#BY A BRUTE-FORCE APPROACH DECRYPTING
#LETTERS AGAINST A CORPUS/DICTIONARY OF A (ARBITRARILY) CHOSEN LANGUAGE

#IN THE FOLLOWING REALIZATION THE LATIN LANGUAGE HAS BEEN CHOSEN TO START DUE ALL CONSIDERATIONS
#BROUGHT UP IN THE PAPER "ENCRYPTED EPIGRAPHS A JOURNAL OF THE DECRYPTION OF THE MYSETERIOUS EPIGRAPH OF SANTA MARIA LA NOVA IN NAPLES"

#NECESSARY REQUISITE TO START THIS PROGRAM IS TO CREATE A TXT FILE CONTAINING A TRANSLITTERATION OF THE UNKNOWN ALPHABET WITH A KNOWN ONE. IT IS SUGGESTED TO USE A NON-LATIN ALPHABET TO THIS PURPOSE, SO THAT CHARS SUBSTITUTIONS CAN BE PERFORMED CONSISTENTLY, OTHERWISE THE PROGRAM WILL PERFORM THE REPLACEMENT (see greekreplace())

#IF THERE IS NO MEAN TO GUESS THE SOURCE LANGUAGE TO START WITH, I PERSONALLY SUGGEST TO USE THE SOFTWARE AZDECRYPT'S LANGUAGE FUNCTIONS, WHICH DELIVERS PROBABILITY DISTRIBUTIONS FOR ALL LANGUAGES AGAINST THE INPUT TEXT


import io
import re
import nltk
from nltk import word_tokenize
import constraint
from nltk.corpus import udhr

#REPLACE ALL LATIN CHARACHTERS CONTAINED IN THE ENCRYPTED EPYGRAPH BY GREEK ONES (pay particular attention in
#matching vowels)
#this operation is necessary to avoid following scenario:
# text = "abc cb aadba" replace 1. a with b, 2. b with d, 3. c with a and 4. d with b. Output: 
#1."bbc cb bbdbb"
#2. "ddc cd ddddd"
#3. "dda ad ddddd"
#4. "bba ab bbbbb", which is not the desired result

def greekreplace():
    e = open("stringaoriginale.txt", "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("egr.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('a', 'α').replace('b', 'β').replace('c', 'ζ').replace('d', 'δ').replace('e', 'ε').replace('f', 'φ').replace('g', 'γ').replace('i', 'η').replace('l', 'λ').replace('m', 'μ').replace('n', 'ν').replace('o', 'ω').replace('p', 'π').replace('q', 'κ').replace('r', 'ρ').replace('s', 'σ').replace('t', 'τ').replace('u', 'υ').replace('v', 'χ').replace('z', 'ψ'))
    e.close()
    eg.close()

# THIS FUNCTION CREATES A FILE WHERE EACH WORD IS REPLACED WITH A PSEUDO-REGEX
# IT DIFFERENTIATES ONLY BETWEEN VOCALS AND CONSONANTS, FOLLOWED BY A NUMBER LABELLING IF 
# THERE ARE OCCURRENCES OF THE SAME ONE 

def regexreplace():
    e = open("stringaoriginale.txt", "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("regexreplace.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('a', 'V1').replace('b', 'K1').replace('c', 'K2').replace('d', 'K3').replace('e', 'V2').replace('f', 'K4').replace('g', 'K5').replace('i', 'V3').replace('l', 'K6').replace('m', 'K7').replace('n', 'K8').replace('o', 'V4').replace('p', 'K9').replace('q', 'K0').replace('r', 'KA').replace('s', 'KB').replace('t', 'KC').replace('u', 'V5').replace('v', 'KD').replace('z', 'KE'))
    e.close()
    eg.close()

# THIS FUNCTION CREATES A FILE WHERE EACH WORD IS REPLACED WITH A PSEUDO-REGEX
# IT DIFFERENTIATES ONLY BETWEEN VOCALS AND CONSONANTS

def regexreplaceweak():
    e = open("stringaoriginale.txt", "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("regexreplaceweak.txt", "wt",  encoding="utf-8")
    vowels = ('a', 'e', 'i', 'o', 'u')

    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        #eg.write(line.replace('a', 'V').replace('b', 'K').replace('c', 'K').replace('d', 'K').replace('e', 'V').replace('f', 'K').replace('g', 'K').replace('i', 'V').replace('l', 'K').replace('m', 'K').replace('n', 'K').replace('o', 'V').replace('p', 'K').replace('q', 'K').replace('r', 'K').replace('s', 'K').replace('t', 'K').replace('u', 'V').replace('v', 'K').replace('z', 'K'))
        for word in line:
            for char in word:
                if char in vowels:
                   eg.write(word.replace(char, 'V'))
                elif char == ' ' or char == '.':
                   eg.write(word.replace(char, ' '))
                else:
                  eg.write(word.replace(char, 'K'))
    e.close()
    eg.close()

#THIS FUNCTION CREATE A MAP BETWEEN VK-REGEX AND A LIST OF POSSIBLE WORDS ASSIGNED TO IT. 
#A WORD CAN BELONG ONLY TO ONE GROUP
#THE PSEUDOCODE
# TAKE A WORD OF THE LATIN DICTIONARY
#TRANSFORM IT TO THE RELATED REGEX (SEE ABOVE)
#LOOP THROUGH THE MAP. IF THE REGEX ALREADY EXISTS, APPEND THE ORIGINAL WORD TO THE LIST RELATED TO THAT REGEX
# IF IT DOES NOT ALREADY EXIST, THEN CREATE A NEW ONE WITH THE SAME DEFINITION; THEN ASSIGN THE ORIGINAL WORD TO THE RELATED EMPTY LIST AS WELL
# AT THE END OF THIS PROCESS WE WILL HAVE A BIG MAP, LINKING TO EACH REGEX A LIST OF WORDS


#THIS REPLACEMENT TAKES PLACE IN ACCORDANCE TO THE CHARS FREQUENCY OCCURRING IN THE CLOSE LATIN EPIGRAPH 
def greekreplacegreg():
    e = open("stringaoriginale.txt", "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("egrgr.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('a', '(ι/ε)').replace('b', 'ο').replace('c', '(ζ/ν/δ)').replace('d', '(β/γ/κυ)').replace('e', '(ρ/υ/ν)').replace('f', '(ζ/ν/δ)').replace('g', '(β/γ/κυ)').replace('i', '(ι/ε)').replace('l', '(λ/π)').replace('m', '(ρ/υ/ν)').replace('n', '(ζ/ν/δ)').replace('o', '(β/γ/κυ)').replace('p', '(β/γ/κυ)').replace('q', '(β/γ/κυ)').replace('r', '(σ/τ)').replace('s', 'β').replace('t', '(σ/τ)').replace('u', 'α').replace('v', '(λ/π)').replace('z', 'ψ'))
    e.close()
    eg.close()

#THIS REPLACEMENT TAKES PLACE IN ACCORDANCE TO THE CHARS FREQUENCY OCCURRING IN THE LATIN DICTIONARY
def greekreplacedic():
    e = open("stringaoriginale.txt", "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("egrdic.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('a', '(ι/ε)').replace('b', 'α').replace('c', '(ζ/μ)').replace('d', '(β/φ/γ/κυ)').replace('e', '(σ/ρ/τ)').replace('f', '(ζ/μ)').replace('g', '(β/φ/γ/κυ)').replace('i', '(ι/ε)').replace('l', 'λ').replace('m', '(σ/ρ/τ)').replace('n', 'ν').replace('o', '(β/φ/γ/κυ)').replace('p', '(β/φ/γ/κυ)').replace('q', '(β/φ/γ/κυ)').replace('r', '(ο/υ)').replace('s', 'δ').replace('t', '(σ/ρ/τ)').replace('u', '(ο/υ)').replace('v', '(λ/π)').replace('z', 'ψ'))
    e.close()
    eg.close()

#THIS FUNCTIONS BRINGS BACK TO LATIN CHARS WHAT WAS TEMPORARILY MAPPED TO GREEK ONES
def latgreekreplace(text):
    e = open(text, "rt", encoding="utf-8")
    #output file to write the result to
    eg = open(text+"lat.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('α','a').replace('β', 'b').replace('ζ', 'c').replace('δ', 'd').replace('ε', 'e').replace('φ', 'f').replace('γ', 'g').replace('η', 'i').replace('λ', 'l').replace('μ', 'm').replace('ν', 'n').replace('ω', 'o').replace('π', 'p').replace('κυ', 'q').replace('ρ', 'r').replace('σ', 's').replace('τ', 't').replace('υ', 'u').replace('χ', 'v').replace('ψ', 'z'))
    e.close()
    eg.close()


#CREATE A DICTIONARY TO STORE MAPPING OF ENCRYPTED-DECRYPTED GLYPHS 
# Assign to the first term the list of greek letters, and to the mapped term an empty space.
# according to this list appropriately filled the final charcter replacement will take place, to which the output of the decrypted epigraph will follow

glyphmap = {
  "α": "",
  "β": "",
  "ζ": "",
  "δ" : "",
  "ε" : "",
  "φ": "",
  "γ": "",
  "η": "",
  "λ": "",
  "μ": "",
  "ν": "",
  "ω": "",
  "π": "",
  "κ": "",
  "ρ": "",
  "σ": "",
  "τ": "",
  "υ": "",
  "χ": "",
  "ψ": "",
}

#CREATE A DICTIONARY TO STORE MAPPING OF GLYPH-FREQUENCIES


glyphmapfreq = {
  "a": 0,
  "b": 0,
  "c": 0,
  "d": 0,
  "e": 0,
  "f": 0,
  "g": 0,
  "h": 0,
  "i": 0,
  "l": 0,
  "m": 0,
  "n": 0,
  "o": 0,
  "p": 0,
  "q": 0,
  "r": 0,
  "s": 0,
  "t": 0,
  "u": 0,
  "v": 0,
  "z": 0
}

#CREATE A DICTIONARY TO STORE MAPPING OF THE ENCRYPTED GLYPH-FREQUENCIES

epglyphmapfreq = {
  "α": 0,
  "β": 0,
  "δ": 0,
  "ε": 0,
  "ζ": 0,
  "φ": 0,
  "γ": 0,
  "η": 0,
  "λ": 0,
  "μ": 0,
  "ν": 0,
  "ω": 0,
  "π": 0,
  "κ": 0,
  "ρ": 0,
  "σ": 0,
  "τ": 0,
  "υ": 0,
  "χ": 0,
  "ψ": 0,
}

#LOOK FOR THE LONGEST WORD IN EG 
# The principle of this action is to directly compare the longest type in the epigraph (which means one of the most
# complex words of the related vocabulary) with the longest dictionary entry.
# This is based on the synergetic linguistics principle that the longer a word is the more complex and rare it is.
#In our case it follows: the more chances there are to confirm the chosen language for the encryption.
# This is also the greediest way to guess as many chars as possible.
#To be sure potential matches will not be discarded because of suffixes changes following declinations
# we are not taking into account the last 3 letters
# if even this precaution will not produce a positive output, it does not immediately mean that the we have
# chosen the wrong language for our validation: it may also suggest that the dictionary is not rich enough, or that the encrypted words have been also anagrammed. 

def longestword ():
    
    #open the file containing the test
    eg = open("egr.txt",  "rt",  encoding="utf-8")
    #convert the file in a list of words separated by space
    # return the split results, which is all the words in the file.
    eg = eg.read().split()

    print(eg)
    #loop trought the egr text to get the longest word
    maxlen = 0
    for word in eg:
        if len(word) > maxlen:
           maxlen = len(word) 
           maxword = word

    maxword1 = maxword[:maxlen - 1]
    maxword2 = maxword[:maxlen - 2]
    maxword3 = maxword[:maxlen - 3]
    print(maxword, maxlen, maxword1, maxlen-1, maxword2, maxlen-2, maxword3, maxlen-3, sep = ' ,')

   
#LOOK FOR THE LONGEST WORD IN THE (LATIN) DICTIONARY

def longestworddict ():
    
    #open the file containing the latin vocabulary
    l = open("latindic.txt", "r")
    #convert the file in a list of words separated by space
    # return the split results, which is all the words in the file.
    l = l.read().split()
    #re.split(', |\*|\n', l)

    #print(l)
    #loop trought the l text to get the longest word
    maxlendict = 0
    maxworddict = []
    for word in l:
        if len(word) >= maxlendict:
            maxlendict = len(word) 
            maxworddict.append(word)
    #remove from the array the shorter words
    for a in list(maxworddict):
        if len(a) < maxlendict:
            maxworddict.remove(a)
   # for word in l:
   #    if len(word) = (maxlen-1):
           

    maxworddict = maxworddict[len(maxworddict)-1]
    maxword1dict = maxworddict[:maxlendict- 1]
    maxword2dict = maxword1dict[:maxlendict- 2]
    maxword3dict = maxword1dict[:maxlendict - 3]
    print(maxworddict,maxlendict, maxword1dict, maxlendict-1, maxword2dict, maxlendict-2, maxword3dict,maxlendict-3, sep = ' ,')



#THIS FUNCTION RETURNS A LIST OF ALL FILE WORDS OF A DETERMINED FILE AND LENGTH
def allwordslength(length, file):
    #open the file containing the latin vocabulary
    l = open(file, "rt",  encoding="utf-8")
    #convert the file in a list of words separated by space
    # return the split results, which is all the words in the file.
    l = l.read().split()
    #re.split(', |\*|\n', l)

    #print(l)
    #loop trought the l text to get the longest word
    wordlenfile = length
    lenwordfile = []
    for word in l:
        if len(word) == wordlenfile:
            lenwordfile.append(word)
         

    #maxword1dict = maxworddict[len(maxworddict)-1]
    #maxword1dict = str(maxworddict[0])
    #maxword2dict = maxword1dict[:maxlendict- 2]
    #maxword3dict = maxword1dict[:maxlendict - 3]
    print(str(length))
    print(lenwordfile)
    return lenwordfile



#THIS FUNCTION COMPARES THE WORDS IN THE SAMPLE AND IN THE DICTIONARY. IF THEY MATCHES, IT OUTPUTS
#"MATCH!" AND PROPAGATES THE LETTER ASSIGNMENT TO THE INITIALLY CREATED CHARS LIST

def wordcompare():
    pass
 
#THIS FUNCTION WEAKLY COMPARES THE LONGEST WORDS IN THE SAMPLE AND IN THE DICTIONARY. 
# "WEAKLY" MEANS THAT THE LETTERS MATCH YET NOT THEIR ORDER (IN OTHER WORDS, THE FIRST COULD BE AN ANAGRAM OF THE SECOND)
#IF THEY MATCHES, IT OUTPUTS
#"WEAK MATCH".
#IN THIS CASE THE LETTER ASSIGNMENT TO THE INITIALLY CREATED CHARS LIST SHALL HAPPEN MANUALLY ACCORDING TO THE 
#USER JUDGEMENT

def wordweakcompare():
    pass

#THIS FUNCTION LOOPS THROUGH A PARTICULAR WORD LIST SEEKING FOR A PATTERN. IT TAKES THE NUMBER OF CHRACTERS AND THE PATTERN AS PARAMETERS. 'K' means consonant, 'Y' vowel and 'U' all different letters

def patternsearch(wordlength, pattern):
    wordlist = []
    wordlist = allwordslength(wordlength, "latindic.txt")
    output = ""
    if pattern == 'KK':
        for word in wordlist:
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
    print("List of all words with length " + str(wordlength) + " and pattern " + str(pattern) + ":\n" + output)


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

while shift<27:
    caesar("stringaoriginale.txt", shift)
    shift +=1

#THIS SMALL FUNCTION REMOVES ALL SPACES IN AN INPUT TEXT OUTPUTTING THE TRIMMED STRING

def RemoveSpaces(epigraph):
    epigraph = open(epigraph, "rt", encoding="utf-8")
    epigraph = epigraph.read()
    trimmedString = epigraph.replace(' ', '').replace('\n','').replace('\t','')
    print(trimmedString)

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
    text = text.read()
    sortedString = ""
    wordarr = []
    text = text.split()
    for word in text:
        word = sorted(set(word))
        wordsort = ''.join(word)
        sortedString = sortedString + " " + wordsort
    sortedtext.write(sortedString)
    #text.close()
    sortedtext.close()
    print(sortedString)  

#THIS FUNCTIONS LIST ALL CHARS FREQUENCY OF A TEST. THE DATA STRUCTURE IN OUTPUT WILL BE A DICTIONARY

def charactersfrequencylat(file):
    text = open(file, "rt", encoding="utf-8")
    text = text.read()
    text = text.split()
    textnospace = ""
    for word in text:
        textnospace += word
    for char in textnospace:
        if char == "a":
            glyphmapfreq["a"] += 1
        elif char == "b":
            glyphmapfreq["b"] += 1
        elif char == "c":
            glyphmapfreq["c"] += 1
        elif char == "d":
            glyphmapfreq["d"] += 1
        elif char == "e":
            glyphmapfreq["e"] += 1
        elif char == "f":
            glyphmapfreq["f"] += 1
        elif char == "g":
            glyphmapfreq["g"] += 1
        elif char == "h":
            glyphmapfreq["h"] += 1
        elif char == "i":
            glyphmapfreq["i"] += 1
        elif char == "l":
            glyphmapfreq["l"] += 1
        elif char == "m":
            glyphmapfreq["m"] += 1
        elif char == "n":
            glyphmapfreq["n"] += 1
        elif char == "o":
            glyphmapfreq["o"] += 1
        elif char == "p":
            glyphmapfreq["p"] += 1
        elif char == "q":
            glyphmapfreq["q"] += 1
        elif char == "r":
            glyphmapfreq["r"] += 1
        elif char == "s":
            glyphmapfreq["s"] += 1
        elif char == "t":
            glyphmapfreq["t"] += 1
        elif char == "u":
            glyphmapfreq["u"] += 1
        elif char == "v":
            glyphmapfreq["v"] += 1
        elif char == "z":
            glyphmapfreq["z"] += 1
    
    print("Real chars frequency \n") 
    print(dict(sorted(glyphmapfreq.items(), key=lambda item: item[1])))
    

#... AND WE PERFORM THE SAME WITH ALL EPIGRAPHS' CHARS
def charactersfrequency(file):
    text = open(file, "rt", encoding="utf-8")
    text = text.read()
    text = text.split()
    textnospace = ""
    for word in text:
        textnospace += word
    for char in textnospace:
        if char == "α":
            epglyphmapfreq["α"] += 1
        elif char == "β":
            epglyphmapfreq["β"] += 1
        elif char == "δ":
            epglyphmapfreq["δ"] += 1
        elif char == "ζ":
            epglyphmapfreq["ζ"] += 1
        elif char == "ε":
            epglyphmapfreq["ε"] += 1
        elif char == "φ":
            epglyphmapfreq["φ"] += 1
        elif char == "γ":
            epglyphmapfreq["γ"] += 1
        elif char == "η":
            epglyphmapfreq["η"] += 1
        elif char == "λ":
            epglyphmapfreq["λ"] += 1
        elif char == "μ":
            epglyphmapfreq["μ"] += 1
        elif char == "ω":
            epglyphmapfreq["ω"] += 1
        elif char == "π":
            epglyphmapfreq["π"] += 1
        elif char == "κ":
            epglyphmapfreq["κ"] += 1
        elif char == "ρ":
            epglyphmapfreq["ρ"] += 1
        elif char == "σ":
            epglyphmapfreq["σ"] += 1
        elif char == "τ":
            epglyphmapfreq["τ"] += 1
        elif char == "υ":
            epglyphmapfreq["υ"] += 1
        elif char == "χ":
            epglyphmapfreq["χ"] += 1
        elif char == "ψ":
            epglyphmapfreq["ψ"] += 1
    
    print("Epigraph's chars frequency \n") 
    print(dict(sorted(epglyphmapfreq.items(), key=lambda item: item[1])))
  
#create array with all matches 


#look for all words with  length equal to the epigraph word length (-2. If for instance it is a verb,
#then the dictionary does not present the declination. there could be alternative solutions to the same
#problem. the same happens with plural genitive, dativ ablativ nouns, see '-ibus' and '-arum')

#Compare the word from e with the bunch of words from l. All matching words are added to the array matches.

#Take the first match word and find in the e file the shortest word containing the hugest amount of letters

greekreplace()
greekreplacegreg()
greekreplacedic()
regexreplace()
regexreplaceweak()
latgreekreplace("egrdic.txt")
latgreekreplace("egrgr.txt")
RemoveSpaces("egr.txt")
skipletters(3, "egr.txt")
SortText("stringaoriginale.txt")
longestword()
longestworddict()
charactersfrequency("egr.txt")
glyphmapfreq = { x:0 for x in glyphmapfreq}
charactersfrequencylat("stringaoriginale.txt")
glyphmapfreq = { x:0 for x in glyphmapfreq}
charactersfrequencylat("gregoriipapaxiii.txt")
charactersfrequencylat("latindic.txt")

i = 1
while i < 16:
  allwordslength(i, "egr.txt")
  #allwordslength(i, "latindic.txt")
  patternsearch(i, 'KK')
  patternsearch(i, 'YY')
  patternsearch(i, 'U')
  i += 1


#THIS CHUNK OF CODE MAKES USE OF CONSTRAINT PROGRAMMING PARADIGM TO SOLVE OUR PROBLEM
# TO BE DEVELOPED LATER

problem = constraint.Problem()

problem.addVariable('glyphep', ["α",
  "β",
  "δ",
  "ε",
  "ζ",
  "φ",
  "γ",
  "η",
  "λ",
  "μ",
  "ν",
  "ω",
  "π",
  "κ",
  "ρ",
  "σ",
  "τ",
  "υ",
  "χ",
  "ψ"])

problem.addVariable('glyphdic',  ["a",
  "b",
  "c",
  "d",
  "e",
  "f",
  "g",
  "h",
  "i",
  "l",
  "m",
  "n",
  "o",
  "p",
  "q",
  "r",
  "s",
  "t",
  "u",
  "v",
  "z" ])

#problem.addVariable('latdic')
def epigraphdecrypt(glyphep, glyphdic):
    pass

#problem.addConstraint(AllDifferentConstraint())
problem.addConstraint(epigraphdecrypt, ['glyphep','glyphdic'])

solutions = problem.getSolutions()

# Easier way to print and see all solutions
# for solution in solutions:
#    print(solution)

# Prettier way to print and see all solutions
length = len(solutions)
print("(glyphep,glyphdic) ∈ {", end="")
for index, solution in enumerate(solutions):
    if index == length - 1:
        print("({},{})".format(solution['glyphep'], solution['glyphdic']), end="")
    else:
        print("({},{}),".format(solution['glyphep'], solution['glyphdic']), end="")
print("}")

#This is useful to show the anagram hypothesis inconsistency - Frequency Graph of words in original string
text = open("stringaoriginale.txt", "rt", encoding="utf-8")
text = text.read().split()
fdist1 = nltk.FreqDist(text)
print(fdist1)
fdist1.most_common(50)
fdist1.plot(50, cumulative=False)

#Frequency graph of sorted words
text2 = open("sortedwords_anagram.txt", "rt", encoding="utf-8")
text2 = text2.read().split()
fdist2 = nltk.FreqDist(text2)
print(fdist2)
fdist2.most_common(50)
fdist2.plot(50, cumulative=False)

# Frequency graph of epigraph of Pope Gregory XIII
text3 = open("gregoriipapaxiii.txt", "rt", encoding="utf-8")
text3 = text3.read().split()
fdist3 = nltk.FreqDist(text3)
print(fdist3)
fdist3.most_common(50)
fdist3.plot(50, cumulative=False)
#return dictionary


  	

nltk.download('udhr')
languages = ['Chickasaw', 'English', 'German_Deutsch',
    'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
cfd = nltk.ConditionalFreqDist(
          (lang, char)
          for lang in languages
          for word in udhr.words(lang + '-Latin1')
          for char in word
          if re.search(r'([a-z])',char))
cfd.plot(cumulative=True)
print(glyphmap)


#nltk.FreqDist(text3).plot()
#output translated text
#write translated text into a new txt file