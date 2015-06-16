__author__ = 'Ties'
import Statement as S
import sys
import copy

class Statement:
    def __init__(self,statement):
        self.statement =  statement
        self.children = []
        self.compile()


    def compile(self):
        #Remove whitespaces at front
        while self.statement[0] == ' ':
            self.statement = self.statement[1:]

        while self.statement[0] == '{':
            self.statement = self.statement[self.findclosure(self.statement,'{','}')+1:]

        #Read first char
        self.a = str(self.statement[0])
        self.b = ""

        #Read additional digits if constant
        if self.a[0] in "0123456789":
            self.statement = self.statement + " "
            while self.statement[len(self.a)] in "0123456789":
                self.a = self.a + self.statement[len(self.a)]
            self.statement = self.statement[:-1]

        if self.a[0] == '\'':
            self.a = self.a + self.statement[len(self.a)]

        if self.a[0] == '"':
            close = self.findclosure(self.statement[len(self.a)-1:],'','"')
            while len(self.a) != close:
                self.a = self.a + self.statement[len(self.a)]
            self.a = self.a + self.statement[len(self.a)]

        if self.a[0] == '[':
            close = self.findclosure(self.statement[len(self.a)-1:],'[',']')
            while len(self.a) != close:
                self.a = self.a + self.statement[len(self.a)]
            self.a = self.a + self.statement[len(self.a)]
            self.encapsulate = S.Statement(self.a[1:-1])

        # print "Statement: " + self.a + " " + " Code: " + self.statement
         #Composition
        if len(self.statement) > len(self.a):
            # print "COMP"
            self.children.append(S.Statement(self.a))
            self.children.append(S.Statement(self.statement[len(self.a):]))

    def findclosure(self,string,begin,end):
        cap = 1
        for i in range(1,len(string)):
            if string[i]==end:
                cap = cap-1
            if string[i]==begin:
                cap = cap+1
            if cap == 0:
                return i
    #     SYNTAX ERROR
        print "syntax error"

    def execute(self,stack,variables):
        self.prestack = str(stack)
        self.prevariables = str(variables)
        # print str(stack) + " on " + self.printtree()
        if len(self.children)==2:
            for child in self.children:
                child.execute(stack,variables)
        else:
            ### ARITHMETIC OPERATIONS:
            # +: Add
            # Input: n, m
            # Output: m+n
            if self.a == '+':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) + a)

            # -: Substract
            # Input: n, m
            # Output: m-n
            elif self.a == '-':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) - a)

            # *: Multiply
            # Input: n, m
            # Output: m*n
            elif self.a == '*':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) * a)

            # /: Divide
            # Input: n, m
            # Output: m/n
            elif self.a == '/':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) / a)

            # _: Negative
            # Input: n
            # Output: -n
            elif self.a == '_':
                stack.append(-stack.pop(len(stack)-1))

            # .: Print integer
            # Input: n
            # Output:
            elif self.a == '.':
                print stack.pop(len(stack)-1)

            # ,: Print char
            # Input: n
            # Output:
            elif self.a == ',':
                print chr(stack.pop(len(stack)-1))

            # : Print string
            # Input:
            # Output:
            elif self.a[0] == '"':
                print self.a[1:-1]

            # {letter}: Put/Execute lambda variable
            # Input:
            # Output:
            elif self.a[0] in "abcdefghijklmnopqrstuvwxyz":
                stack.append(self.a[0])

            elif self.a[0]==':':
                a = stack.pop(len(stack)-1)
                if a in "abcdefghijklmnopqrstuvwxyz":
                    variables[a] = stack.pop(len(stack)-1)
                else:
                    raise Exception("Try to assign to illegal variable!")

            elif self.a[0]==';':
                stack.append(variables[stack.pop(len(stack)-1)])

            # !: Execute lambda variable
            # Input: []
            # Output:
            elif self.a == '!':
                self.children.append(stack.pop(len(stack)-1))
                self.children[0].execute(stack,variables)

            # ?: Execute lambda variable conditionally (IF)
            # Input: [] n
            # Output:
            elif self.a == '?':
                a = stack.pop(len(stack)-1)
                if stack.pop(len(stack)-1)!=0:
                    a.execute(stack,variables)

            # #: Execute lambda variable conditionally repeatedly (WHILE)
            # Input: [] [] n
            # Output:
            elif self.a == "#":
                a = stack.pop(len(stack)-1)
                b = stack.pop(len(stack)-1)
                b.execute(stack,variables)
                self.repetitions = 0
                self.stacks = []
                self.variables = []
                while(stack.pop(len(stack)-1)!=0):
                    self.repetitions = self.repetitions + 1
                    child = copy.copy(a)
                    self.children.append(child)
                    child.execute(stack,variables)
                    child = copy.copy(b)
                    self.children.append(child)
                    child.execute(stack,variables)

            ### CONDITIONAL OPERATIONS:
            # =: Equals
            # Input: n, m
            # Output: n==m
            elif self.a == '=':
                if stack.pop(len(stack)-1)==stack.pop(len(stack)-1):
                    stack.append(-1)
                else:
                    stack.append(0)

            # >: Greater Than
            # Input: n, m
            # Output: n>m
            elif self.a == '>':
                if stack.pop(len(stack)-1)<stack.pop(len(stack)-1):
                    stack.append(-1)
                else:
                    stack.append(0)

            ###BASIC STACK OPERATIONS
            # $: Duplicate top
            # Input: n
            # Output: n, n
            elif self.a == '$':
                stack.append(stack[len(stack)-1])

            # $: Pick
            # Input: n
            # Output: m
            elif len(self.a) == 1 and ord(self.a[0]) == 195:
                stack.append(stack[len(stack)-1-stack.pop(len(stack)-1)])

            # \: Swap
            # Input: n, m
            # Output: n, m
            elif self.a == '\\':
                a = stack.pop(len(stack)-1)
                b = stack.pop(len(stack)-1)
                stack.append(a)
                stack.append(b)

            # @: Rotate
            # Input: n, m, o
            # Output: m, o, n
            elif self.a == '@':
                a = stack.pop(len(stack)-1)
                b = stack.pop(len(stack)-1)
                c = stack.pop(len(stack)-1)
                stack.append(b)
                stack.append(a)
                stack.append(c)

            # %: Remove
            # Input: n
            # Output:
            elif self.a == '%':
                stack.pop(len(stack)-1)

            elif self.a == 'Q':
                stack.append(stack[len(stack)-2-stack.pop(len(stack)-1)])

            ### INTEGER:
            # {integer}: Integer
            # Input:
            # Output: {integer}
            elif self.a.isdigit():
                stack.append(int(self.a))

            elif self.a[0] == '\'':
                stack.append(ord(self.a[1]))

            ### STATEMENT:
            else:
                if hasattr(self,'encapsulate'):
                    stack.append(self.encapsulate)
                else:
                    raise Exception("Undefined statement '" + self.a + "', ASCII code '" + str(ord(self.a[0])) + "'!")
        self.poststack = str(stack)
        self.postvariables = str(variables)

    def printtree(self):
        if len(self.children)==2:
            return self.children[0].printtree() + self.children[1].printtree()
        else:
            return "[" + self.a + "]"

    def printlatex(self):
        if len(self.children)>0:
            string = ""

            if hasattr(self,'repetitions'):
                return self.makeWhile(0)
            else:
                for child in self.children:
                    string = string + child.printlatex()
                return "\infer{<" \
                   + self.format(self.a) + self.format(self.statement[len(self.a):]) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
                   + ">\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)\
                   + ")}{" + string + "}"
        else:
            if self.a[0] == '!':
                return self.children[0].printlatex()
            return "<"+ self.format(self.a) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
                   + ">\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)+">"

    def makeWhile(self,i):
        if i+2<=len(self.children):
            return self.children[i].printlatex() + self.children[i+1].printlatex() \
            +  "\infer{" \
            + self.format(self.a) + self.format(self.statement[len(self.a):]) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
            + ">\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)\
            + "\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)\
            + ")}{" + self.makeWhile(i+2) + "}"
        else:
            return "\infer{<" \
            + self.format(self.a) + self.format(self.statement[len(self.a):]) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
            + ">\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)\
            + ")}{}"
        return 0

    def printbuss(self):
            if len(self.children)>0:
                string = ""
                if self.a[0] == '!' and len(self.children)==1:
                    return "\\UnaryInfC{$"+ self.children[0].printbuss() + "$}\n"
                elif hasattr(self,'repetitions'):
                    return self.makeWhileb(0)
                else:
                    for child in self.children:
                        string = string + child.printbuss()
                    return string + "\BinaryInfC{$<" \
                       + self.format(self.a) + self.format(self.statement[len(self.a):]) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
                       + ">\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)\
                       + ")$}\n"
            else:
                return "\\AxiomC{$\\langle "+ self.format(self.a) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
                       + "\\rangle\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)+")$}\n"

    def makeWhileb(self,i):
        if i+2<=len(self.children):
            return self.children[i].printbuss() + self.children[i+1].printbuss() +  self.makeWhileb(i+2) \
            + "\TrinaryInfC{$<" \
            + self.format(self.a) + self.format(self.statement[len(self.a):]) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
            + ">\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)\
            + ")$}\n"
        else:
            return "\\AxiomC{$<"+ self.format(self.a) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
                       + ">\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)+">$}\n"
            # return "\infer{<" \
            # + self.format(self.a) + self.format(self.statement[len(self.a):]) + "," + self.format(self.prevariables) + "," + self.format(self.prestack) \
            # + ">\\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.poststack)\
            # + ")}{}"
        return 0

    def whileBody(self):
        return self.format(self.a) + self.format(self.statement[len(self.a):])

    def __repr__(self):
        return  self.statement

    def format(self,string):
        string = string.replace(str('\\'),"\\backslash")
        string = string.replace(str('^'),"$\\textasciicircum$")
        for char in "$_&%#":
            string = string.replace(str(char),"\\"+str(char))
        return string.replace(str(' '),"\\:")