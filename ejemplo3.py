sexo=input("[H]: Hombre / [M]: Mujer").upper()
edad=int(input("dame tu edad:"))

if sexo[0]=="H" and edad>65:
    print("Te jubilaras!")
elif sexo[0]=="M" and edad>60:
    print("TE JUBILARAS")
else:
    print("AUN NO TE TOCA")

