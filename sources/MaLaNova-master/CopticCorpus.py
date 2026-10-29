
#CLTK COPTIC
#cltk==v0.1.111  (as in youtube tutorials)
#from cltk.corpus.utils.importer import CorpusImporter
#corpus_importer = CorpusImporter("coptic")
#print(corpus_importer.list_corpora)
#corpus_importer.import_corpus("coptic_models_cltk")
#corpus_importer.import_corpus("coptic_text_scriptorium")
#from cltk.corpus.readers import get_corpus_reader
#reader = get_corpus_reader(corpus_name = 'grc_text_perseus', language = 'greek')
#coptic_corpusreader = get_corpus_reader(corpus_name = 'coptic_text_scriptorium', language = 'coptic')
#sentscopt = list(coptic_corpusreader.sents())[50:90]
#for sent in sentscopt:
#    print (sent)

#copticlist = sorted(copticfrequency.items(), key=lambda item: item[1], reverse=True)
#x, y = zip(*copticlist) # unpack a list of pairs into two tuples
#plt.plot(x, y)
#plt.show()
#plt.plot(range(len(copticfrequency)), list(copticfrequency.values()), color = 'blue')

import matplotlib.pylab as plt

#COPTIC GLYPHS MAP
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

# THE MAPPING WILL BE FILLED WITH GREEK GLYPHS BECAUSE THE LIBRARY MATPLOTLIB IS NOT ABLE TO SHOW COPTIC GLYPHS ON THE X-AXIS
corcopticfrequency = {
        "Α": 0, #Ⲁ
    	"Β": 0, #Ⲃ
        "Γ": 0, #Ⲅ
        "Δ": 0, #Ⲇ
        "Ε": 0, #Ⲉ
        "ς": 0, #Ⲋ
        "Ζ": 0, #Ⲍ 
        "Η": 0, #Ⲏ
        "Θ": 0, #Ⲑ
        "Ι": 0, #Ⲓ
        "Κ": 0, #Ⲕ 
        "Λ": 0, #Ⲗ
        "Μ": 0,  #Ⲙ
        "Ν": 0, #Ⲛ
        "Ο": 0, #Ⲟ
        "ζ": 0, #Ⲝ
        "Π": 0, #Ⲡ
        "Ρ": 0, #Ⲣ
        "C": 0, #Ⲥ 
        "Τ": 0, #Ⲧ
        "Υ": 0, #Ⲩ
        "Φ": 0, #Ⲫ
        "Χ": 0, #Ⲭ
        "W": 0, #Ⲯ
        "Ω": 0, #Ⲱ
        "F": 0, #Ⳡ
        "ST": 0, #⳨
        "Os": 0, #Ⳝ
        "D": 0, #Ⳛ
        "[": 0, #Ⳟ
        "xx": 0 #ⳮ
    } 


#CHARS FREQUENCY DISTRIBUTION OF COPTIC CORPUS
def charactersfrequencycoptcorpus():
    copt = open("copticbible.txt", "rt", encoding="utf-8")
    copt = copt.read().split()
    textnospacecorpuscopt = ""
    for word in copt:
        textnospacecorpuscopt += word
    for char in textnospacecorpuscopt:
        if char == "Ⲁ":
            corcopticfrequency["Α"] += 1
        elif char == "Ⲃ":
            corcopticfrequency["Β"] += 1
        elif char == "Ⲅ":
            corcopticfrequency["Γ"] += 1
        elif char == "Ⲇ":
            corcopticfrequency["Δ"] += 1
        elif char == "Ⲉ":
            corcopticfrequency["Ε"] += 1
        elif char == "Ⲋ":
            corcopticfrequency["ς"] += 1
        elif char == "Ⲍ":
            corcopticfrequency["Ζ"] += 1
        elif char == "Ⲏ":
            corcopticfrequency["Η"] += 1
        elif char == "Ⲑ":
            corcopticfrequency["Θ"] += 1
        elif char == "Ⲓ":
            corcopticfrequency["Ι"] += 1
        elif char == "Ⲕ":
            corcopticfrequency["Κ"] += 1
        elif char == "Ⲗ":
            corcopticfrequency["Λ"] += 1
        elif char == "Ⲙ":
            corcopticfrequency["Μ"] += 1
        elif char == "Ⲛ":
            corcopticfrequency["Ν"] += 1
        elif char == "Ⲟ":
            corcopticfrequency["Ο"] += 1
        elif char == "Ⲝ":
            corcopticfrequency["ζ"] += 1
        elif char == "Ⲡ":
            corcopticfrequency["Π"] += 1
        elif char == "Ⲣ":
            corcopticfrequency["Ρ"] += 1
        elif char == "Ⲥ":
            corcopticfrequency["C"] += 1
        elif char == "Ⲧ":
            corcopticfrequency["Τ"] += 1
        elif char == "Ⲩ":
            corcopticfrequency["Υ"] += 1
        elif char == "Ⲫ":
            corcopticfrequency["Φ"] += 1
        elif char == "Ⲭ":
            corcopticfrequency["Χ"] += 1
        elif char == "Ⲯ":
            corcopticfrequency["W"] += 1
        elif char == "Ⲱ":
            corcopticfrequency["Ω"] += 1
        elif char == "Ⳡ":
            corcopticfrequency["F"] += 1
        elif char == "⳨":
            corcopticfrequency["ST"] += 1
        elif char == "Ⳝ":
            corcopticfrequency["Os"] += 1
        elif char == "Ⳛ":
            corcopticfrequency["D"] += 1
        elif char == "Ⳟ":
            corcopticfrequency["["] += 1
        elif char == "ⳮ":
            corcopticfrequency["xx"] += 1
        else:
            if char not in corcopticfrequency:
                corcopticfrequency.update({char: 1})
            else:
                corcopticfrequency[char]+= 1 
    print("Coptic Corpus' chars frequency \n") 
    #print(corglyphmapfreq)
    #grcorlists = dict(sorted(corglyphmapfreq.items(), key=lambda item: item[1]))
    for key in list(corcopticfrequency):
        if corcopticfrequency[key]< 3 or key == "."  or key == "-" or key == "]":
           corcopticfrequency.pop(key)
    coptcorlists = sorted(corcopticfrequency.items(), key=lambda item: item[1], reverse=True)
    print("coptcorlists")
    print(coptcorlists)
    x, y = zip(*coptcorlists) # unpack a list of pairs into two tuples
    plt.plot(x, y)
    plt.show()

    corcopticfrequency2 = {}
def charactersfrequencycoptcorpus2():
    copt = open("copticbible.txt", "rt", encoding="utf-8")
    copt = copt.read().split()
    textnospacecorpuscopt = ""
    for word in copt:
        textnospacecorpuscopt += word
    for char in textnospacecorpuscopt:
        if char not in corcopticfrequency:
            corcopticfrequency.update({char: 1})
        else:
            corcopticfrequency[char]+= 1 
    print("Coptic Corpus' chars frequency \n") 
    #print(corglyphmapfreq)
    #grcorlists = dict(sorted(corglyphmapfreq.items(), key=lambda item: item[1]))
    coptcorlists = sorted(corcopticfrequency.items(), key=lambda item: item[1], reverse=True)
    print("coptcorlists")
    print(coptcorlists)
    x, y = zip(*coptcorlists) # unpack a list of pairs into two tuples
    plt.plot(x, y)

    plt.show()