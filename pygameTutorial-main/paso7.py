# =====================================================================
# PASO 7: SIMULACIÓN DE TRAYECTORIA PARABÓLICA INTERACTIVA
# =====================================================================

import pygame
import sys
import math

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Paso 7: Simulador de Lanzamiento Parabólico")

reloj = pygame.time.Clock()

# --- PALETA DE COLORES ---
COLOR_GRIS = (100, 110, 120)
COLOR_AMARILLO = (255, 215, 0)   # Proyectil
COLOR_ROJO = (230, 57, 70)       # Botón de disparo
COLOR_VERDE = (46, 204, 113)     # Vector de ángulo
COLOR_BLANCO = (255, 255, 255)

# --- CONFIGURACIÓN DEL PROYECTIL (CUADRADO AMARILLO) ---
X_INICIAL = 10
Y_INICIAL = 500
proyectil_rect = pygame.Rect(X_INICIAL, Y_INICIAL, 10, 10)

# --- CONFIGURACIÓN DEL BOTÓN (CUADRADO ROJO) ---
# Esquina inferior derecha: ancho ventana - margen - lado botón
boton_rect = pygame.Rect(ANCHO_VENTANA - 40, ALTO_VENTANA - 40, 20, 20)

# --- VARIABLES FÍSICAS DE LA SIMULACIÓN ---
GRAVEDAD = 0.25         # Aceleración hacia abajo (píxeles/frame²)
VELOCIDAD_INICIAL = 12  # Magnitud del impulso inicial (píxeles/frame)

angulo_grados = 45.0    # Ángulo inicial por defecto
vx = 0.0                # Componente de velocidad X
vy = 0.0                # Componente de velocidad Y

# Estados: "CONFIGURANDO" (Espera entrada/disparo) o "EN_VUELO"
estado_juego = "CONFIGURANDO"

print("========================================================")
print("       LABORATORIO DE CINEMÁTICA: PARÁBOLA COMPUTACIONAL")
print("========================================================")
print(" Instrucciones:")
print("  1. Introduce el ángulo en la terminal cuando se solicite.")
print("  2. Haz clic en el CUADRADO ROJO (esquina inf. der.) para disparar.")
print("  3. Presiona ESC en la ventana para salir.")
print("========================================================")

# BUCLE PRINCIPAL
ejecutando = True
while ejecutando:
    
    posicion_mouse = pygame.mouse.get_pos()
    
    # --- 1. GESTIÓN DE EVENTOS Y ENTRADAS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
                
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clic izquierdo
                
                # Si hacemos clic en el botón rojo y estamos listos para disparar
                if estado_juego == "CONFIGURANDO" and boton_rect.collidepoint(posicion_mouse):
                    # PEDIR ÁNGULO POR CONSOLA (Síncrono)
                    try:
                        print("\n[CONFIGURACIÓN DE DISPARO]")
                        entrada = input(" Ingrese ángulo de elevación (0 a 90 grados): ")
                        angulo_grados = float(entrada)
                        
                        # Restringimos pedagógicamente entre 0 y 90
                        angulo_grados = max(0.0, min(90.0, angulo_grados))
                    except ValueError:
                        print(" ❌ Entrada inválida. Usando ángulo por defecto (45°).")
                        angulo_grados = 45.0
                    
                    # --- CÁLCULO VECTORIAL DE VELOCIDADES ---
                    radianes = math.radians(angulo_grados)
                    
                    # X avanza a la derecha (positivo)
                    vx = VELOCIDAD_INICIAL * math.cos(radianes)
                    # Y debe subir (en Pygame subir es restar -=, por eso es negativo)
                    vy = -VELOCIDAD_INICIAL * math.sin(radianes)
                    
                    # Activamos el motor físico
                    estado_juego = "EN_VUELO"
                    print(f"🚀 ¡Disparo efectuado! Ángulo: {angulo_grados}° | vx: {vx:.2f} | vy: {vy:.2f}")

    # --- 2. MOTOR DE FÍSICA (ACTUALIZACIÓN CONTINUA) ---
    if estado_juego == "EN_VUELO":
        # Aplicamos las velocidades a las coordenadas del proyectil
        proyectil_rect.x += int(vx)
        proyectil_rect.y += int(vy)
        
        # Efecto de la gravedad: altera la velocidad vertical en cada fotograma
        vy += GRAVEDAD 
        
        # CONDICIÓN DE LÍMITE: Si cae al suelo o sale de la pantalla, se resetea
        if proyectil_rect.y >= Y_INICIAL or proyectil_rect.x >= ANCHO_VENTANA:
            proyectil_rect.x = X_INICIAL
            proyectil_rect.y = Y_INICIAL
            estado_juego = "CONFIGURANDO"
            print("🏁 [SISTEMA]: El proyectil impactó el suelo. Reiniciando lanzador.")

    # --- 3. RENDERIZADO GRÁFICO ---
    pantalla.fill(COLOR_GRIS)
    
    # Dibujamos la línea de tierra (Suelo analítico)
    pygame.draw.line(pantalla, COLOR_BLANCO, (0, Y_INICIAL + 10), (ANCHO_VENTANA, Y_INICIAL + 10), 2)
    
    # Dibujamos el Botón de Disparo (Cuadrado Rojo)
    pygame.draw.rect(pantalla, COLOR_ROJO, boton_rect)
    
    # DIBUJO DEL VECTOR ÁNGULO (Línea Verde)
    # Se dibuja partiendo desde el centro del proyectil solo en fase de configuración
    if estado_juego == "CONFIGURANDO":
        rad_linea = math.radians(angulo_grados)
        LARGO_LINEA = 50
        # Calculamos el punto final del vector apuntando hacia arriba
        linea_fin_x = X_INICIAL + 5 + int(LARGO_LINEA * math.cos(rad_linea))
        linea_fin_y = Y_INICIAL + 5 - int(LARGO_LINEA * math.sin(rad_linea))
        pygame.draw.line(pantalla, COLOR_VERDE, (X_INICIAL + 5, Y_INICIAL + 5), (linea_fin_x, linea_fin_y), 3)

    # Dibujamos el Proyectil (Cuadrado Amarillo)
    pygame.draw.rect(pantalla, COLOR_AMARILLO, proyectil_rect)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()