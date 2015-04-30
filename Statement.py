__author__ = 'Ties'
import Statement as S
import sys

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

        if self.a[0] in "abcdefghijklmnopqrstuvwxyz":
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
            self.b = self.statement[len(self.a)]
            if self.b[0] == '[':
                close = self.findclosure(self.statement[len(self.a):],'[',']')
                while len(self.b) < close:
                    # print self.b + str(close) + " " + str(len(self.b))
                    self.b = self.b + self.statement[len(self.a)+len(self.b)]
                self.b = self.b + self.statement[len(self.a)+len(self.b)]
                if self.statement[len(self.a)+len(self.b)] == '#':
                    self.b = self.b + self.statement[len(self.a)+len(self.b)]
            elif self.b in "abcdefghijklmnopqrstuvwxyz":
                self.b = self.b + self.statement[len(self.a)+len(self.b)]
            elif self.b != "?":
                self.b = ""

        print "Statement: " + self.a + " " + self.b + " Code: " + self.statement
         #Composition
        if len(self.statement) > len(self.a)+len(self.b):
            # print "COMP"
            self.children.append(S.Statement(self.a+self.b))
            self.children.append(S.Statement(self.statement[len(self.a)+len(self.b):]))
            self.b = ""
        elif len(self.b) > 0:
            #Var declaration
            if self.b[0] in "abcdefghijklmnopqrstuvwxyz":
                self.a = self.a[1:-1]
                self.children.append(S.Statement(self.a))
            #If
            elif self.b == "?":
                self.a = self.a[1:-1]
                self.children.append(S.Statement(self.a))
            #While
            else:
                self.a = self.a[1:-1]
                self.b = self.b[1:-2]
                self.children.append(S.Statement(self.a))
                self.children.append(S.Statement(self.b))
                self.repeat = 0

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
        # print str(stack) + " on " + self.printtree()
        if len(self.children)>0:
            if len(self.b) > 0:
                if self.b[0] in "abcdefghijklmnopqrstuvwxyz":
                    variables[ord(self.b[0])-97] = self.children[0]
                elif self.b == "?":
                    if stack.pop(len(stack)-1) !=0:
                        self.children[0].execute(stack,variables)
                else:
                    self.children[0].execute(stack,variables)
                    while stack.pop(len(stack)-1)!=0:
                        self.repeat = self.repeat + 1
                        self.children[1].execute(stack,variables)
                        self.children[0].execute(stack,variables)
            else:
                for child in self.children:
                    child.execute(stack,variables)
        else:

            #Basic arithmetic operators
            if self.a == '+':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) + a)
            elif self.a == '-':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) - a)
            elif self.a == '*':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) * a)
            elif self.a == '/':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) / a)
            elif self.a == '_':
                stack.append(-stack.pop(len(stack)-1))

            elif self.a == '.':
                print stack.pop(len(stack)-1)
            elif self.a[0] == '"':
                print self.a[1:-1]

            elif self.a[0] in "abcdefghijklmnopqrstuvwxyz":
                variables[ord(self.a[0])-97].execute(stack,variables)

            elif self.a == '!':
                0

            # Conditions
            elif self.a == '=':
                if stack.pop(len(stack)-1)==stack.pop(len(stack)-1):
                    stack.append(-1)
                else:
                    stack.append(0)

            #Basic stack operations
            elif self.a == '$':
                stack.append(stack[len(stack)-1])

            elif self.a == '\\':
                a = stack.pop(len(stack)-1)
                b = stack.pop(len(stack)-1)
                stack.append(a)
                stack.append(b)
            elif self.a == '@':
                a = stack.pop(len(stack)-1)
                b = stack.pop(len(stack)-1)
                c = stack.pop(len(stack)-1)
                stack.append(b)
                stack.append(a)
                stack.append(c)
            elif self.a == '%':
                stack.pop(len(stack)-1)
            else:
                stack.append(int(self.a))

    def printtree(self):
        if len(self.children)==0:
            return "[" + self.a + "]"
        else:
            if len(self.b)>0:
                if self.b[0] in "abcdefghijklmnopqrstuvwxyz":
                    return " (" + self.children[0].printtree() + "->" + self.b + ") "
                elif self.b == "?":
                    return " (" + self.children[0].printtree() + ") "
                else:
                    return " {" + self.children[0].printtree() + " : " + self.children[1].printtree() + "} "
            else:
                return self.children[0].printtree() + self.children[1].printtree()

    def printlatex(self,counter):
        if len(self.children)==0:
            return self.a
        else:
            if len(self.b)>0:
                if self.b[0] in "abcdefghijklmnopqrstuvwxyz":
                    return " (" + self.children[0].printlatex(counter) + "->" + self.b + ") "
                elif self.b == "?":
                    return " (" + self.children[0].printlatex(counter) + ") "
                else:
                    return " {" + self.children[0].printlatex(counter) + " : " + self.children[1].printlatex(counter) + "} "
            else:
                return self.children[0].printlatex(counter) + self.children[1].printlatex(counter)

    def __repr__(self):
        return  self.statement