
#THIS CHUNK OF CODE MAKES USE OF CONSTRAINT PROGRAMMING PARADIGM TO SOLVE OUR PROBLEM
# TO BE DEVELOPED LATER
import constraint

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
  "ψ",
  "θ",
  "ο", 
  "ι",
  "ξ"])

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
#def epigraphdecrypt(glyphep, glyphdic):
   # pass

#problem.addConstraint(AllDifferentConstraint())
#problem.addConstraint(epigraphdecrypt, ['glyphep','glyphdic'])

#solutions = problem.getSolutions()

# Easier way to print and see all solutions
# for solution in solutions:
#    print(solution)

# Prettier way to print and see all solutions
#length = len(solutions)
#print("(glyphep,glyphdic) ∈ {", end="")
#for index, solution in enumerate(solutions):
    #if index == length - 1:
    #    print("({},{})".format(solution['glyphep'], solution['glyphdic']), end="")
    #else:
      #  print("({},{}),".format(solution['glyphep'], solution['glyphdic']), end="")
#print("}")


