def estimador_bateria():
    print("="*50)
    print("BIENVENIDO AL ESTIMADOR DE BATERÍA - SMARTFIT V2")
    print("="*50)
    
    continuar = True
    
    # Uso de estructura WHILE para mantener el programa en ejecución
    while continuar:
        nombre_cliente = input("\nIngrese el nombre del cliente: ")
        total_horas_intensivas = 0
        
        print(f"\n--- Analizando perfil semanal de {nombre_cliente} ---")
        
        # Uso de estructura FOR para iterar los 7 días de la semana
        for dia in range(1, 8):
            while True:
                try:
                    horas = float(input(f"Día {dia} - Horas de uso intensivo (GPS/Deporte): "))
                    if 0 <= horas <= 24:
                        total_horas_intensivas += horas
                        break
                    else:
                        print("Error: Ingrese un valor válido entre 0 y 24.")
                except ValueError:
                    print("Error: Por favor ingrese un número válido.")
        
        # Operadores y lógica matemática
        promedio_diario = total_horas_intensivas / 7
        bateria_base = 120 # horas de batería en reposo
        
        # Estructuras de control condicionales (if/elif/else)
        if promedio_diario <= 1.0:
            perfil = "Básico"
            autonomia_estimada = bateria_base - (promedio_diario * 10)
        elif promedio_diario <= 3.0:
            perfil = "Intermedio"
            autonomia_estimada = bateria_base - (promedio_diario * 15)
        else:
            perfil = "Extremo"
            autonomia_estimada = bateria_base - (promedio_diario * 20)
            
        print("\n" + "-"*30)
        print("RESULTADOS DEL ANÁLISIS:")
        print("-"*30)
        print(f"Cliente: {nombre_cliente}")
        print(f"Perfil de usuario: {perfil}")
        print(f"Promedio de uso intensivo diario: {promedio_diario:.2f} horas")
        print(f"Autonomía de batería estimada: {autonomia_estimada:.2f} horas por carga completa")
        print("-"*30)
        
        # Validación para continuar o salir del ciclo while
        respuesta = input("\n¿Desea evaluar a otro cliente? (s/n): ").lower()
        if respuesta != 's':
            continuar = False
            print("\nGracias por usar el sistema de relanzamiento SmartFit V2. ¡Hasta pronto!")

# Llamada a la función principal
if __name__ == "__main__":
    estimador_bateria()