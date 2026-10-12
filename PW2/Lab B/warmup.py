"""
PW2 Lab B Part 2 -- three routes to a minimum.

Compare gradient descent, Newton, and SLSQP on two functions:
  2A: f(x) = (x-3)**2 + 1          (easy, one minimum at x=3)
  2B: g(x) = x**4 - 3*x**2 + x + 5 (harder, several stationary points)
Run:  python warmup.py
"""
import numpy as np
from scipy.optimize import newton, minimize

# ---------- 2A: easy convex function ----------
def f(x):   return (x-3)**2 + 1
def df(x):  return 2*(x-3)
def d2f(x): return 2.0

# TODO 2A: minimise f three ways from x0=0 and print each result:

x0 = 0
lr = 0.05
tolerance = 0.001
step = lr
x=x0
print("Simple function")
#   (1) gradient descent by hand (loop x = x - lr*df(x) until the step is tiny)
while(step>=tolerance):
  x = x - lr*df(x)
  step = abs(lr*df(x))
  

print(f"Gradient descent: {x:.2f}")

#   (2) scipy.optimize.newton(df, x0, fprime=d2f)
result = newton(df, x0, fprime=d2f)
print(f"Newton: {result:.2f}")

#   (3) scipy.optimize.minimize(f, x0, method="SLSQP")
result = minimize(f, x0, method="SLSQP")
print(f"SLSQP: {result.x[0]:.2f}")

# ---------- 2B: harder landscape ----------
def g(x):   return x**4 - 3*x**2 + x + 5
def dg(x):  return 4*x**3 - 6*x + 1
def d2g(x): return 12*x**2 - 6

# TODO 2B: run the same three methods on g, from x0=0 AND from x0=2.
#   For Newton (which solves dg(x)=0), also check the sign of d2g at the answer:
#   d2g > 0 means a minimum, d2g < 0 means a maximum.
#   In your README note: do the methods agree? did Newton find a minimum or
#   another stationary point? how did the starting point change the result?

x0 = 0
step = lr
x=x0
print("\nDifficult function, x0=0")
#   (1) gradient descent by hand (loop x = x - lr*df(x) until the step is tiny)
while(step>=tolerance):
  x = x - lr*dg(x)
  step = abs(lr*dg(x))
  
print(f"Gradient descent: {x:.2f}")

#   (2) scipy.optimize.newton(df, x0, fprime=d2f)
result = newton(dg, x0, fprime=d2g)
print(f"Newton: {result:.2f}")

if d2g(result) > 0:
  print(f"Minimum d2g={d2g(result):.2f}")
else:
  print(f"Maximum d2g={d2g(result):.2f}")

#   (3) scipy.optimize.minimize(f, x0, method="SLSQP")
result = minimize(g, x0, method="SLSQP")
print(f"SLSQP: {result.x[0]:.2f}")


x0 = 2
step = lr
x=x0
print("\nDifficult function, x0=2")
#   (1) gradient descent by hand (loop x = x - lr*df(x) until the step is tiny)
while(step>=tolerance):
  x = x - lr*dg(x)
  step = abs(lr*dg(x))
  

print(f"Gradient descent: {x:.2f}")

#   (2) scipy.optimize.newton(df, x0, fprime=d2f)
result = newton(dg, x0, fprime=d2g)
print(f"Newton: {result:.2f}")

if d2g(result) > 0:
  print(f"Minimum d2g={d2g(result):.2f}")
else:
  print(f"Maximum d2g={d2g(result):.2f}")

#   (3) scipy.optimize.minimize(f, x0, method="SLSQP")
result = minimize(g, x0, method="SLSQP")
print(f"SLSQP: {result.x[0]:.2f}")