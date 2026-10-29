#THIS PROJECT AIMS TO SOLVE ALL ENCRYPTED SHORT TEXTS WITH UNKNOWN ALPHABETS 
#BY A BRUTE-FORCE APPROACH DECRYPTING
#LETTERS AGAINST A CORPUS/DICTIONARY OF A (ARBITRARILY) CHOSEN LANGUAGE

#IN THE FOLLOWING REALIZATION THE LATIN LANGUAGE HAS BEEN CHOSEN TO START DUE ALL CONSIDERATIONS
#BROUGHT UP IN THE PAPER "ENCRYPTED EPIGRAPHS - A DECRYPTION REPORT OF THE MYSTERIOUS EPIGRAPH IN THE NEAPOLITAN CHURCH OF SANTA MARIA LA NOVA"

#pip install --upgrade [package]==[version]

import io
import re
import nltk
from nltk import word_tokenize
import constraint
from nltk.corpus import udhr
import matplotlib.pylab as plt
#from cltk.tokenize.coptic.params import CopticLanguageVars 
from Palindromes import listPalindromes, isPalindrome
from Replace import *
from CopticCorpus import *
from GreekCorpus import *
from LatinCorpus import *
from WordLength import *
from ConstraintProgramming import *
from Graphs import *
from NLP import *
from Crypto import *


copticfrequency = {
    	"ⲃ": 30,
        "ⲅ": 8,
        "ⲇ": 14,
        "ⲋ": 62,
        "ⲍ": 1,
        "ⲑ": 22,
        "ⲕ": 25,
        "ⲗ": 27,
        "ⲙ": 86,
        "ⲛ": 205,
        "ⲝ": 23,
        "ⲡ": 67,
        "ⲣ": 67,
        "ⲥ": 71,
        "ⲧ": 127,
        "ⲩ": 8,
        "ⲫ": 23,
        "ⲭ": 9,
        "ⲯ": 32,
        "f": 52,
        "x": 44
    }

corcopticfrequency = {
        "ⲁ": 0,
    	"ⲃ": 0,
        "ⲅ": 0,
        "ⲇ": 0,
        "ⲉ": 0,
        "ⲋ": 0,
        "ⲍ": 0,
        "ⲏ": 0,
        "ⲑ": 0,
        "ⲓ": 0,
        "ⲕ": 0,
        "ⲗ": 0,
        "ⲙ": 0,
        "ⲛ": 0,
        "ⲟ": 0,
        "ⲝ": 0,
        "ⲡ": 0,
        "ⲣ": 0,
        "ⲥ": 0,
        "ⲧ": 0,
        "ⲩ": 0,
        "ⲫ": 0,
        "ⲭ": 0,
        "ⲯ": 0,
        "ⲱ": 0,
        "ⳡ": 0,
        "⳨": 0,
        "ⳝ": 0,
        "ⳛ": 0,
        "ⳟ": 0,
        "ⳮ": 0
    }


#CREATE A DICTIONARY TO STORE MAPPING OF ENCRYPTED-DECRYPTED GLYPHS 
# Assign to the first term the list of greek letters, and to the mapped term an empty space.
# according to this list appropriately filled the final charcter replacement will take place, to which the output of the decrypted epigraph will follow

glyphmap = {
  "α": "",
  "β": "",
  "ζ": "",
  "δ": "",
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
  "θ": "",
  "ο": "",
  "ι": "",
  "ξ": ""
}

#CREATE A DICTIONARY TO STORE MAPPING OF LATIN GLYPH-FREQUENCIES

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
  "θ": 0,
  "ο": 0,
  "ι": 0,
  "ξ": 0
}

#CREATE A DICTIONARY TO STORE MAPPING OF THE GREEK CORPUS  GLYPH-FREQUENCIES

corglyphmapfreq = {
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
  "θ": 0,
  "ο": 0,
  "ι": 0,
  "ξ": 0
}

shift = 1


#FUNCTIONS' CALLS

#greekreplace()
#replacegreek()
#greekreplacegreg()
#greekreplacedic()
#regexreplace()
#regexreplacevowels()
#latgreekreplace("egrdic.txt")
#RemoveSpaces("egr.txt")
#skipletters(3, "egr.txt")
#SortText("stringaoriginale.txt")
#longestword("copticbible.txt")
#extracTypes("copticstring.txt")
#longestworddict("latincorpus2.txt")
#charactersfrequency("egr.txt")
#glyphmapfreq = { x:0 for x in glyphmapfreq}
#charactersfrequencylat("stringaoriginale.txt")
#glyphmapfreq = { x:0 for x in glyphmapfreq}
#charactersfrequencylat("gregoriipapaxiii.txt")
#charactersfrequencylat("latindic.txt")
#charactersfrequencygrcorpus(sentsgr)
#charactersfrequencylatcorpus(sents)
#charactersfrequencycoptcorpus()
#finder.ngram_fd.viewitems()  to find bigrams
i = 1
while i < 18:
  #allwordslength(i, "stringaoriginale.txt")
  #allwordslength(i, "greekcorpus.txt")
  #allwordslength(i, "copticbible.txt")
  #patternsearch(i, 'KK')
  #patternsearch(i, 'YY')
  #patternsearch(i, 'U')
  i += 1

#typetokenratio("copticstring2.txt")
#allwordslength(19, "stringaoriginale.txt")
#patternsearch(5, "greekcorpus.txt", 'DEFED')

#extracTypes("copticpalindrome.txt")
#patternsearch(4, "stringaoriginale.txt", 'TOAT')
#patternsearch(4, "stringaoriginale.txt", 'RTOA')

#dittonghisuff("stringaoriginale.txt")
#dittonghipref("stringaoriginale.txt")
#dittonghifr("bcy.txt")
#trittonghifr("bcy.txt")
#dittonghipos("stringaoriginale.txt")
#trittonghipos("stringaoriginale.txt")
#listPalindromes("copticbible.txt")
#extracTypes("latinpalindromes5.txt")
#trittonghipref("gregoriipapaxiii.txt")
#trittonghisuff("gregoriipapaxiii.txt")
#trittonghifr("copticstring2.txt")
#xmlParse('copticbible.xml')
#LatinLetterFreq()
#FrequencyLettersOrig()
#typetokenratio("lux.txt")

#wordChunks("stringaoriginale.txt", 3, "n-2")
#wordChunks("stringaoriginale.txt", 3, "1")
#wordChunks("stringaoriginale.txt", 3, "-1")
word = "rcfcr"
#matchWord(word, "coptic"+str(len(word))+".txt")
#matchWord(word, "allwordslengthgreek"+str(len(word))+".txt")
matchWord(word, "allwordslengthlatin"+str(len(word))+".txt")

