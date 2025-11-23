import telebot
import telebot.types as tp
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

import Interpreter.Lexer as Lx
import Interpreter.Parser as Ps
import Interpreter.ASTNodes as AST
import Tools.Tools as Tls

import numpy as np
import matplotlib.pyplot as plt


API_TOKEN = "8028863934:AAFxrMjKDNLJ60CoQ2_dtiLcYdRW0dI6HgQ"
state_storage = StateMemoryStorage()  # In-memory state storage
bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage)


Methods = ['RK4', 'EM', 'Graf']
Functs = ['Der-Velocidad', 'Distancia', 'Velocidad']
Zeros = ['SEC', 'BS', 'BIQI', 'RF']
Data = {
    'Method': Methods[0],
    'Funct': Functs[0],
    'Zero': Zeros[0],
    'Parameters': []
}

class MyStates(StatesGroup):
    Inic = State()
    Param = State()
    Isoc = State()
    Zero = State()


def VerifyMethod(call):
    for i in Methods:
        if call == i:
            return True
    return False

def VerifyFunct(call):
    for i in Functs:
        if call == i:
            return True
    return False

def VerifyZeros(call):
    for i in Zeros:
        if call == i:
            return True
    return False


@bot.message_handler(commands=['start'])
def Inicialize(message):
    
    state = bot.get_state(message.from_user.id, message.chat.id)
    
    if state != MyStates.Inic.name:
        bot.send_message(message.chat.id, 'Bot corriendo...')
    else:
        bot.send_message(message.chat.id, 'Iniciando parametros por defecto...')
    
    bot.set_state(message.from_user.id, MyStates.Inic, message.chat.id)
    Data = {'Method': Methods[0], 'Funct': Functs[0], 'Zero': Zeros[0], 'Parameters': []}
    #Crear Script de Funciones Basicas

@bot.message_handler(func= lambda msg : msg.text == '/graf' and bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Inic.name)
def SelectGrafMethod(msg):
    #Create Markup
    bt1 = tp.InlineKeyboardButton('Euler Mejorado', callback_data='EM')
    bt2 = tp.InlineKeyboardButton('Runge-Kutta 4', callback_data='RK4')
    bt3 = tp.InlineKeyboardButton('Graficar(normal)', callback_data='Graf')
    markup = tp.InlineKeyboardMarkup()
    markup.add(bt1)
    markup.add(bt2)
    markup.add(bt3)
    
    bot.send_message(msg.chat.id, text='Selecciona uno de los siguientes metodos para graficar', reply_markup=markup)

@bot.message_handler(func= lambda msg : msg.text == '/isoclina' and bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Inic.name)
def IsoclinaListParam(msg):
    # XLeftrg, XRightrg, YDownrg, YUprg, F, seg = 0.5, fsize= (10,10), SeeVectors = True, SeeLines = True
    text = '''Introduzca en un mensaje el "valor" los parametros en orden correspondiente separados por coma:\n
            XLeft: Limite Izquierdo en el eje x\n
            XRight: Limite Derecho en el eje x\n
            YDown: Limite Inferior en el eje y\n
            YUp: Limite Superior en el eje y'''
    bot.send_message(msg.chat.id, text)
    bot.set_state(msg.from_user.id, MyStates.Isoc, msg.chat.id)

@bot.callback_query_handler(func= lambda call : VerifyMethod(call.data))
def PrintMethodParam(call):
    
    bot.answer_callback_query(call.id, f'Ejecutando {call.data} para la funcion {Data["Funct"]}')
    Data['Method'] = call.data
    
    text = '''Introduzca en un mensaje el "valor" los parametros en orden correspondiente separados por coma:\n
    XLeft: Limite Izquierdo en el eje x\n
    XRight: Limite Derecho en el eje x\n'''
    
    if call.data == 'RK4' or call.data == 'EM':
        text += '   y: Coordenada en y del punto inicial\n'
    
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)
    bot.set_state(call.from_user.id, MyStates.Param, call.message.chat.id)

