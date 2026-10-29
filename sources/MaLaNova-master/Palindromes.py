
#THIS FUNCTION TELLS IF THE STRING IS PALINDROME OR NOT 
def isPalindrome(s):
    return s == s[::-1]


#THIS FUNCTION TAKES A TEXT FILE AND RETURN A LIST OF PALINDROMES SORTED BY WORD LENGTH
def listPalindromes(file):
    if file == "allwordslengthlatin.txt" or file == "allwordslengthgreek.txt":
        i = 3
        while i < 16:
            infile = open(file[0:19]+str(i)+".txt", "rt", encoding="utf-8")
            infile = infile.read()
            infile = infile.split()
            if file == "allwordslengthlatin.txt":
                outfile = "palindromilat.txt"
            elif file == "allwordslengthgreek.txt":
                outfile = "palindromigre.txt"
            for word in infile:
                if isPalindrome(word):
                    with open(outfile, "a",  encoding="utf-8") as f: 
                      f.write(word +'\n')
            i+=1
    else:
        outfile = "palindromiorig.txt" # the output file is the same for coptic and for the original string
        infile = open(file, "rt", encoding="utf-8")
        infile = infile.read()
        infile = infile.split()
        for word in infile:
                if isPalindrome(word):
                    with open(outfile, "a",  encoding="utf-8") as f: 
                      f.write(word +'\n')
