import sys
import asyncio
import aiofiles

from telebot.async_telebot import AsyncTeleBot, asyncio_filters
import telebot.types as tp
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.asyncio_storage import StateMemoryStorage

import Interpreter.Lexer as Lx
import Interpreter.Parser as Ps
import Interpreter.ASTNodes as AST
import Tools.Tools as Tls

import numpy as np
import matplotlib.pyplot as plt



API_TOKEN = "8028863934:AAFxrMjKDNLJ60CoQ2_dtiLcYdRW0dI6HgQ"
state_storage = StateMemoryStorage()  # In-memory state storage
bot = AsyncTeleBot(API_TOKEN, state_storage=state_storage)
bot.add_custom_filter(asyncio_filters.StateFilter(bot))

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


@bot.message_handler(commands=['stop'])
async def Stop(message):
    await bot.send_message(message.chat.id, 'Adios')
    sys.exit(0)

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
async def Inicialize(message):
    
    state = await bot.get_state(message.from_user.id, message.chat.id)
    
    if state != MyStates.Inic.name:
        await bot.send_message(message.chat.id, 'Bot corriendo...')
    else:
        await bot.send_message(message.chat.id, 'Iniciando parametros por defecto...')
    
    await bot.set_state(message.from_user.id, MyStates.Inic, message.chat.id)
    Data = {'Method': Methods[0], 'Funct': Functs[0], 'Zero': Zeros[0], 'Parameters': []}
    #Crear Script de Funciones Basicas

@bot.message_handler(state = MyStates.Inic, func= lambda msg : msg.text == '/graf')
async def SelectGrafMethod(msg):
    #Create Markup
    bt1 = tp.InlineKeyboardButton('Euler Mejorado', callback_data='EM')
    bt2 = tp.InlineKeyboardButton('Runge-Kutta 4', callback_data='RK4')
    bt3 = tp.InlineKeyboardButton('Graficar(normal)', callback_data='Graf')
    markup = tp.InlineKeyboardMarkup()
    markup.add(bt1)
    markup.add(bt2)
    markup.add(bt3)
    
    await bot.send_message(msg.chat.id, text='Selecciona uno de los siguientes metodos para graficar', reply_markup=markup)

@bot.message_handler(state=MyStates.Inic, func= lambda msg : msg.text == '/isoclina')
async def IsoclinaListParam(msg):
    # XLeftrg, XRightrg, YDownrg, YUprg, F, seg = 0.5, fsize= (10,10), SeeVectors = True, SeeLines = True
    text = '''Introduzca en un mensaje el "valor" los parametros en orden correspondiente separados por coma:\n
            XLeft: Limite Izquierdo en el eje x\n
            XRight: Limite Derecho en el eje x\n
            YDown: Limite Inferior en el eje y\n
            YUp: Limite Superior en el eje y'''
    await bot.send_message(msg.chat.id, text)
    await bot.set_state(msg.from_user.id, MyStates.Isoc, msg.chat.id)

@bot.callback_query_handler(func= lambda call : VerifyMethod(call.data))
async def PrintMethodParam(call):
    
    await bot.answer_callback_query(call.id, f'Ejecutando {call.data} para la funcion {Data["Funct"]}')
    Data['Method'] = call.data
    
    text = '''Introduzca en un mensaje el "valor" los parametros en orden correspondiente separados por coma:\n
    XLeft: Limite Izquierdo en el eje x\n
    XRight: Limite Derecho en el eje x\n'''
    
    if call.data == 'RK4' or call.data == 'EM':
        text += '   y: Coordenada en y del punto inicial\n'
    
    
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, text)
    await bot.set_state(call.from_user.id, MyStates.Param, call.message.chat.id)

@bot.message_handler(state=MyStates.Param)
async def GetMethodParam(msg):
    
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
    
    await ObtainGrafwithParam(msg, Funct, Cargs)

