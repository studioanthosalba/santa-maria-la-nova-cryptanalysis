
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

def longestword(file):
    
    #open the file containing the test
    eg = open(file,  "rt",  encoding="utf-8")
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

   
#LOOK FOR THE LONGEST WORD IN THE (LATIN/GREEK) DICTIONARY/CORPUS

def longestworddict(corpustypes):
    
    #open the file containing the latin vocabulary
    #l = open("latindic.txt", "r")
    #convert the file in a list of words separated by space
    # return the split results, which is all the words in the file.
    #l = l.read().split()
    #re.split(', |\*|\n', l)
    l = corpustypes
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


global lenwordfile

#THIS FUNCTION RETURNS A LIST OF ALL FILE WORDS ()TYPE OF A DETERMINED FILE AND LENGTH
def allwordslength(length, file):
    #open the file containing the latin vocabulary
    l = open(file, "rt",  encoding="utf-8")
    #convert the file in a list of words separated by space
    # return the split results, which is all the words in the file.
    l = l.read().replace(',','').replace('.','').replace(';','').replace(':','')
    l = l.split()
    #re.split(', |\*|\n', l)

    #print(l)
    #loop trought the l text to get the longest word
    wordlenfile = length
    #if file == "latincorpus.txt":
    #    lenwordfile = open("allwordslengthlatin"+str(length)+".txt", "a",  encoding="utf-8")
    #elif file == "greekcorpus.txt":
    #    lenwordfile = open("allwordslengthgreek"+str(length)+".txt", "a",  encoding="utf-8")
    #elif file == "stringaoriginale.txt":
    #    lenwordfile = open("allwordslengthoriginal"+str(length)+".txt", "a",  encoding="utf-8")
    #else:
    lenwordlist = []
    lenwordfile = open(str(file).replace('.txt', '')+str(length)+".txt", "a",  encoding="utf-8")
    for word in l:
        if len(word) == wordlenfile:
           lenwordlist.append(word)       
    lenwordlist = set(lenwordlist)
    for mot in lenwordlist:
        lenwordfile.write(mot + ' ')
    #maxword1dict = maxworddict[len(maxworddict)-1]
    #maxword1dict = str(maxworddict[0])
    #maxword2dict = maxword1dict[:maxlendict- 2]
    #maxword3dict = maxword1dict[:maxlendict - 3]
    #print(str(length))
    #print(lenwordfile)
    if file == "latincorpus.txt":
        lenwordfilelist = open("allwordslengthlatin"+str(length)+".txt", "rt",  encoding="utf-8")
    elif file == "greekcorpus.txt":
        lenwordfilelist = open("allwordslengthgreek"+str(length)+".txt", "rt",  encoding="utf-8")
    elif file == "stringaoriginale.txt":
        lenwordfilelist = open("allwordslengthoriginal"+str(length)+".txt", "rt",  encoding="utf-8")
    else:
        lenwordfilelist = open(str(file).replace('.txt', '')+str(length)+".txt", "rt",  encoding="utf-8")
    
    lenwordfilelist = lenwordfilelist.read().split()
    return lenwordfilelist

