
#CLTK GREEK
#cltk-1.0.12
#corpus_downloadergr = FetchCorpus(language="grc")
#print(corpus_downloadergr.list_corpora)
#['example_distributed_latin_corpus', 'lat_text_perseus', 'lat_treebank_perseus', 'lat_text_latin_library', 'phi5', 'phi7', 'latin_proper_names_cltk', 'lat_models_cltk', 'latin_pos_lemmata_cltk', 'latin_treebank_index_thomisticus', 'latin_lexica_perseus', 'latin_training_set_sentence_cltk', 'latin_word2vec_cltk', 'latin_text_antique_digiliblt', 'latin_text_corpus_grammaticorum_latinorum', 'latin_text_poeti_ditalia', 'lat_text_tesserae']
#corpusgr = corpus_downloadergr.import_corpus("grc_text_perseus")
#print(str(corpusgr).split())
#from cltk.languages.pipelines import GreekPipeline
#e_pipeline = GreekPipeline()
#e_pipeline.description
#e_pipeline.language
#e_pipeline.language.name
#e_pipeline.processes

import matplotlib.pylab as plt

#CLTK GREEK
#cltk==v0.1.111  
#corpus_importer = CorpusImporter("greek")
#print (corpus_importer.list_corpora)
#corpus_importer.import_corpus("greek_models_cltk")
#corpus_importer.import_corpus("greek_text_perseus")
#reader = get_corpus_reader(corpus_name = 'grc_text_perseus', language = 'greek')
#greek_corpus = get_corpus_reader(corpus_name = 'greek_text_perseus', language = 'greek')
#sentsgr = list(greek_corpus.sents())[50:80]
#for sent in sentsgr:
#  print (sent)

#EXPORT GREEK CORPUS TO TXT FILE
#greekcorpuslist = list(greek_corpus.words())[0:400]
#print(greekcorpuslist)

#greekcorpustypes = set(list(greek_corpus.words()))
#print(len(greekcorpustypes))
#EXPORT SET TO TXT FILE

#gcorpus = open("greekcorpus.txt", "wt",  encoding="utf-8")
    #for each line in the input file
#for word in greekcorpustypes:
	#read replace the string and write to output file
    #gcorpus.write(word + ' ')
#gcorpus.close()



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


#CHARS FREQUENCY DISTRIBUTION OF GREEK CORPUS
def charactersfrequencygrcorpus(sentsgr):
    textnospacecorpus = ""
    for sent in sentsgr:
        #for word in sent:
        textnospacecorpus += sent
    for char in textnospacecorpus:
        if char in ('α', 'ἀ', 'ἁ', 'ἂ','ἃ','ἄ','ἅ','ἆ','ἇ', 'ὰ','ά' ):
            corglyphmapfreq["α"] += 1
        elif char == "β":
            corglyphmapfreq["β"] += 1
        elif char == "δ":
            corglyphmapfreq["δ"] += 1
        elif char == "ζ":
            corglyphmapfreq["ζ"] += 1
        elif char in ('ε', 'ἐ', 'ἑ', 'ἒ', 'ἓ', 'ἔ', 'ἕ','ὲ','έ' ):
            corglyphmapfreq["ε"] += 1
        elif char == "φ":
            corglyphmapfreq["φ"] += 1
        elif char == "γ":
            corglyphmapfreq["γ"] += 1
        elif char in ('η', 'ἠ', 'ἡ', 'ἢ', 'ἣ', 'ἤ', 'ἥ', 'ἦ', 'ἧ', 'ὴ', 'ή'):
            corglyphmapfreq["η"] += 1
        elif char == "λ":
            corglyphmapfreq["λ"] += 1
        elif char == "μ":
            corglyphmapfreq["μ"] += 1
        elif char == "ν":
            corglyphmapfreq["ν"] += 1
        elif char in ('ω', 'ὠ', 'ὡ', 'ὢ', 'ὣ', 'ὤ', 'ὥ', 'ὦ', 'ὧ', 'ὼ' ,'ώ'):
            corglyphmapfreq["ω"] += 1
        elif char == "π":
            corglyphmapfreq["π"] += 1
        elif char == "κ":
            corglyphmapfreq["κ"] += 1
        elif char == "ρ":
            corglyphmapfreq["ρ"] += 1
        elif char == "σ":
            corglyphmapfreq["σ"] += 1
        elif char == "τ":
            corglyphmapfreq["τ"] += 1
        elif char in  ('ὐ','ὑ', 'ὒ', 'ὓ', 'ὔ', 'ὕ','ὖ','ὗ','υ','ὺ','ύ'):
            corglyphmapfreq["υ"] += 1
        elif char == "χ":
            corglyphmapfreq["χ"] += 1
        elif char == "ψ":
            corglyphmapfreq["ψ"] += 1
        elif char == "θ":
            corglyphmapfreq["θ"] += 1
        elif char in ('ο', 'ὀ', 'ὁ', 'ό', 'ὸ', 'ὀ', 'ὄ', 'ὂ', 'ὁ', 'ὅ', 'ὃ', 'ὸ', 'ό'):
            corglyphmapfreq["ο"] += 1
        elif char in ( 'ι', 'ἰ', 'ἱ', 'ἲ', 'ἳ', 'ἴ', 'ἵ', 'ἶ', 'ἷ','ὶ' ,'ί'):
            corglyphmapfreq["ι"] += 1
        elif char == "ξ":
            corglyphmapfreq["ξ"] += 1
    
    print("Greek Corpus' chars frequency \n") 
    #print(corglyphmapfreq)
    #grcorlists = dict(sorted(corglyphmapfreq.items(), key=lambda item: item[1]))
    grcorlists = sorted(corglyphmapfreq.items(), key=lambda item: item[1], reverse=True)
    print("grcorlists")
    #print(grcorlists)
    x, y = zip(*grcorlists) # unpack a list of pairs into two tuples
    plt.plot(x, y)
    plt.show()