@bot.message_handler(commands=['select'])
async def SelectFunction(msg):
    
    markup = tp.InlineKeyboardMarkup()
    
    for F in Functs:
        button = tp.InlineKeyboardButton(F, callback_data= F)
        markup.add(button)
    
    Text = '''Selecciona una de las siguientes funciones:\n
    (Por defecto: "Der-Velocidad")'''
    
    await bot.send_message(msg.chat.id, Text, reply_markup = markup)

@bot.callback_query_handler(func= lambda call : VerifyFunct(call.data))
async def FunctionQueries(call):
    
    await bot.answer_callback_query(call.id, f'{call.data} establecido')
    Data['Funct'] = call.data

@bot.message_handler(state=MyStates.Isoc)
async def GetIsocParam(msg):
    
    await ObtainGrafwithParam(msg, Tls.Graf_Isoclina, 4)

@bot.message_handler(commands=['zero'])
async def SelectZeroMethod(msg):
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
    
    await bot.send_message(msg.chat.id, text='Selecciona uno de los siguientes metodos para hallar una raiz', reply_markup=markup)


@bot.callback_query_handler(func= lambda call : VerifyZeros(call.data))
async def ZerosQueries(call):
    
    await bot.answer_callback_query(call.id, f'Ejecutando {call.data} para la funcion {Data["Funct"]}')
    Data['Zero'] = call.data
    
    text = '''Introduzca en un mensaje el "valor" los parametros en orden correspondiente separados por coma:\n
    XLeft: Limite Izquierdo en el eje x\n
    XRight: Limite Derecho en el eje x\n'''
    
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, text)
    await bot.set_state(call.from_user.id, MyStates.Zero, call.message.chat.id)

@bot.message_handler(state=MyStates.Zero)
async def SelectZeroMethod(msg):

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
    
    await ObtainGrafwithParam(msg, Funct, Cargs)

async def ObtainGrafwithParam(msg, Funct, CArgs):
    
    await bot.send_message(msg.chat.id, 'Procesando...')
    
    #Obtain Text Parameters
    Text = '(' + msg.text + ')'
    #Tokenizar Parameters
    Lexer = Lx.Lexer(Text)
    await asyncio.to_thread(Lexer.Tokenize)
    Tks = Lexer.Tokens
    
    if Lexer.NoErrors == False:
        ErrText = Lexer.MsgErr[0].Error
        await bot.send_message(msg.chat.id, 'Lexer -> ' + ErrText)
        return
    
    #Parsear
    Parser = Ps.Parser(Tks)
    Parser.IndexLine = 1
    Nodes = await asyncio.to_thread(Parser.__ObtainArgs__, Tks[0])
    
    if Parser.NoErrors == False:
        ErrText = Parser.MsgErr[0].Error
        await bot.send_message(msg.chat.id, 'Parser -> ' + ErrText)
        return
    
    #Visitor Semantico
    for n in Nodes:
        Visitor = AST.CheckVisitor()
        Val = await asyncio.to_thread(n.Accept, Visitor)
        
        if Val == 'Unknow':
            ErrText = Visitor.MsgErr[0].Error
            await bot.send_message(msg.chat.id, 'Check Semantic -> ' + ErrText)
            return
    
    #Visitor Operacional
    Args = []
    for n in Nodes:
        Visitor = AST.Visitor()
        Val = await asyncio.to_thread(n.Accept, Visitor)
        
        if Visitor.NoErrors == False:
            ErrText = Visitor.MsgErr[0].Error
            await bot.send_message(msg.chat.id, 'Operation -> ' + ErrText)
        else:
            Args.append(Val)
    
    #Verificar si estan todos los argumentos
    if len(Args) != CArgs:
        await bot.send_message(msg.chat.id, f'Recived Arguments -> Se esperaban {CArgs} argumentos. Se obtuvieron {len(Args)}')
    else:
        
        #Manejo de errores
        Value = False
        
        try:
            if await bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Isoc.name:
                Value = await CallIsoclina(msg, Args)
            elif await bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Param.name:
                Value = await CallGrafMethod(msg, Funct, Args)
            elif await bot.get_state(msg.from_user.id, msg.chat.id) == MyStates.Zero.name:
                Value = await CallZero(msg, Funct, Args)
            
        except OverflowError as e:
            await bot.send_message(msg.chat.id, f'Error -> {e}')
        except ZeroDivisionError as e:
            await bot.send_message(msg.chat.id, f'Error -> {e}')
        except TypeError as e:
            await bot.send_message(msg.chat.id, f'Error -> {e}')
        except ValueError as e:
            await bot.send_message(msg.chat.id, f'Error -> {e}')
        
        
        #Mostrar Grafica
        if Value:
            async with aiofiles.open('Figura.png', 'rb') as Img:
                await bot.send_photo(msg.chat.id, Img)
        
        await bot.set_state(msg.from_user.id, MyStates.Inic, msg.chat.id)

