from init import *
from sympy import abc
from sympy.parsing.sympy_parser import parse_expr


expr = parse_expr(input("y = "))

def eval_function(x):
	return float(expr.subs({"x": x}).evalf())

g = Graph(eval_function, [-5, 5], bindings={"range": lambda: [canvas.min_x, canvas.max_x], "definedStep": lambda:  10 / canvas.ratio}, cache=False)

canvas.addObject(g)

canvas.loop(60)