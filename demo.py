from digitalElectronic import *

a,b,c = symbols("A B C")

print(a+b*c+a*b*c.xor(a))