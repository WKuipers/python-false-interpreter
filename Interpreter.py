__author__ = 'Ties'

import Statement as S

state = S.Statement(raw_input())
# state = S.Statement("[3 5+]a:5a;-")
# state = S.Statement("[3-]a:3 5+[[$-1][$.]#]z:%{ dit is een comment }99 9[1-$][\$@$@$@$@\/*=[1-$$[%\ 1-$@]?0=[\$.\]?]?]#")
# state = S.Statement("1$[$][$@+$.]#")1
stack = []
print state.statement
variables = []
while len(variables)<26:
    variables.append(None)
state.execute(stack,variables)
print "Stack: " + str(stack)
print "Variables: " + str(variables)
print "Syntax: " + state.printtree()
counter=0
print "LaTeX: " + state.printlatex(counter)
print "Counter: " + str(counter)