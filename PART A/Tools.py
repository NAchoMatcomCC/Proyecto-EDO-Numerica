import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Isoclina///////////////////////////////////////////////////////////////////////////////////////////////

#Funcion para representar vectores
def __Vector(tang, initialx, initialy, scale, SeeVectors, SeeLines):
    angle = np.arctan(tang)
    xval = np.cos(angle)
    yval = np.sin(angle)
    if SeeVectors:
        plt.quiver(initialx, initialy, xval, yval, angles='xy', scale_units='xy', scale=1 * scale**-1)
    if SeeLines:
        plt.streamplot(initialx, initialy, xval, yval)

#Sacar las derivadas de cada punto (x,y) y representar el vector correspondiente
def __Isoclina(Funtion, seg ,lrg, rrg, drg, urg, SeeVectors, SeeLines):
    
    Xdiv = np.arange(lrg, rrg, seg)
    Ydiv = np.arange(drg, urg, seg)
    X, Y = np.meshgrid(Xdiv, Ydiv)
    
    tang = np.array([[Funtion(i,j) for i in Xdiv] for j in Ydiv])
    
    __Vector(tang, X, Y, seg, SeeVectors, SeeLines)


#Funcion Portal de Isoclina
def Graf_Isoclina(XLeftrg, XRightrg, YDownrg, YUprg, F, seg = 2, fsize= (10,10), SeeVectors = True, SeeLines = True):
    
    plt.subplots(figsize=fsize)
    
    __Isoclina(F, seg, XLeftrg, XRightrg+1, YDownrg, YUprg+1, SeeVectors, SeeLines)
    
    plt.xlim(XLeftrg, XRightrg)
    plt.ylim(YDownrg, YUprg)
    plt.grid()
    plt.savefig('Figura')


#Graf Methods ///////////////////////////////////////////////////////////////////////////////////////////////////

def RungeKutta4(xLeft, xRight, y, Der, intervals = 0.1):
    
    X = [xLeft]
    Y = [y]
    x0 = xLeft
    y0 = y
    
    while x0 < xRight:
        #Pendiente
        k1 = Der(x0, y0)
        k2 = Der(x0 + intervals/2, y0 + intervals/2 * k1)
        k3 = Der(x0 + intervals/2, y0 + intervals/2 * k2)
        k4 = Der(x0 + intervals, y0 + intervals * k3)
        
        m = (k1 + 2*k2 + 2*k3 + k4) / 6
        
        y0 = m * intervals + y0
        x0 += intervals
        
        X.append(x0)
        Y.append(y0)
    
    return (X,Y)

def EulerMejorado(xLeft, xRight, y, Der, intervals = 0.1):
    
    X = [xLeft]
    Y = [y]
    x0 = xLeft
    y0 = y
    
    while x0 < xRight:
        #Pendiente
        m0 = Der(x0, y0)
        m = (m0 + Der(x0 + intervals, y0 + intervals * m0)) / 2
        
        y0 = m * intervals + y0
        x0 += intervals
        
        X.append(x0)
        Y.append(y0)
    
    return (X,Y)

def Graficar(xLeft, xRight, F, intervals = 0.1):
    
    X = np.arange(xLeft, xRight, intervals)
    Y = [F(x) for x in X]
    
    return (X,Y)

#Cero Methods ///////////////////////////////////////////////////////////////////////////////////////////////////

import matplotlib.pyplot as plt
import numpy as np

def Bisection(a,b,Funtion, e = 1e-10):
    
    if np.sign(Funtion(a)) == np.sign(Funtion(b)):
        print("Invalido")
        raise ValueError(f"Biseccion no soportada para extremos de mismo signo")
    
    while abs(a - b) > e:
        
        m = a + (b - a)/2
        Sign = np.sign(Funtion(m))
        
        if Sign == 0:
            return m
        
        if Sign == np.sign(Funtion(a)):
            a = m
        else:
            b = m
    
    return (a, b)

def quadratic_interpolation(f, x0, x1, x2, tol=1e-10, max_iter=100):
    
    for _ in range(max_iter):
        # Evalúa la función en los tres puntos de interpolación
        fx0 = f(x0)
        fx1 = f(x1)
        fx2 = f(x2)
        # Construir la función cuadrática que pasa por los puntos x0, x1 y x2
        l0 = (x0 * fx1 * fx2) / ((fx0 - fx1) * (fx0 - fx2))
        l1 = (x1 * fx0 * fx2) / ((fx1 - fx0) * (fx1 - fx2))
        l2 = (x2 * fx1 * fx0) / ((fx2 - fx0) * (fx2 - fx1))
        xn = l0 + l1 + l2
        # Revisar si se ha alcanzado la tolerancia
        if np.abs(f(xn)) < tol:
            return (xn)
        x2 = x1
        x1 = x0
        x0 = xn
        
    # Si no se alcanzó la tolerancia en el número máximo de iteraciones
    raise ValueError(f"No se alcanzó la tolerancia en {max_iter} iteraciones.")