@bot.message_handler(func= lambda msg : bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Param.name)
def GetMethodParam(msg):
    
    F = Data['Method']
    
    if F == 'RK4':
        Funct = Tls.RungeKutta4
        Cargs = 3
    elif F == 'EM':
        Funct = Tls.EulerMejorado
        Cargs = 3
    elif F == 'Graf':
        Funct = Tls.Graficar
        Cargs = 2
    
    ObtainGrafwithParam(msg, Funct, Cargs)

@bot.message_handler(commands=['select'])
def SelectFunction(msg):
    
    markup = tp.InlineKeyboardMarkup()
    
    for F in Functs:
        button = tp.InlineKeyboardButton(F, callback_data= F)
        markup.add(button)
    
    Text = '''Selecciona una de las siguientes funciones:\n
    (Por defecto: "Der-Velocidad")'''
    
    bot.send_message(msg.chat.id, Text, reply_markup = markup)

@bot.callback_query_handler(func= lambda call : VerifyFunct(call.data))
def FunctionQueries(call):
    
    bot.answer_callback_query(call.id, f'{call.data} establecido')
    Data['Funct'] = call.data

@bot.message_handler(func = lambda msg : bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Isoc.name)
def GetIsocParam(msg):
    
    ObtainGrafwithParam(msg, Tls.Graf_Isoclina, 4)

@bot.message_handler(commands=['zero'])
def SelectZeroMethod(msg):
    #Create Markup
    bt1 = tp.InlineKeyboardButton('Biseccion', callback_data='BS')
    bt2 = tp.InlineKeyboardButton('Biseccion/Interpolacion', callback_data='BIQI')
    bt3 = tp.InlineKeyboardButton('Regula Falsi', callback_data='RF')
    bt4 = tp.InlineKeyboardButton('Secante', callback_data='SEC')
    markup = tp.InlineKeyboardMarkup()
    markup.add(bt1)
    markup.add(bt2)
    markup.add(bt3)
    markup.add(bt4)
    
    bot.send_message(msg.chat.id, text='Selecciona uno de los siguientes metodos para hallar una raiz', reply_markup=markup)


@bot.callback_query_handler(func= lambda call : VerifyZeros(call.data))
def ZerosQueries(call):
    
    bot.answer_callback_query(call.id, f'Ejecutando {call.data} para la funcion {Data["Funct"]}')
    Data['Zero'] = call.data
    
    text = '''Introduzca en un mensaje el "valor" los parametros en orden correspondiente separados por coma:\n
    XLeft: Limite Izquierdo en el eje x\n
    XRight: Limite Derecho en el eje x\n'''
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)
    bot.set_state(call.from_user.id, MyStates.Zero, call.message.chat.id)

@bot.message_handler(func= lambda msg : bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Zero.name)
def SelectZeroMethod(msg):

    F = Data['Zero']
    
    if F == 'SEC':
        Funct = Tls.SecantMethod
        Cargs = 2
    elif F == 'BS':
        Funct = Tls.Bisection
        Cargs = 2
    elif F == 'BIQI':
        Funct = Tls.Hibrid_Bis_IQI
        Cargs = 2
    elif F == 'RF':
        Funct = Tls.RegulaFalsi
        Cargs = 2
    
    ObtainGrafwithParam(msg, Funct, Cargs)



