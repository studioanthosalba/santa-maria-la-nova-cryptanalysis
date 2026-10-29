
#REPLACE ALL LATIN CHARACHTERS CONTAINED IN THE ENCRYPTED EPYGRAPH BY GREEK ONES (pay particular attention in
#matching vowels)
#this operation is necessary to avoid following scenario:
# text = "abc cb aadba" replace 1. a with b, 2. b with d, 3. c with a and 4. d with b. Output: 
#1."bbc cb bbdbb"
#2. "ddc cd ddddd"
#3. "dda ad ddddd"
#4. "bba ab bbbbb", which is not the desired result

def greekreplacescgr(file):
    e = open(file, "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("egrscgr.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('a', 'τ').replace('d', 'ε').replace('e', 'ε').replace('f', 'π').replace('o', 'α').replace('p', 'π').replace('r', 'ν').replace('t', 'ρ').replace('v', 'μ'))
    e.close()
    eg.close()

def greekreplace(file):
    e = open(file, "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("soluzione.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('a', 'α').replace('b', 'β').replace('c', 'ζ').replace('d', 'δ').replace('e', 'ε').replace('f', 'φ').replace('g', 'γ').replace('i', 'η').replace('l', 'λ').replace('m', 'μ').replace('n', 'ν').replace('o', 'ω').replace('p', 'π').replace('q', 'κ').replace('r', 'ρ').replace('s', 'σ').replace('t', 'τ').replace('u', 'υ').replace('v', 'χ').replace('s', 'ς').replace('w', 'κ').replace('z', 'θ').replace('h', 'ψ').replace('x', 'ξ').replace('y', 'ι'))
    e.close()
    eg.close()


#THIS FUNCTION REPLACES THE GREEK-WRITTEN ORIGINAL FILE WITH LATIN LETTERS ACCORDING TO THE LETTER FREQUENCY RANKING 
# OF BOHEMIAN
def bohreplacegreek():
    e = open("egra.txt", "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("stringaoriginalebohemian.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('α', 'i-').replace('β', 'b/f-').replace('ζ', 'v/l-').replace('δ', 'z/d/m-').replace('ε', 'n/l-').replace('φ', 'd/m-').replace('γ', 'y/p-').replace('η', 'e-').replace('λ', 'u/j-').replace('μ','s/t-').replace('ν', 'n/l-').replace('ω', 'h/c-').replace('π', 'j/k/u-').replace('κ','p/y-').replace('ρ', 'o/s-').replace('σ','u/k/c-').replace('τ','s/t-').replace('υ','a/o-').replace('χ','h/y/r/b-').replace('ψ','r/b/h-').replace('ξ','r/h/y-').replace('ς','r/h/y-').replace('κ','f/g-').replace('θ','r/b/h-'))
    e.close()
    eg.close()

#THIS FUNCTION REPLACES LETTERS FROM THE ORIGINAL STRING ACCORDING TO LETTER FREQUENCY DISTRIBUTION
#FOR THE ANCIENT GREEK LANGUAGE BASED ON THE PERSEUS CORPUS
def replacegreek():
    eο = open("stringaoriginale.txt", "rt", encoding="utf-8")
    #output file to write the result to
    egrtemp = open("egrtemp.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in eο:
	    #read replace the string and write to output file
        egrtemp.write(line.replace('a', 'τ/α-').replace('b', 'σ/κ/λ/δ-').replace('c', 'λ/δ/γ-').replace('d', 'ω/φ/η-').replace('e', 'ρ/π/μ-').replace('f', 'λ/δ/γ-').replace('g', 'ω/φ/η-').replace('i', 'ν-').replace('l', 'λ/δ/γ-').replace('m', 'π/μ-').replace('n', 'σ/κ/λ/δ-').replace('o', 'χ/β/ζ-').replace('p', 'φ/η/χ/β-').replace('q', 'ζ/ψ-').replace('r', 'ε/ρ-').replace('s', 'ω/φ/η-').replace('t', 'ρ/π/μ-').replace('u', 'τ/α-').replace('v', 'υ-').replace(' ', '---'))
    eο.close()
    egrtemp.close()

# THIS FUNCTION CREATES A FILE WHERE EACH WORD IS REPLACED WITH A NUMBER, IN ORDER TO AVOID CONFUSION
# GIVEN BY LETTERS

def regexreplace(file):
    e = open(file, "rt", encoding="utf-8")
    #output file to write the result to
    eg = open("regexreplace.txt", "wt",  encoding="utf-8")
    #for each line in the input file
    for line in e:
	    #read replace the string and write to output file
        eg.write(line.replace('a', '0').replace('b', '1').replace('c', '2').replace('d', '3').replace('e', 'F').replace('f', '4').replace('g', '5').replace('i', 'G').replace('l', '6').replace('m', '7').replace('n', '8').replace('o', '4').replace('p', '9').replace('q', 'O').replace('r', 'A').replace('s', 'B').replace('t', 'C').replace('u', 'H').replace('v', 'D').replace('z', 'E'))
    e.close()
    eg.close()

# THIS FUNCTION CREATES A FILE WHERE EACH WORD IS REPLACED WITH A PSEUDO-REGEX
# IT DIFFERENTIATES ONLY BETWEEN VOCALS AND CONSONANTS

def regexreplacevowels():
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
                  eg.write(word.replace('b', '1').replace('c', '2').replace('d', '3').replace('f', '4').replace('g', '5').replace('l', '6').replace('m', '7').replace('n', '8').replace('p', '9').replace('q', 'O').replace('r', 'A').replace('s', 'B').replace('t', 'C').replace('v', 'D').replace('z', 'E'))
    e.close()
    eg.close()


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