import Interpreter.Error as Err
from enum import Enum

class TokenType(Enum):
    Identifier = 1
    # KeyWord = 2
    Number = 2
    Operation = 3
    Symbol = 4
    EndLine = 5
    Indent = 6
    WhiteSpace = 7
    # Special = 9
    Unknow = 8
    End = 9

class Token:
    def __init__(self, Text, Type, Line):
        self.Text = Text
        self.Type = Type
        self.Line = Line


class Lexer:    
    def __init__(self, Text):
        self.Text = Text
        self.Index = 0
        self.Line = 0
        
        self.Tokens = []
        self.TokenLine = []
        
        # self.KeyWord = ['def', 'if', 'for']
        # self.Special = ['return']
        
        self.NoErrors = True
        self.MsgErr = []
    
    
    def Tokenize(self):
        while True:
            
            ident = self.__MoveAhead__()
            
            if self.__GetType__(ident) == 'Number':
                while self.__GetType__(self.__GetNext__()) == 'Number':
                    ident += self.__MoveAhead__()
                
                if self.__GetNext__() == '.':
                    ident += self.__MoveAhead__()
                    
                    while self.__GetType__(self.__GetNext__()) == 'Number':
                        ident += self.__MoveAhead__()
                
                self.TokenLine.append(Token(ident, TokenType.Number, self.Line))
            
            elif self.__GetType__(ident) == 'Letter':
                while self.__GetType__(self.__GetNext__()) == 'Letter' or self.__GetType__(self.__GetNext__()) == 'Number' or self.__GetNext__() == '_' or self.__GetNext__() == '.':
                    ident += self.__MoveAhead__()
                
                if ident == 'and' or ident == 'or':
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                # elif self.__Contain__(self.Special, ident):
                #     self.TokenLine.append(Token(ident, TokenType.Special, self.Line))
                # elif self.__Contain__(self.Keywords, ident):
                #     self.TokenLine.append(Token(ident, TokenType.KeyWord, self.Line))
                else:
                    self.TokenLine.append(Token(ident, TokenType.Identifier, self.Line))
            
            elif self.__GetType__(ident) == 'Symbol':
                
                if ident == '+':
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                elif ident == '-':
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                elif ident == '*':
                    if self.__GetNext__() == '*':
                        ident += self.__MoveAhead__()
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                elif ident == '/':
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                elif ident == '=':
                    if self.__GetNext__() == '=':
                        ident += self.__MoveAhead__()
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                elif ident == '<':
                    if self.__GetNext__() == '=':
                        ident += self.__MoveAhead__()
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                elif ident == '>':
                    if self.__GetNext__() == '=':
                        ident += self.__MoveAhead__()
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                
                elif ident == ',':
                    self.TokenLine.append(Token(ident, TokenType.Symbol, self.Line))
                elif ident == ':':
                    self.TokenLine.append(Token(ident, TokenType.Symbol, self.Line))
                elif ident == '(' or ident == ')':
                    self.TokenLine.append(Token(ident, TokenType.Symbol, self.Line))
                elif ident == '[' or ident == ']':
                    self.TokenLine.append(Token(ident, TokenType.Symbol, self.Line))
                elif ident == '!':
                    if self.__GetNext__() == '=':
                        ident += self.__MoveAhead__()
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                elif ident == '&' and self.__GetNext__() == '&':
                    ident += self.__MoveAhead__()
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                elif ident == '|' and self.__GetNext__() == '|':
                    ident += self.__MoveAhead__()
                    self.TokenLine.append(Token(ident, TokenType.Operation, self.Line))
                else:
                    self.NoErrors = False
                    self.MsgErr.append(Err.Error(f'Caracter {ident} inesperado en la linea {self.Line}'))
                    self.TokenLine.append(Token(ident, TokenType.Unknow, self.Line))
            
            elif self.__GetType__(ident) == 'LineJump':
                
                self.TokenLine.append(Token('End', TokenType.End, self.Line))
                self.Line += 1
                self.Tokens.append(self.TokenLine)
                self.TokenLine = []
            
            elif self.__GetType__(ident) == 'Space':
                if self.__GetType__(self.__GetNext__()) == 'Space' and self.__GetType__(self.__GetNext__(1)) == 'Space':
                    ident += self.__MoveAhead__()
                    ident += self.__MoveAhead__()
                    self.TokenLine.append(Token(ident, TokenType.Indent, self.Line))
                    #No hay Espacios en Blanco por ser INNECESARIOS
            else:
                self.NoErrors = False
                self.MsgErr.append(Err.Error(f'Caracter Vacio No Posee Clasificacion, linea: {self.Line}'))
                self.TokenLine.append(Token(ident, TokenType.Unknow, self.Line))
            
            if self.__End__(self.Index) == False:
                self.TokenLine.append(Token('End', TokenType.End, self.Line))
                self.Tokens.append(self.TokenLine)
                break
    
    
    def __MoveAhead__(self):
        char = self.Text[self.Index]
        self.Index += 1
        return char
        
    def __End__(self, idx, steps = 0):
        return idx + steps < len(self.Text)
    
    def __GetNext__(self, steps = 0):
        if self.__End__(self.Index + steps):
            return self.Text[self.Index + steps]
    
    #Obtener El tipo de Datos con Manejo de Caracteres
    def __GetType__(self, char):
        
        if char == None:
            return 'None'
        
        elif str.isspace(char):
            if char == '\n':
                return 'LineJump'
            else:
                return 'Space'
        
        elif str.isnumeric(char):
            return 'Number'
        
        elif str.isidentifier(char):
            return 'Letter'
        
        else:
            return 'Symbol'
    
    # #Contain Method
    # def __Contain__(self, Objs, element):
    #     for object in Objs:
    #         if object == element:
    #             return True
    #     return False