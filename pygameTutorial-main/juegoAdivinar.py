import random
import msvcrt

# ============================================================================
# 1. FUNCIONES DE UTILIDAD (Operaciones básicas y puras)
# ============================================================================

def generar_aleatorio(limite_inferior, limite_superior):
    """
    Genera un número aleatorio dentro del rango especificado.
    Principio: Single Responsibility (SRP).
    """
    return random.randint(limite_inferior, limite_superior)


def verificar_en_intervalo(limite_inferior, limite_superior, numero):
    """
    Valida si un número está dentro del rango permitido.
    Principio: Open/Closed (OCP).
    """
    return limite_inferior <= numero <= limite_superior


# ============================================================================
# 2. FUNCIONES DE CONFIGURACIÓN (Setup del juego)
# ============================================================================

def solicitar_limite(mensaje, minimo_permitido=1):
    """
    Solicita un valor numérico validando la entrada.
    Principio: DRY (Don't Repeat Yourself).
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo_permitido:
                return valor
            else:
                print(f"⚠️  El valor debe ser al menos {minimo_permitido}. Intenta de nuevo.\n")
        except ValueError:
            print("⚠️  Entrada inválida. Por favor, ingresa un número entero.\n")


def configurar_juego():
    """
    Permite al usuario definir los parámetros del juego.
    Principio: SRP (Separa la configuración de la ejecución).
    """
    print("\n" + "="*60)
    print("🎮 CONFIGURACIÓN DEL JUEGO")
    print("="*60)
    
    limite_inferior = solicitar_limite(" Ingresa el límite INFERIOR del rango: ")
    
    while True:
        limite_superior = solicitar_limite(" Ingresa el límite SUPERIOR del rango: ")
        if limite_superior > limite_inferior:
            break
        print(f"⚠️  El límite superior debe ser mayor que {limite_inferior}.\n")
    
    max_intentos = solicitar_limite("🎯 ¿Cuántos intentos deseas tener? (mínimo 1): ", minimo_permitido=1)
    
    return limite_inferior, limite_superior, max_intentos


# ============================================================================
# 3. FUNCIONES DE INTERFAZ (Presentación visual)
# ============================================================================

def mostrar_bienvenida(limite_inferior, limite_superior, max_intentos):
    """Muestra el mensaje de bienvenida e instrucciones."""
    print("\n" + "="*60)
    print("🎲 ¡BIENVENIDO AL JUEGO DE ADIVINANZA! 🎲")
    print("="*60)
    print(f"\n INSTRUCCIONES:")
    print(f"   • He pensado un número entre {limite_inferior} y {limite_superior}")
    print(f"   • Tienes {max_intentos} intentos para adivinarlo")
    print(f"   • Presiona ESC antes de ingresar un número para salir")
    print("="*60 + "\n")


def mostrar_estado_intentos(intentos_restantes, max_intentos):
    """Muestra el progreso visual de los intentos."""
    intentos_usados = max_intentos - intentos_restantes
    barra = "█" * intentos_usados + "░" * intentos_restantes
    print(f"\n📊 Progreso: [{barra}] {intentos_restantes} intento(s) restante(s)")


def solicitar_numero_usuario(limite_inferior, limite_superior):
    """Solicita y valida la entrada numérica del usuario."""
    while True:
        try:
            numero = int(input("\n🔢 Ingresa tu número: "))
            if verificar_en_intervalo(limite_inferior, limite_superior, numero):
                return numero
            else:
                print(f"⚠️  El número debe estar entre {limite_inferior} y {limite_superior}")
        except ValueError:
            print("⚠️  Entrada inválida. Ingresa solo números enteros.")


def evaluar_intento(numero_usuario, numero_secreto):
    """Compara el número y retorna el estado de la jugada."""
    if numero_usuario == numero_secreto:
        return 'correcto'
    elif numero_usuario < numero_secreto:
        print("📈 ¡El número secreto es MAYOR!")
        return 'menor'
    else:
        print("📉 ¡El número secreto es MENOR!")
        return 'mayor'


def mostrar_resultado_final(gano, numero_secreto, intentos_usados):
    """Muestra el mensaje de victoria o derrota."""
    print("\n" + "="*60)
    if gano:
        print("🎉 ¡FELICIDADES! ¡HAS GANADO! 🎉")
        print(f"   Adivinaste el número {numero_secreto} en {intentos_usados} intento(s)")
    else:
        print("💀 ¡FIN DEL JUEGO! 💀")
        print(f"   Te quedaste sin intentos. El número era: {numero_secreto}")
    print("="*60 + "\n")


# ============================================================================
# 4. FUNCIONES DE CONTROL DE FLUJO (Lógica del juego)
# ============================================================================

def detectar_tecla_esc():
    """
    Verifica de forma no bloqueante si se presionó ESC.
    Nota: Se ejecuta entre turnos para no interrumpir el input() nativo.
    """
    if msvcrt.kbhit():
        tecla = msvcrt.getch()
        if ord(tecla) == 27: # 27 es el código ASCII de ESC
            return True
    return False


def ejecutar_ronda(limite_inferior, limite_superior, max_intentos):
    """
    Ejecuta una partida completa.
    Returns: True si la ronda terminó normal, False si se presionó ESC.
    """
    numero_secreto = generar_aleatorio(limite_inferior, limite_superior)
    intentos_restantes = max_intentos
    
    mostrar_bienvenida(limite_inferior, limite_superior, max_intentos)
    
    while intentos_restantes > 0:
        # Verificar si el usuario quiere salir antes de pedir el número
        if detectar_tecla_esc():
            print("\n\n👋 Saliendo del juego... ¡Hasta pronto!")
            return False
        
        mostrar_estado_intentos(intentos_restantes, max_intentos)
        numero_usuario = solicitar_numero_usuario(limite_inferior, limite_superior)
        resultado = evaluar_intento(numero_usuario, numero_secreto)
        
        if resultado == 'correcto':
            intentos_usados = max_intentos - intentos_restantes + 1
            mostrar_resultado_final(True, numero_secreto, intentos_usados)
            return True # Ronda terminada exitosamente
            
        intentos_restantes -= 1
    
    # Si el bucle termina, se agotaron los intentos
    mostrar_resultado_final(False, numero_secreto, max_intentos)
    return True # Ronda terminada por derrota, pero no por ESC


def preguntar_continuar():
    """Pregunta al usuario si desea jugar otra ronda."""
    print("\n" + "-"*60)
    respuesta = input("¿Deseas jugar otra ronda? (s/n): ").strip().lower()
    print("-"*60)
    return respuesta == 's'


# ============================================================================
# 5. EJECUCIÓN SECUENCIAL DEL PROGRAMA (Ámbito Global)
# ============================================================================

print("\n" + "🎮" * 30)
print("   JUEGO DE ADIVINANZA - PYTHON")
print("🎮" * 30)

# Paso 1: Configurar los parámetros iniciales
limite_inferior, limite_superior, max_intentos = configurar_juego()

# Paso 2: Bucle principal que mantiene el juego activo
juego_activo = True

while juego_activo:
    # Ejecutar la ronda y guardar su estado de salida
   # continuar_juego=      Completar la implementacion llamando a la funcion adecuada. 
    
    # Si la función retornó False, significa que se presionó ESC
    if not continuar_juego:
        #Completar ruptura de la ejecucion.
    
    # Si la ronda terminó normal, preguntar si quiere repetir
    if not preguntar_continuar():
        print("\n👋 ¡Gracias por jugar! ¡Hasta la próxima!")
        juego_activo = False
    else:
        # Dar la opción de reconfigurar los límites o intentos
        reconfigurar = input("\n¿Deseas cambiar la configuración del juego? (s/n): ").strip().lower()
        if reconfigurar == 's':
            limite_inferior, limite_superior, max_intentos = # llamar a la funcion adecuada

print("\n✅ Programa finalizado correctamente.\n")