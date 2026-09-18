print("== LOGIN E-COMMERCE ==")


# Entrada de datos
nombre = input("Ingrese su nombre: ")
edad = int(input("Ingrese su edad: "))
tipo_usuario = input("¿Eres cliente, administrador o invitado?: ")
registrado = input("¿Estás registrado? (si/no): ")
contraseña = input("Ingresa tu contraseña: ")


print("\nVerificando Datos")


# Creamos nuestras condiciones
# Verificamos edad
if edad < 18:
    print("Lo sentimos,", nombre, "debes ser mayor de edad")

elif tipo_usuario == "cliente":
    if registrado == "si":
        if contraseña != "":
            print("Acceso concedido,", nombre)
            print("Bienvenido a la tienda")
        else:
            print("Debes ingresar tu contraseña")
    else:
        print("No estás registrado en la tienda")

elif tipo_usuario == "administrador":
    if registrado == "si":
        if contraseña != "":
            print("Bienvenido,", nombre)
            print("Acceso al panel de administración")
        else:
            print("Debes ingresar tu contraseña")
    else:
        print("Debes estar registrado para ingresar")

elif tipo_usuario == "invitado":
    print("\nAcceso de invitado")

    motivo = input("¿Cuál es el motivo de tu visita?: ")

    if edad >= 18:
        if registrado != "si":
            print("\nTienes acceso temporal a la tienda")
            print("Nombre:", nombre)
            print("Motivo:", motivo)
            print("Tienes acceso como invitado")
        else:
            print("Ya estás registrado como cliente")
            print("Utiliza el acceso correspondiente")
    else:
        print("No cumples con los requisitos para acceder")

else:
    print("Tipo de usuario no válido")