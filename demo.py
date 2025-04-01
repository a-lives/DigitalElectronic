from digitalElectronic import *

a,b,c = symbols("A B C")

# print(~a+b*c+~(a*b*c.xnor(a)))

ang = [ANDNOTgate() for _ in range(7)]

ang[0](a,b)
ang[1](ang[0],a)
ang[2](ang[0],b)
ang[3](ang[1],ang[2],c)
ang[4](ang[2],ang[3],ang[1])
ang[5](ang[3],c)
ang[6](ang[4],ang[5])

output = ang[6].output
df = output.get_truth_table((a,b,c))
print(df)