def Hibrid_Bis_IQI(a, b, F, Be = 1):
    
    if Be < abs(a - b):
        a, b = Bisection(a, b, F, Be)
    
    m = a + (b - a)/2
    result = quadratic_interpolation(F, a, m, b)
    
    return result


def NewtonMethod(F ,dF, x0, max_iter = 100, e = 1e-10):
    
    #Hallar x0 cuando y = 0
    #(y-y0) = (x-x0)m -> -y0 = xm - x0m -> x = (-y0 + x0m)/m = -y0/m + x0
    c = 0
    for _ in range(max_iter):
        #Pendiente
        m = dF(x0)
        y0 = F(x0)
        
        x = -y0/m + x0
        
        if abs(F(x)) < e:
            print(c)
            return x
        
        x0 = x
        c+=1
    
    raise ValueError(f"No se alcanzó la tolerancia en {max_iter} iteraciones.")


def RegulaFalsi(a, b, F, max_iter = 100, e = 1e-10):
    
    for _ in range(max_iter):
        
        w = (F(b)*a - F(a)*b) / (F(b) - F(a))
        
        if F(a)*F(w) <= 0:
            b = w
        else:
            a = w
        
        if abs(a-b) < e:
            return(a, b)
    
    raise ValueError(f"No se alcanzó la tolerancia en {max_iter} iteraciones.")

def SecantMethod(x0, x1, F, max_iter = 100, e = 1e-10):
    
    c=0
    for _ in range(max_iter):
        
        m = (x1 - x0)/(F(x1) - F(x0))
        y1 = F(x1)
        
        x = -y1*m + x1
        
        if abs(F(x)) < e:
            print(c)
            return x
        
        x0 = x1
        x1 = x
        c+=1
    
    raise ValueError(f"No se alcanzó la tolerancia en {max_iter} iteraciones.")




#Functions ///////////////////////////////////////////////////////////////////////////////////////////////////

def Distancia(t, x0 = 10000, v0 = 0, tp = 20):
    if t > tp:
        x1 = __Distance__(x0, v0, 20, 0.15)
        v1 = __Velocity__(v0, tp, 0.15)
        x = __Distance__(x1, v1, t-tp, 1.5)
    else:
        x = __Distance__(x0, v0, t, 0.15)
    return x

def __Distance__(x0,v0,t,r):
    g = 32
    vt = -g/r
    x = x0 + vt*t + 1/r * (v0 - vt) * (1 - np.e**(-r*t))
    return x


#Velocidad
def Velocidad(t, y = 0, v0 = 0, tp = 20):
    #y parameter is useless (For Derivate F(X,Y))
    
    if t > tp:
        v1 = __Velocity__(v0, tp, 0.15)
        v = __Velocity__(v1, t-tp, 1.5)
    else:
        v = __Velocity__(v0, t, 0.15)
    return v

def __Velocity__(v0, t, r):
    g = 32
    vt = -g/r
    v = (v0 - vt) * np.e**(-r*t) + vt
    return v


def Der_Velocidad(t, v, tp = 20):
    g = 32
    r = 0.15
    
    if t >= tp:
        r = 1.5
    
    return -g -r*v


def D(u,z):
    return u - z**2




#Class Functions ///////////////////////////////////////////////////////////////////////////////////////////////////

class Functions:
    def __init__(self, F):
        self.Function = F

#Functions of type (F=(X,Y))
class Derivade(Functions):
    def __init__(self, F):
        super().__init__(F)

#Functions of type (F=(X))
class Normal(Functions):
    def __init__(self, F):
        super().__init__(F)



class DFunctions(Derivade):
    def __init__(self, F):
        super().__init__(F)

class NFunction(Normal):
    def __init__(self, F):
        super().__init__(F)

class SFunction(Derivade, Normal):
    def __init__(self, F):
        super().__init__(F)


DictFunct = {
    'Der-Velocidad': DFunctions(Der_Velocidad),
    'Distancia': NFunction(Distancia),
    'Velocidad': SFunction(Velocidad)
}


