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