def ObtainGrafwithParam(msg, Funct, CArgs):
    
    bot.send_message(msg.chat.id, 'Procesando...')
    
    #Excepciones no compatibles
    if Data['Funct'] == 'Der-Velocidad' and Funct == Tls.Graficar:
            bot.send_message(msg.chat.id, f'Metodo Grafica no soporta Funciones F(X,Y)')
            return
    
    
    #Obtain Text Parameters
    Text = '(' + msg.text + ')'
    #Tokenizar Parameters
    Lexer = Lx.Lexer(Text)
    Lexer.Tokenize()
    Tks = Lexer.Tokens
    
    if Lexer.NoErrors == False:
        ErrText = Lexer.MsgErr[0].Error
        bot.send_message(msg.chat.id, 'Lexer -> ' + ErrText)
        return
    
    #Parsear
    Parser = Ps.Parser(Tks)
    Parser.IndexLine = 1
    Nodes = Parser.__ObtainArgs__(Tks[0])
    
    if Parser.NoErrors == False:
        ErrText = Parser.MsgErr[0].Error
        bot.send_message(msg.chat.id, 'Parser -> ' + ErrText)
        return
    
    #Visitor Semantico
    for n in Nodes:
        Visitor = AST.CheckVisitor()
        if n.Accept(Visitor) == 'Unknow':
            ErrText = Visitor.MsgErr[0].Error
            bot.send_message(msg.chat.id, 'Check Semantic -> ' + ErrText)
            return
    
    #Visitor Operacional
    Args = []
    for n in Nodes:
        Visitor = AST.Visitor()
        Val = n.Accept(Visitor)
        
        if Visitor.NoErrors == False:
            ErrText = Visitor.MsgErr[0].Error
            bot.send_message(msg.chat.id, 'Operation -> ' + ErrText)
        else:
            Args.append(Val)
    
    #Verificar si estan todos los argumentos
    if len(Args) != CArgs:
        bot.send_message(msg.chat.id, f'Recived Arguments -> Se esperaban {CArgs} argumentos. Se obtuvieron {len(Args)}')
    else:
        
        #Manejo de errores
        #try:
        if bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Isoc.name:
            CallIsoclina(Args)
        elif bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Param.name:
                CallGrafMethod(Funct, Args)
        elif bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Zero.name:
            CallZero(msg, Funct, Args)
        # except OverflowError as e:
        #     bot.send_message(msg.chat.id, f'Error -> {e}')
        # except ZeroDivisionError as e:
        #     bot.send_message(msg.chat.id, f'Error -> {e}')
        # except TypeError as e:
        #     bot.send_message(msg.chat.id, f'Error -> {e}')
        # except ValueError as e:
        #     bot.send_message(msg.chat.id, f'Error -> {e}')
        
        
        #Mostrar Grafica
        with open('Figura.png', 'rb') as Img:
            bot.send_photo(msg.chat.id, Img)
        
        bot.set_state(msg.from_user.id, MyStates.Inic, msg.chat.id)



def CallIsoclina(Args):
    
    if Args[0] > Args[1]:
        Val = Args[0]
        Args[0] = Args[1]
        Args[1] = Val
    
    if Args[2] > Args[3]:
        Val = Args[2]
        Args[2] = Args[3]
        Args[3] = Val
    
    ParamFunct = Tls.DictFunct[Data['Funct']]
    Tls.Graf_Isoclina(*Args, ParamFunct)

def CallGrafMethod(F, Args):
    
    if Args[0] > Args[1]:
        Val = Args[0]
        Args[0] = Args[1]
        Args[1] = Val
    
    ParamFunct = Tls.DictFunct[Data['Funct']]
    X, Y = F(*Args, ParamFunct)
    
    plt.plot(X, Y)
    plt.grid()
    plt.savefig('Figura')

def CallZero(msg, F, Args):
    
    if Args[0] > Args[1]:
        Val = Args[0]
        Args[0] = Args[1]
        Args[1] = Val
    
    ParamFunct = Tls.DictFunct[Data['Funct']]
    x = F(*Args, ParamFunct)
    
    X, Y = Tls.Graficar(min(Args[0], min(Args[1], x)), max(Args[0], max(Args[1], x)), ParamFunct)
    
    plt.plot(X, Y)
    plt.grid()
    #Cero
    plt.plot(x, 0, 'bo-')
    plt.savefig('Figura')
    
    bot.send_message(msg.chat.id, f'El cero de la funcion se encuentra en x = {x}')


















@bot.message_handler(commands=['stop'])
def Stop(message):
    bot.send_message(message.chat.id, 'Adios')
    bot.stop_bot()

@bot.message_handler(commands=['Ver'])
def Stop(message):
    print(bot.get_state(message.from_user.id, message.chat.id) == MyStates.Param.name)
    print(bot.get_state(message.from_user.id, message.chat.id))


@bot.message_handler(func= lambda msg : msg.text != '/start' and bot.get_state(msg.from_user.id, msg.chat.id) == None)
def InicFeedBack(message):
    bot.send_message(message.chat.id, "Bot no Inicializado. Utilize el comando /start para correr el bot")

#Never Stop
if __name__ == '__main__':
    bot.polling(none_stop=True)