#plt.plot(range(len(corglyphmapfreq)), list(corglyphmapfreq.values()), color = 'blue')


    
#... AND WE PERFORM THE SAME WITH ALL EPIGRAPHS' CHARS
def charactersfrequencygr(file):
    text = open(file, "rt", encoding="utf-8")
    text = text.read()
    text = text.split()
    textnospace = ""
    for word in text:
        textnospace += word
    for char in textnospace:
        if char in ('α', 'ἀ', 'ἁ', 'ἂ','ἃ','ἄ','ἅ','ἆ','ἇ', 'ὰ', 	'ά' ):
            epglyphmapfreq["α"] += 1
        elif char == "β":
            epglyphmapfreq["β"] += 1
        elif char == "δ":
            epglyphmapfreq["δ"] += 1
        elif char == "ζ":
            epglyphmapfreq["ζ"] += 1
        elif char in ('ε', 'ἐ', 'ἑ', 'ἒ', 'ἓ', 'ἔ', 'ἕ', 	'ὲ',	'έ' ):
            epglyphmapfreq["ε"] += 1
        elif char == "φ":
            epglyphmapfreq["φ"] += 1
        elif char == "γ":
            epglyphmapfreq["γ"] += 1
        elif char in ('η', 'ἠ', 	'ἡ', 	'ἢ', 	'ἣ', 	'ἤ', 	'ἥ', 	'ἦ', 	'ἧ', 'ὴ', 	'ή'):
            epglyphmapfreq["η"] += 1
        elif char == "λ":
            epglyphmapfreq["λ"] += 1
        elif char == "μ":
            epglyphmapfreq["μ"] += 1
        elif char == "ν":
            epglyphmapfreq["ν"] += 1
        elif char in ('ω', 'ὠ', 	'ὡ', 	'ὢ', 	'ὣ', 	'ὤ', 	'ὥ', 	'ὦ', 	'ὧ', 	'ὼ' 	,'ώ'):
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
        elif char in  ('ὐ', 	'ὑ', 	'ὒ', 	'ὓ', 	'ὔ', 	'ὕ', 'ὖ', 	'ὗ' ,'υ' , 'ὺ', 'ύ' ):
            epglyphmapfreq["υ"] += 1
        elif char == "χ":
            epglyphmapfreq["χ"] += 1
        elif char == "ψ":
            epglyphmapfreq["ψ"] += 1
        elif char == "θ":
            epglyphmapfreq["θ"] += 1
        elif char in ('ο', 'ὀ', 'ὁ', 'ό', 'ὸ', 'ὀ', 'ὄ', 'ὂ', 'ὁ', 'ὅ', 'ὃ', 'ὸ', 'ό'):
            epglyphmapfreq["ο"] += 1
        elif char in ( 'ι', 'ἰ', 	'ἱ', 	'ἲ', 	'ἳ', 	'ἴ', 	'ἵ', 	'ἶ', 	'ἷ', 'ὶ' ,'ί'):
            epglyphmapfreq["ι"] += 1
        elif char == "ξ":
            epglyphmapfreq["ξ"] += 1
    
    print("Epigraph's chars frequency \n") 
    print(dict(sorted(epglyphmapfreq.items(), key=lambda item: item[1])))
