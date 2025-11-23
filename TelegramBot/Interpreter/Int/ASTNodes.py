import Interpreter.Error as Err

#Clase Objecto
class ConcreteObject:
    def __init__(self):
        pass
    
    def Accept(self, Visitor):
        return Visitor.Visit(self)


#Clase Visitor Para Calcular
class Visitor:
    def __init__(self):
        self.NoErrors = True
        self.MsgErr = []
    
    
    def Visit(self, Object):
        
        
        if isinstance(Object, DefFunct):
            
            pass
        elif isinstance(Object, FunctAssig):
            
            pass
        elif isinstance(Object, SpecialFunct):
            
            pass
        
        elif isinstance(Object, Assignation):
            Ident = Object.Identifier
            D = Object.Der.Accept(self)
            
            #Agregar a la memoria la nueva variable con el nuevo valor
            
            return D
        
        elif isinstance(Object, LogicOperators):
            I = Object.Izq.Accept(self)
            D = Object.Der.Accept(self)
            
            if Object.Op == 'and' or Object.Op == '&&':
                return I and D
            elif Object.Op == 'or' or Object.Op == '||':
                return I or D
        
        elif isinstance(Object, AritBinOp):
            I = Object.Izq.Accept(self)
            D = Object.Der.Accept(self)
            
            try:
                if Object.Op == '+':
                    return I + D
                elif Object.Op == '-':
                    return I - D
                elif Object.Op == '*':
                    return I * D
                elif Object.Op == '/':
                        return I / D
                elif Object.Op == '**':
                    return I ** D
                elif Object.Op == '>':
                    return I > D
                elif Object.Op == '>=':
                    return I >= D
                elif Object.Op == '<':
                    return I < D
                elif Object.Op == '<=':
                    return I <= D
                elif Object.Op == '==':
                    return I == D
                elif Object.Op == '!=':
                    return I != D
            except ZeroDivisionError:
                self.NoErrors = False
                self.MsgErr.append(Err.Error(f'Error de Division por Cero -> {I} / {D}'))
            except OverflowError:
                self.NoErrors = False
                self.MsgErr.append(Err.Error(f'Desvordamiento Superior (OFL) -> {I} {Object.Op} {D}'))
            
            return 0
        
        elif isinstance(Object, AritUnaryOp):
            D = Object.Der.Accept(self)
            
            if Object.Op == '!':
                if D:
                    return False
                else:
                    return True
            elif Object.Op == '-':
                return -D
            elif Object.Op == '(':
                return D
            elif Object.Op == '[':
                return D
        
        elif isinstance(Object, Primary):
            Token = Object.Value
            
            if Token.Type.name == 'Number':
                return float(Token.Text)
            elif Token.Type.name == 'Identifier':
                
                #Extraer de la memoria el valor de la variable
                pass






#Clase Visitor Para Checkear Semanticamente
class CheckVisitor:
    def __init__(self):
        self.NoErrors = True
        self.MsgErr = []
    
    def Visit(self, Object):
        
        if isinstance(Object, DefFunct):
            
            pass
        elif isinstance(Object, FunctAssig):
            
            pass
        elif isinstance(Object, SpecialFunct):
            
            pass
        
        elif isinstance(Object, Assignation):
            Ident = Object.Identifier
            D = Object.Der.Accept(self)
            
            return D
        
        elif isinstance(Object, LogicOperators):
            I = Object.Izq.Accept(self)
            D = Object.Der.Accept(self)
            
            if (Object.Op == 'and' or Object.Op == '&&') and I == 'Bool' and D == 'Bool':
                return 'Bool'
            elif (Object.Op == 'or' or Object.Op == '||')  and I == 'Bool' and D == 'Bool':
                return 'Bool'
            else:
                self.NoErrors = False
                self.MsgErr.append(Err.Error(f'Error semantico detectado -> {I} {Object.Op} {D}'))
                return 'Unknow'
        
        elif isinstance(Object, AritBinOp):
            I = Object.Izq.Accept(self)
            D = Object.Der.Accept(self)
            
            if (Object.Op == '+' or Object.Op == '-' or Object.Op == '*' or Object.Op == '/'
                or Object.Op == '**') and I == 'Number' and D == 'Number':
                
                return 'Number'
            
            elif (Object.Op == '>' or Object.Op == '>=' or Object.Op == '<'
                or Object.Op == '<=') and I == 'Number' and D == 'Number':
                
                return 'Bool'
            
            elif (Object.Op == '==' or Object.Op == '!=') and I == D:
                
                return 'Bool'
            
            else:
                self.NoErrors = False
                self.MsgErr.append(Err.Error(f'Error semantico detectado -> {I} {Object.Op} {D}'))
                return 'Unknow'
        
        elif isinstance(Object, AritUnaryOp):
            D = Object.Der.Accept(self)
            
            if Object.Op == '!' and D == 'Bool':
                return 'Bool'
            elif Object.Op == '-' and D == 'Number':
                return 'Number'
            elif Object.Op == '(':
                return D
            elif Object.Op == '[':
                return D
            else:
                self.NoErrors = False
                self.MsgErr.append(Err.Error(f'Error semantico detectado -> {Object.Op} {D}'))
                return 'Unknow'
        
        elif isinstance(Object, Primary):
            Token = Object.Value
            
            if Token.Type.name == 'Number':
                return 'Number'
            elif Token.Type.name == 'Identifier':
                #Extraer de la memoria el valor de la variable
                #Verificar el tipo
                pass
















#Operaciones
class AritBinOp(ConcreteObject):
    def __init__(self, Izq, Der, op):
        super().__init__()
        self.Izq = Izq
        self.Der = Der
        self.Op = op

class AritUnaryOp(ConcreteObject):
    def __init__(self, Der, op):
        super().__init__()
        self.Der = Der
        self.Op = op

class Assignation(ConcreteObject):
    def __init__(self, Identifier, Der):
        super().__init__()
        self.Identifier = Identifier
        self.Der = Der

class Primary(ConcreteObject):
    def __init__(self, Value):
        super().__init__()
        self.Value = Value

class FunctAssig(ConcreteObject):
    def __init__(self, Identifier, Arguments, Body):
        super().__init__()
        self.Identifier = Identifier
        self.Arguments = Arguments
        self.Body = Body

class DefFunct(ConcreteObject):
    def __init__(self, Identifier, *args):
        super().__init__()
        self.Identifier = Identifier
        self.Arguments = args

class SpecialFunct(ConcreteObject):
    def __init__(self, Ident, Value):
        super().__init__()
        self.Ident = Ident
        self.Value = Value

class LogicOperators(ConcreteObject):
    def __init__(self, Izq, Der, op):
        super().__init__()
        self.Izq = Izq
        self.Der = Der
        self.Op = op