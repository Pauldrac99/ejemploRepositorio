#edadCliente=input("Dame tu edad: ")
edadCliente=int(input("Dame tu edad: "))
#if int(edadCliente)>18:
if edadCliente<18:
    print("Eres menor de edad")
elif edadCliente<30:
    print("Eres joven")
elif edadCliente<65:
    print("eres un adulto menor")
else:
    print("Eres un legendario")