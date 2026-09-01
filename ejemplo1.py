#BLOQUE IF
temperatura=18
if temperatura == 17:
    #Acciones si es verdadero.
    print("es verdad, estoy dentro de la estructura de control IF")
    temperatura=tambien+3
    print(f"temperatura: {temperatura}")
   
else:
    #Acciones si es falso.
     print("tambien estoy dentro de la estructura")
     temperatura=temperatura-1
     print(f"temperatura: {temperatura}")

print("estoy fuera de la estructura IF")

temperatura=temperatura*10
