# ==========================================
# GYMFIT - SISTEMA BÁSICO DE GIMNASIO
# ==========================================

# ------------------------------------------
# DATOS DEL USUARIO
# ------------------------------------------
nombre = ""
apellido = ""
correo = ""
contraseña = ""
edad = 0

objetivo = ""
nivel = ""
horas_totales = 0
historial = []

# ------------------------------------------
# DATOS DEL ENTRENADOR
# ------------------------------------------
correo_entrenador = "trainer@gymfit.com"
contraseña_entrenador = "1234"


# ==========================================
# REGISTRO
# ==========================================
def registrar_usuario():
    global nombre, apellido, correo, contraseña, edad

    print("\n========== REGISTRO ==========")
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    correo = input("Ingrese su correo: ")
    contraseña = input("Ingrese su contraseña: ")

    confirmar = input("Confirme su contraseña: ")
    while contraseña != confirmar:
        print("Las contraseñas no coinciden.")
        confirmar = input("Confirme nuevamente su contraseña: ")

    try:
        edad = int(input("Ingrese su edad: "))
    except ValueError:
        edad = 0
        print("Edad no válida, se guardó como 0.")

    print("\nRegistro completado correctamente.")


# ==========================================
# ELEGIR OBJETIVO
# ==========================================
def elegir_objetivo():
    global objetivo

    print("\n========== ELEGIR OBJETIVO ==========")
    print("1. Bajar de peso")
    print("2. Aumentar masa muscular")

    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        objetivo = "Bajar de peso"
        print("\nObjetivo seleccionado: Bajar de peso")
    elif opcion == "2":
        objetivo = "Aumentar masa muscular"
        print("\nObjetivo seleccionado: Aumentar masa muscular")
    else:
        print("\nOpción incorrecta.")


# ==========================================
# ELEGIR NIVEL
# ==========================================
def elegir_nivel():
    global nivel

    print("\n========== ELEGIR NIVEL ==========")
    print("1. Fácil\n   Estoy comenzando o tengo poca experiencia.")
    print("\n2. Básico\n   Ya conozco los ejercicios básicos y tengo algo de experiencia.")
    print("\n3. Avanzado\n   Entreno regularmente y tengo experiencia con ejercicios y pesas.")

    opcion = input("\nSeleccione su nivel: ")
    if opcion == "1":
        nivel = "Fácil"
        print("\nNivel seleccionado: Fácil")
    elif opcion == "2":
        nivel = "Básico"
        print("\nNivel seleccionado: Básico")
    elif opcion == "3":
        nivel = "Avanzado"
        print("\nNivel seleccionado: Avanzado")
    else:
        print("\nOpción incorrecta.")