async def CallIsoclina(msg, Args):
    
    ParamFunct = Tls.DictFunct[Data['Funct']]
    
    if isinstance(ParamFunct, Tls.Derivade):
        
        if Args[0] > Args[1]:
            Val = Args[0]
            Args[0] = Args[1]
            Args[1] = Val
        
        if Args[2] > Args[3]:
            Val = Args[2]
            Args[2] = Args[3]
            Args[3] = Val
        
        await asyncio.to_thread(Tls.Graf_Isoclina, *Args, ParamFunct.Function)
        return True
    await bot.send_message(msg.chat.id, f'Operacion no siportada para Funciones del tipo F(x)')
    return False

async def CallGrafMethod(msg, F, Args):
    
    ParamFunct = Tls.DictFunct[Data['Funct']]
    
    
    
    if Args[0] > Args[1]:
        Val = Args[0]
        Args[0] = Args[1]
        Args[1] = Val
    
    try:
        X, Y = await asyncio.to_thread(F, *Args, ParamFunct.Function)
    except:
        await bot.send_message(msg.chat.id, f'Operacion no siportada')
    
    
    plt.plot(X, Y)
    plt.grid()
    plt.savefig('Figura')
    return True


#No se puede llamar para funciones del tipo F(x,y)
async def CallZero(msg, F, Args):
    
    ParamFunct = Tls.DictFunct[Data['Funct']]
    
    if isinstance(ParamFunct, Tls.Normal):
    
        if Args[0] > Args[1]:
            Val = Args[0]
            Args[0] = Args[1]
            Args[1] = Val
        
        x = await asyncio.to_thread(F, *Args, ParamFunct.Function)
        
        X, Y = await asyncio.to_thread(Tls.Graficar(), min(Args[0], min(Args[1], x)), max(Args[0], max(Args[1], x)), ParamFunct.Function)
        
        plt.plot(X, Y)
        plt.grid()
        #Cero
        plt.plot(x, 0, 'bo-')
        plt.savefig('Figura')
        
        await bot.send_message(msg.chat.id, f'El cero de la funcion se encuentra en x = {x}')
        return True
    await bot.send_message(msg.chat.id, f'Operacion no siportada para Funciones del tipo F(x,y)')
    return False




















@bot.message_handler(commands=['Ver'])
async def Stop(message):
    print(await bot.get_state(message.from_user.id, message.chat.id) == MyStates.Param.name)
    print(await bot.get_state(message.from_user.id, message.chat.id))


@bot.message_handler(state=None, func= lambda msg : msg.text != '/start')
async def InicFeedBack(message):
    await bot.send_message(message.chat.id, "Bot no Inicializado. Utilize el comando /start para correr el bot")




#Never Stop
# Main async entry point
async def main():
    print("Bot is running...")
    await bot.polling(non_stop=True)

if __name__ == "__main__":
    asyncio.run(main())