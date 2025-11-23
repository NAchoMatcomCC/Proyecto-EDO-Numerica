import Interpreter.ASTNodes as AST
import Interpreter.Error as Err


class Parser:
    def __init__(self, Tokens):
        self.Tokens = Tokens
        self.IndexLine = 0
        self.Index = 0
        self.Nodes = []
        self.NoErrors = True
        self.MsgErr = []
    
    
    #Parsear por Linea
    def Parse(self):
        
        while self.IndexLine < len(self.Tokens):
            Line = self.__ObtainLine__()
            self.__DeleteIdentations__(Line)
            self.__CreateNode__(Line)
    
    def __ObtainLine__(self, Vlevel = 0):
        if self.IndexLine < len(self.Tokens):
            Line = self.Tokens[self.IndexLine]
            Send = True
            for i in range(Vlevel):
                if Line[i].Type.name != 'Indent':
                    Send = False
            if Send:
                self.IndexLine += 1
                self.Index = 0
                return Line
            return None
    
    def __DeleteIdentations__(self, Tokens, level = 0):
        Delete = True
        if Tokens[0].Type.name == 'Indent':
            Delete = False
        
        idx = []
        
        for i in range(len(Tokens)):
            if Tokens[i].Type.name != 'Indent' or i >= level:
                Delete = True
            
            if Delete and Tokens[i].Type.name == 'Indent':
                idx.append(i)
        
        for i in range(1, len(idx) + 1):
            Tokens.pop(idx[-i])
    
    
    
    # def __ParseDefinedFuntion__(self, Tokens):
    #     Ident = self.__EatToken__(Tokens, 'Identifier').Text
    #     Args = self.__ObtainArgs__(Tokens)
        
    #     return AST.DefFunct(Ident, Args)
    
    
    # def __CreateFunction__(self, Tokens, level = 0):
    #     Key = self.__EatToken__(Tokens, 'KeyWord')
    #     Ident = None
        
    #     #Obtener Identificador
    #     if Key.Text == 'def':
    #         Ident = self.__EatToken__(Tokens, 'Identifier').Text
    #     else:
    #         Ident = Key.Text
        
    #     #Obtener Argumentos
    #     Args = self.__ObtainArgs__(Args, Tokens)
        
    #     #Finalizar Declaracion
    #     if Tokens[self.Index].Text == ':':
    #         self.__EatToken__(Tokens, 'Symbol')
    #     self.__EatToken__(Tokens, 'End')
        
    #     #Obtener Cuerpo de la Declaracion
    #     Body = []
    #     Tokens = self.__ObtainLine__(level + 1)
        
    #     while Tokens != None:
    #         self.__DeleteIdentations__(Tokens)
    #         Expr = self.__ParseExpression__(Tokens, level + 1)
    #         Body.append(Expr)
            
    #         Tokens = self.__ObtainLine__(level + 1)
        
    #     return AST.FunctAssig(Ident, Args, Body)
    
    
    def __ObtainArgs__(self, Tokens):
        
        #Obtener TODOS los Argumentos y ponerlos en linea
        self.__EatToken__(Tokens, Name='(')
        Ind = 1
        NewTkLine = []
        
        while Ind != 0:
            
            if Tokens[self.Index].Text == ')':
                self.__EatToken__(Tokens, Name=')')
                Ind -= 1
                continue
            elif Tokens[self.Index].Text == '(':
                self.__EatToken__(Tokens, Name='(')
                Ind += 1
                continue
            
            Tk = self.__LineAttach__(Tokens)
            
            if Tk == False:
                break
            else:
                Tokens = Tk
            
            NewTkLine.append(self.__EatToken__(Tokens))
        
        #Agregar END al final de los argumentos
        ActInd = self.Index
        NewTkLine.append(Tokens[-1])
        
        #Parsear Argumentos
        self.Index = 0
        Expr = self.__ParseExpression__(NewTkLine)
        self.Index = ActInd
        return Expr
    
    def __LineAttach__(self, Tokens):
        while Tokens[self.Index].Text == 'End':
            
            Tokens = self.__ObtainLine__()
            
            if Tokens == None:
                return False
            else:
                self.__DeleteIdentations__(Tokens)
        
        return Tokens
    
    
    def __CreateNode__(self, Tokens):
        
        if Tokens[self.Index].Type.name == 'Identifier':
            
            #Es una asignacion
            if Tokens[self.Index + 1].Text == '=':
                Expr = self.__ParseExpression__(Tokens)
                self.Nodes.append(Expr)
            
            #Funciones Definidas
            # elif Tokens[self.Index + 1].Text == '(':
            #     Expr = self.__ParseDefinedFuntion__(Tokens)
            #     self.Nodes.append(Expr)
        
        #Funciones indefinidas
        # elif Tokens[self.Index].Type.name == 'KeyWord':
        #     Expr = self.__CreateFunction__(Tokens)
        #     self.Nodes.append(Expr)
        
        
        elif Tokens[self.Index].Type.name == 'End':
            #Do nothing
            pass
        
        #Operacion no soportada
        else:
            self.MsgErr.append(Err.Error(f'Operacion no soportada en la linea {Tokens[self.Index].Line}'))
            self.NoErrors = False
    
    
    def __EatToken__(self, Tokens , Type = None, Name = None):
        
        if Type != None and Tokens[self.Index].Type.name != Type:
            self.MsgErr.append(Err.Error(f'Tipo de Token inesperado: Tipo: {Tokens[self.Index].Type.name}, Esperado: {Type}, linea: {Tokens[self.Index].Line}'))
            self.NoErrors = False
        
        if Name != None and Tokens[self.Index].Text != Name:
            self.MsgErr.append(Err.Error(f'Nombre de Token inesperado: Nombre: {Tokens[self.Index].Text}, Esperado: {Name}, linea: {Tokens[self.Index].Line}'))
            self.NoErrors = False
        
        Tk = Tokens[self.Index]
        self.__MoveNext__()
        return Tk
    
    def __MoveNext__(self, steps = 1):
        self.Index += steps
    
    
    #Funciones para
    #Parsear
    #Expresiones
    #Aritmeticas y Funciones
    
    def __ParseExpression__(self, Tokens, level = 0):
        
        Nodes = []
        
        while Tokens[self.Index].Type.name != 'End':
            Node = self.__Assignation__(Tokens, level)
            if Tokens[self.Index].Text == ',':
                self.__EatToken__(Tokens)
            Nodes.append(Node)
        
        return Nodes
    
    
    def __Assignation__(self, Tokens, level):
        Expr = None
        if Tokens[self.Index].Type.name == 'Identifier' and Tokens[self.Index + 1].Text == '=':
            ident = self.__EatToken__(Tokens, 'Identifier').Text
            self.__EatToken__(Tokens, Name='=')
            Expr = AST.Assignation(ident, self.__LogicOp__(Tokens, level))
        else:
            Expr = self.__LogicOp__(Tokens, level)
        return Expr
    
    def __LogicOp__(self, Tokens, level):
        Expr = self.__Equals__(Tokens, level)
        op = Tokens[self.Index].Text
        while op == 'and' or op == 'or' or op == '&&' or op == '||':
            self.__EatToken__(Tokens)
            Expr = AST.LogicOperators(Expr, self.__Equals__(Tokens, level), op)
            op = Tokens[self.Index].Text
        return Expr
    
    def __Equals__(self, Tokens, level):
        Expr = self.__Comparative__(Tokens, level)
        op = Tokens[self.Index].Text
        while op == '==' or op == '!=':
            self.__EatToken__(Tokens)
            Expr = AST.AritBinOp(Expr, self.__Comparative__(Tokens, level), op)
            op = Tokens[self.Index].Text
        return Expr
    
    def __Comparative__(self, Tokens, level):
        Expr = self.__ParseBin1__(Tokens, level)
        op = Tokens[self.Index].Text
        while op == '>' or op == '>=' or op == '<' or op == '<=':
            self.__EatToken__(Tokens)
            Expr = AST.AritBinOp(Expr, self.__ParseBin1__(Tokens, level), op)
            op = Tokens[self.Index].Text
        return Expr
    
    def __ParseBin1__(self, Tokens, level):
        Expr = self.__ParseBin2__(Tokens, level)
        op = Tokens[self.Index].Text
        while op == '+' or op == '-':
            self.__EatToken__(Tokens)
            Expr = AST.AritBinOp(Expr, self.__ParseBin2__(Tokens, level), op)
            op = Tokens[self.Index].Text
        return Expr
    
    def __ParseBin2__(self, Tokens, level):
        Expr = self.__ParseExp__(Tokens, level)
        op = Tokens[self.Index].Text
        while op == '*' or op == '/':
            self.__EatToken__(Tokens)
            Expr = AST.AritBinOp(Expr, self.__ParseExp__(Tokens, level), op)
            op = Tokens[self.Index].Text
        return Expr
    
    def __ParseExp__(self, Tokens, level):
        Expr = self.__ParseUnary__(Tokens, level)
        op = Tokens[self.Index].Text
        while op == '**':
            self.__EatToken__(Tokens)
            Expr = AST.AritBinOp(Expr, self.__ParseUnary__(Tokens, level), op)
            op = Tokens[self.Index].Text
        return Expr
    
    def __ParseUnary__(self, Tokens, level):
        op = Tokens[self.Index].Text
        Expr = None
        if op == '!' or op == '-':
            self.__EatToken__(Tokens)
            Expr = AST.AritUnaryOp(self.__Parentesis__(Tokens, level), op)
        else:
            Expr = self.__Parentesis__(Tokens, level)
        return Expr
    
    def __Parentesis__(self, Tokens, level):
        op = Tokens[self.Index].Text
        Expr = None
        if op == '(':
            self.__EatToken__(Tokens)
            Expr = AST.AritUnaryOp(self.__Equals__(Tokens, level), op)
            self.__EatToken__(Tokens, Name=')')
        else:
            Expr = self.__Claps__(Tokens, level)
        return Expr
    
    def __Claps__(self, Tokens, level):
        op = Tokens[self.Index].Text
        Expr = None
        if op == '[':
            self.__EatToken__(Tokens)
            Expr = AST.AritUnaryOp(self.__Equals__(Tokens, level), op)
            self.__EatToken__(Tokens, Name=']')
        else:
            Expr = self.__Primary__(Tokens, level)
        return Expr
    
    def __Primary__(self, Tokens, level):
        
        if Tokens[self.Index].Type.name == 'Number':
            
            value = self.__EatToken__(Tokens)
            return AST.Primary(value)
        
        elif Tokens[self.Index].Type.name == 'Identifier':
            
            # if Tokens[self.Index + 1].Text == '(':
            #     Expr = self.__ParseDefinedFuntion__(Tokens)
            #     return Expr
            # else:
            value = self.__EatToken__(Tokens)
            return AST.Primary(value)
        
        # elif Tokens[self.Index].Type.name == 'KeyWord':
        #     Expr = self.__CreateFunction__(Tokens, level)
        #     return Expr
        
        # elif Tokens[self.Index].Type.name == 'Special':
        #     value = self.__EatToken__(Tokens)
        #     return AST.SpecialFunct(value, self.__ParseExpression__(Tokens, level))
        
        else:
            self.MsgErr.append(Err.Error(f'Error de Token Primario sin clasificacion. Nombre:{Tokens[self.Index].Text}, Tipo: {Tokens[self.Index].Type.name}, linea: {Tokens[self.Index].Line}'))
            self.NoErrors = False
            return None




