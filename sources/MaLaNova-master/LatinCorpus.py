
#CLTK LATIN
#cltk-1.0.12
#from cltk.data.fetch import FetchCorpus
#import cltk.lemmatize.lat 

#corpus_downloader = FetchCorpus(language="lat")
#corpus_downloader.list_corpora
#['example_distributed_latin_corpus', 'lat_text_perseus', 'lat_treebank_perseus', 'lat_text_latin_library', 'phi5', 'phi7', 'latin_proper_names_cltk', 'lat_models_cltk', 'latin_pos_lemmata_cltk', 'latin_treebank_index_thomisticus', 'latin_lexica_perseus', 'latin_training_set_sentence_cltk', 'latin_word2vec_cltk', 'latin_text_antique_digiliblt', 'latin_text_corpus_grammaticorum_latinorum', 'latin_text_poeti_ditalia', 'lat_text_tesserae']
#corpuslat = corpus_downloader.import_corpus("lat_text_latin_library")

#from cltk.languages.pipelines import LatinPipeline
#a_pipeline = LatinPipeline()
#a_pipeline.description
#a_pipeline.language
#Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a')
#a_pipeline.language.name
#a_pipeline.processes

#CLTK LATIN
#cltk==v0.1.111
#from cltk.corpus.utils.importer import CorpusImporter
#corpus_importer = CorpusImporter("latin")
#print (corpus_importer.list_corpora)
#corpus_importer.import_corpus("latin_models_cltk")
#corpus_importer.import_corpus("latin_text_latin_library")
#from cltk.corpus.readers import get_corpus_reader
#reader = get_corpus_reader(corpus_name = 'grc_text_perseus', language = 'greek')
#latin_corpus = get_corpus_reader(corpus_name = 'latin_text_latin_library', language = 'latin')
#sents = list(latin_corpus.sents())#[40:770]
#for sent in sents:
#    print (sent)

#EXPORT LATIN CORPUS TO TXT FILE
#latincorpustypes = set(list(latin_corpus.words()))
#print(len(greekcorpustypes))
#EXPORT SET TO TXT FILE

#lcorpus = open("latincorpus2.txt", "wt",  encoding="utf-8")
    #for each line in the input file
#for word in latincorpustypes:
	#read replace the string and write to output file
    #lcorpus.write(word + ' ')
#lcorpus.close()

#CREATE A DICTIONARY TO STORE MAPPING OF ENCRYPTED-DECRYPTED GLYPHS 
# Assign to the first term the list of greek letters, and to the mapped term an empty space.
# according to this list appropriately filled the final charcter replacement will take place, to which the output of the decrypted epigraph will follow

import matplotlib.pylab as plt

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


#CHARS FREQUENCY DISTRIBUTION OF LATIN CORPUS
def charactersfrequencylatcorpus(sents):
    textnospacecorpuslat = ""
    for sent in sents:
       for word in sent:
           textnospacecorpuslat += word
    for char in textnospacecorpuslat:
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

    print("Latin Corpus' chars frequency \n") 
    #print(corglyphmapfreq)
    #grcorlists = dict(sorted(corglyphmapfreq.items(), key=lambda item: item[1]))
    latcorlists = sorted(glyphmapfreq.items(), key=lambda item: item[1], reverse=True)
    print("latcorlists")
    print(latcorlists)
    x, y = zip(*latcorlists) # unpack a list of pairs into two tuples
    plt.plot(x, y)
    plt.show()

    
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
    
    print("Latin chars frequency \n") 

    print(dict(sorted(glyphmapfreq.items(), key=lambda item: item[1])))
    print(sorted(glyphmapfreq.values(), reverse=True)) 