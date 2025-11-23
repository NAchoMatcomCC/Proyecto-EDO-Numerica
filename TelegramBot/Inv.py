# import Interpreter.Lexer as Lx
# import Interpreter.Parser as Ps
# import Interpreter.ASTNodes as AST

# Text = """(Hola = X, Manana = 3, Sera = 
# 5, 1 + 3 / 4, Gran,
# Dia = 1.01)"""

# Text1 = '(-1, 5, -5, 5)'

# Text2 = '(2 + 3 / 0)'

# Lexer = Lx.Lexer(Text2)
# Lexer.Tokenize()
# Tokens = Lexer.Tokens

# Parser = Ps.Parser(Tokens)

# Parser.IndexLine = 1
# Nodes = Parser.__ObtainArgs__(Tokens[0])

# Operation = Nodes[0]

# Visitor = AST.CheckVisitor()

# Value = Operation.Accept(Visitor)

# Visitor = AST.Visitor()

# Value = Operation.Accept(Visitor)

# print(Value)


import numpy as np

def quadratic_interpolation(f, x0, x1, x2, tol=1e-20, max_iter=100):
    
    """Implementa el método de interpolación cuadrática inversa para aproximar la solución de una ecuación no lineal.
    Parameters
    ----------
    f : function
        Función no lineal para la cual se desea aproximar la solución.
    x0 : float
        El primer punto inicial.
    x1 : float
        El segundo punto inicial.
    x2 : float
        El tercer punto inicial.
    tol : float, optional
        Tolerancia para la aproximación de la solución. El valor por defecto es 1e-8.
    max_iter : int, optional
        Número máximo de iteraciones permitidas. El valor por defecto es 100.
    Returns
    -------
    float
        Aproximación de la solución de la ecuación no lineal.
    Raises
    ------
    ValueError
        Si no se alcanza la tolerancia en el número máximo de iteraciones.
    Notes
    -----
    El método de interpolación cuadrática inversa puede no converger en algunos casos, por lo que se recomienda probar diferentes puntos iniciales si se obtiene una solución incorrecta o si la función lanza una excepción.
    Examples
    --------
    >>> f = lambda x: x**3 - x**2 - x - 1
    >>> x0, x1, x2 = 0, 1, 2
    >>> x = quadratic_interpolation(f, x0, x1, x2)
    >>> print(x)
    1.8392867550506584
    """
    
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
        if np.abs(xn - x0) < tol:
            return (x0, _)
        x2 = x1
        x1 = x0
        x0 = xn
        
    # Si no se alcanzó la tolerancia en el número máximo de iteraciones
    raise ValueError(f"No se alcanzó la tolerancia en {max_iter} iteraciones.")


def S(x):
    return x**2 - 4 * np.sin(x)

# val = quadratic_interpolation(S, 1, 1.75, 2.5)

print(np.sign(0) == 0)