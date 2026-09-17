print("== SISTEMA DE ACCESO ==")

#Entrada de datos
nombre = input("Ingrese tu nombre")
edad = int(input("Ingrese tu edad"))
tipo_usuario = input("¿Eres estudiante, profesor o invitado?: ")
matriculado = input ("¿Estas matriculado? (si/no): ")
pago = input("¿Has realizado el pago? (si/no): ")

print("\nVerificando Datos")

# Creamos nuestras condiciones
# Verificamos edad
if edad < 18:
    print("Lo sentimos, ", nombre, " debes ser mayor de edad")

elif tipo_usuario == "estudiante":
    if matriculado == "si":
        if pago == "si":
            print("Acceso concedido,", nombre)
            print("Bienvenido al curso")
        else:
            print("Estas matriculado, pero debes realizar el pago")
    else:
        print("No estas matriculado en el curso")

elif tipo_usuario == "profesor":
    if matriculado == "si":
        if pago == "si":
            print("Bievenido, ",nombre)
            print("Ingrese curso asignado")
            curso = input("curso: ")

            print("\n Datos del docente")
            print("Nombre:", nombre)
            print("Curso:", curso)
    else:
        print("Debes estar registrado o tener un pago valido")

elif tipo_usuario == "invitado":
    print("\n Acceso de invitado")

    motivo = input("¿Cuál es el motivo de tu visita?: ")

    if edad >=18:
        pago == "si"
        if not matriculado == "si":
            print ("\nTienes acceso temporal al sitio")
            print ("Nombre: ", nombre)
            print ("Motivo: ", motivo)
            print ("Tienes acceso de 1 hora")
        else:
            print("Ya estas matriculado como estudiante")
            print("Utiliza el acceso correspondiente")
    else:
        print("No cumples con los requisitos para acceder a este sitio como invitado")
else:
    print("Tipo de usuario no valido")

    