__author__ = 'Ties Robroek, Jan Martens en Wietse Kuipers'

import Statement as S
import sys
import argparse

#Parse arguments
parser = argparse.ArgumentParser(description="Python interpreter for the FALSE language")
parser.add_argument("-f", "--file", type=file, help="Specify a file to read FALSE program from")
parser.add_argument("-l", "--latex", action="store_true", default=False, help="Output LaTeX code for proof tree corresponding to program")
parser.add_argument("-o", "--outfile", default="output.tex", help="Specify an output file for the generated LaTeX code. The default is output.tex")
parser.add_argument("-i", "--input", help="Specify a file to take a string input from.")
parser.add_argument("--recursionlimit", help="Set the recursion limit for large computations", type=int, default=999)
args = vars(parser.parse_args())

sys.setrecursionlimit(args["recursionlimit"])

if args["file"] != None:
    data=args["file"].read().replace('\n','').replace('\t','').replace(chr(184),'').replace(chr(248),chr(195))
    print "DATA =" + data
else:
    data = raw_input().replace('\n','').replace('\t','').replace(chr(184),'').replace(chr(248),chr(195))
if args.has_key("input"):
    with open (args["input"], "r") as file:
        input=file.read().replace('\n','')
print "Input: " + input
state = S.Statement(data)
stack = []
print state.statement
variables = {}
try:
    state.execute(stack, variables)
except Exception as exc:
    print "EXCEPTION: " + str(exc)
    exit()

print "\nExecution successfull:"
print " Stack: " + str(stack)
print " Variables: " + str(variables)
print " Syntax: " + state.printtree()

if args.get("latex"):
    with open ("header.tex", "r") as file:
        header=file.read()

    busstree = header +  state.printbuss() + "\DP\n\\end{document}"
    with open ("output.tex", "w") as file:
        file.write(busstree)
    print "LaTeX was written to " + args["outfile"]
