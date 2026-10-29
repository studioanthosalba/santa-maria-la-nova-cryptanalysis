
from nltk.corpus import udhr
import matplotlib.pylab as plt
import numpy as np
import nltk
import io
import re
from scipy import stats, special

#SCIPY CLUSTER HIERARCHY

#from scipy.cluster.hierarchy import dendrogram, linkage

#from matplotlib import pyplot as plot
#word = "Desossiribonucleico"
#word = word.split()
#X = [[char] for char in word]
#Z = linkage(X, 'ward')
#fig = plot.figure(figsize=(25, 10))
#dn = dendrogram(Z)
#Z = linkage(X, 'single')
#fig = plot.figure(figsize=(25, 10))
#dn = dendrogram(Z)
#plot.show()

#KOMLMOGOROV-SMIRNOV TEST TO ASSESS SIMILARITY OF TWO DISTRIBUTIONS

def KStest (vec1, vec2):
    print("Kolmogorv-Smirnov test:" + str(stats.kstest(vec1, vec2)))
    print("KS-two samples test:" + str(stats.ks_2samp(vec1, vec2)))


#STATISTICAL TESTS TO ASSESS SIMILARITY OF TWO DISTRIBUTIONS WITH SAME LENGTH

def Stest (vec1, vec2):
    obs = np.array([vec1, vec2])
    #print("Discrete Fischer test:" + str(stats.fisher_exact(obs)))
    print("KL-divergence test:" + str(special.kl_div(vec1, vec2)))
    print("X2 test:" + str( stats.chi2_contingency(obs)))

#GRAPH OF LETTER DISTRIBUTION FOR INPUT STRING

def FrequencyLetters(file):
    #open the file containing the latin vocabulary
    epigr = open(file, "rt", encoding="utf-8")
    #convert the file in a list of words separated by space
    # return the split results, which is all the words in the file.
    epigr = epigr.read()#.split()
    cfdr = nltk.FreqDist(
              (epigr, char)
              for word in epigr
                for char in word
                    if re.search(r'([a-z])',char))
    print(cfdr)
    cfdr.plot(cumulative=False)
    #print(glyphmap)
    #epigr.close()


#This is useful to show the anagram hypothesis inconsistency - Frequency Graph of words in original string
def FrequencyWordsOrig():
    text = open("stringaoriginale.txt", "rt", encoding="utf-8")
    text = text.read().split()
    fdist1 = nltk.FreqDist(text)
    print(fdist1)
    fdist1.most_common(50)
    fdist1.plot(50, cumulative=False)

#Frequency graph of sorted words
def FrequencySortWords():
    text2 = open("sortedwords_anagram.txt", "rt", encoding="utf-8")
    text2 = text2.read().split()
    fdist2 = nltk.FreqDist(text2)
    print(fdist2)
    fdist2.most_common(50)
    fdist2.plot(50, cumulative=False)

# Frequency graph of epigraph of Pope Gregory XIII
def FrequencyWordGregory():
    text3 = open("gregoriipapaxiii.txt", "rt", encoding="utf-8")
    text3 = text3.read().split()
    fdist3 = nltk.FreqDist(text3)
    print(fdist3)
    fdist3.most_common(50)
    fdist3.plot(50, cumulative=False)
    #return dictionary


#LANGUAGE COMPARISON WORD LENGTH

def CompareWordLengths():
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


#LANGUAGE COMPARISON LETTER FREQUENCY
def CompareLetterFrequency():
    languages = ['Latin_Latina-v2-Latin1', 'German_Deutsch-Latin1', 'Italian_Italiano-Latin1',
       'Luxembourgish_Letzebuergeusch-Latin1', 'Hungarian_Magyar-Latin1']
    cfde = nltk.ConditionalFreqDist(
              (lang, char)
              for lang in languages
              for word in udhr.words(lang)
              for char in word
              if re.search(r'([a-z])',char))
    cfde.plot(cumulative=False)

#LANGUAGE COMPARISON LETTER FREQUENCY GREEK GENERAL

def GreekLetterFreq():
    cfdeg = nltk.FreqDist(
              ('Greek_Ellinika-UTF8', char)
              for word in udhr.words('Greek_Ellinika-UTF8')
              for char in word
              if re.search(r'([^A-Ω0-9])',char)
              )
    cfdeg.plot(cumulative=False)

#LANGUAGE COMPARISON LETTER FREQUENCY LATIN GENERAL

def LatinLetterFreq():
    cfdel = nltk.FreqDist(
              ('Italian_Italiano-Latin1', char)
              for word in udhr.words('Italian_Italiano-Latin1')
              for char in word
              if re.search(r'([a-z])',char)
              )
    cfdel.plot(cumulative=False)


#GRAPH OF LETTER DISTRIBUTION FOR ORIGINAL STRING

def FrequencyLettersOrig():
    #open the file containing the latin vocabulary
    epigr = open("moderncoptic.txt", "rt", encoding="utf-8")
    #convert the file in a list of words separated by space
    # return the split results, which is all the words in the file.
    epigr = epigr.read()#.split()
    cfdr = nltk.FreqDist(
              (epigr, char)
              for word in epigr
                for char in word
                    if re.search(r'([a-z])',char))
    cfdr.plot(cumulative=False)
    #print(glyphmap)
    #epigr.close()


#GRAPH OF LETTER DISTRIBUTION FOR ORIGINAL ADIACENT EPIGRAPH
def FrequencyLetterGregory():
    #open the file containing the latin vocabulary
    epigra = open("gregoriipapaxiii.txt", "r")
    #convert the file in a list of words separated by space
    # return the split results, which is all the words in the file.
    #epigr = epigr.read().split()
    cfdra = nltk.FreqDist(
              (epigra, char)
              for word in epigra
              for char in word
              if re.search(r'([a-z])',char))
    cfdra.plot(cumulative=False)
    #print(glyphmap)
    epigra.close()

#Frequency graph of random text
#text4 = open("randomtext.txt", "r")
#text4a = nltk.FreqDist(
#          (text4, char)
#          for word in text4
#          for char in word
#          if re.search(r'([a-z])',char))
#text4a.plot(cumulative=False)
#text4.close()
##return dictionary

##Frequency graph of random text2
#text5 = open("randomtext2.txt", "r")
#text5a = nltk.FreqDist(
#          (text5, char)
#          for word in text5
#          for char in word
#          if re.search(r'([a-z])',char))
#text5a.plot(cumulative=False)
#text5.close()
#return dictionary
#nltk.FreqDist(text3).plot()
#output translated text
#write translated text into a new txt file