# ==========================================
# MOSTRAR RUTINA
# ==========================================
def mostrar_rutina():
    print("\n========== MI RUTINA ==========")

    if objetivo == "" or nivel == "":
        print("Primero debes seleccionar un objetivo y un nivel.")
        return

    # --------------------------------------
    # BAJAR DE PESO
    # --------------------------------------
    if objetivo == "Bajar de peso":
        if nivel == "Fácil":
            print("\nRutina - Bajar de peso / Fácil")
            print("Duración aproximada: 30 - 45 minutos")
            print("\nEjercicios:")
            print("1. Caminata ligera - 10 minutos")
            print("2. Bicicleta estática - 10 minutos")
            print("3. Sentadillas sin peso - 3 series de 10")
            print("4. Movilidad y estiramiento - 5 minutos")

        elif nivel == "Básico":
            print("\nRutina - Bajar de peso / Básico")
            print("Duración aproximada: 45 - 60 minutos")
            print("\nEjercicios:")
            print("1. Caminata rápida - 10 minutos")
            print("2. Bicicleta estática - 15 minutos")
            print("3. Sentadillas - 3 series de 12")
            print("4. Zancadas - 3 series de 10")
            print("5. Cardio - 10 minutos")

        elif nivel == "Avanzado":
            print("\nRutina - Bajar de peso / Avanzado")
            print("Duración aproximada: 60 minutos")
            print("\nEjercicios:")
            print("1. Carrera/HIIT - 15 minutos")
            print("2. Burpees - 4 series de 15")
            print("3. Mountain Climbers - 4 series de 30 seg")
            print("4. Sentadillas con salto - 4 series de 15")
            print("5. Enfriamiento y cardio suave - 10 minutos")

    # --------------------------------------
    # AUMENTAR MASA MUSCULAR
    # --------------------------------------
    elif objetivo == "Aumentar masa muscular":
        if nivel == "Fácil":
            print("\nRutina - Masa Muscular / Fácil")
            print("Duración aproximada: 40 minutos")
            print("\nEjercicios:")
            print("1. Calentamiento articular - 5 minutos")
            print("2. Sentadillas asistidas - 3 series de 10")
            print("3. Flexiones apoyando rodillas - 3 series de 8")
            print("4. Remo con mancuernas ligeras - 3 series de 10")

        elif nivel == "Básico":
            print("\nRutina - Masa Muscular / Básico")
            print("Duración aproximada: 50 minutos")
            print("\nEjercicios:")
            print("1. Sentadillas con barra/mancuerna - 4 series de 10")
            print("2. Press de banca o pechadas - 4 series de 10")
            print("3. Peso muerto rumano - 3 series de 10")
            print("4. Press militar con mancuernas - 3 series de 10")

        elif nivel == "Avanzado":
            print("\nRutina - Masa Muscular / Avanzado")
            print("Duración aproximada: 60 - 75 minutos")
            print("\nEjercicios:")
            print("1. Sentadilla pesada - 4 series de 6 a 8")
            print("2. Press de banca pesado - 4 series de 6 a 8")
            print("3. Dominadas o Remo con barra - 4 series de 8")
            print("4. Press militar pesado - 4 series de 8")
            print("5. Curl de bíceps y Extensiones de tríceps - 3 series de 12")


# ==========================================
# MENÚS
# ==========================================
def menu_cliente():
    while True:
        print("\n========== MENÚ CLIENTE ==========")
        print("1. Elegir objetivo")
        print("2. Elegir nivel")
        print("3. Ver mi rutina")
        print("4. Cerrar sesión")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            elegir_objetivo()
        elif opcion == "2":
            elegir_nivel()
        elif opcion == "3":
            mostrar_rutina()
        elif opcion == "4":
            print("\nCerrando sesión del cliente...")
            break
        else:
            print("\nOpción no válida.")


def menu_entrenador():
    while True:
        print("\n========== MENÚ ENTRENADOR ==========")
        print("1. Ver datos del cliente")
        print("2. Cerrar sesión")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("\n--- INFORMACIÓN DEL CLIENTE ---")
            if nombre == "":
                print("No hay ningún cliente registrado actualmente.")
            else:
                print(f"Nombre completo: {nombre} {apellido}")
                print(f"Correo: {correo}")
                print(f"Edad: {edad}")
                print(f"Objetivo: {objetivo if objetivo != '' else 'No definido'}")
                print(f"Nivel: {nivel if nivel != '' else 'No definido'}")
        elif opcion == "2":
            print("\nCerrando sesión del entrenador...")
            break
        else:
            print("\nOpción no válida.")


def iniciar_sesion():
    print("\n========== INICIAR SESIÓN ==========")
    correo_ingresado = input("Correo: ")
    contraseña_ingresada = input("Contraseña: ")

    # LOGIN ENTRENADOR
    if correo_ingresado == correo_entrenador and contraseña_ingresada == contraseña_entrenador:
        print("\nBienvenido, entrenador.")
        menu_entrenador()

    # LOGIN CLIENTE
    elif correo_ingresado == correo and contraseña_ingresada == contraseña and correo != "":
        print(f"\nBienvenido, {nombre} {apellido}.")
        menu_cliente()

    else:
        print("\nCorreo o contraseña incorrectos (o el usuario aún no se ha registrado).")


# ==========================================
# BUCLE PRINCIPAL
# ==========================================
def main():
    while True:
        print("\n==========================================")
        print("        GYMFIT - SISTEMA PRINCIPAL       ")
        print("==========================================")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            print("\nGracias por usar GymFit. ¡Hasta pronto!")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
