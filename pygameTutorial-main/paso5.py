# =====================================================================
# PASO 5: CINEMÁTICA Y ANIMACIÓN POR MÁQUINA DE ESTADOS
# =====================================================================

import pygame
import sys

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Paso 5: Animación Secuencial de Ida y Vuelta")

# Herramienta vital para controlar la velocidad de los fotogramas (FPS)
reloj = pygame.time.Clock()

# --- PALETA DE COLORES ---
COLOR_GRIS = (100, 110, 120)
COLOR_AMARILLO = (230, 180, 0)
COLOR_BLANCO = (255, 255, 255)

# --- ANÁLISIS CARTESIANO DE POSICIONES ---
CENTRO_X = ANCHO_VENTANA // 2
CENTRO_Y = ALTO_VENTANA // 2

TAMANIO_BOTON = 150
boton_rect = pygame.Rect(0, 0, TAMANIO_BOTON, TAMANIO_BOTON)
boton_rect.center = (CENTRO_X, CENTRO_Y)

# Guardamos las coordenadas originales exactas del home/centro
HOME_X = boton_rect.x  

# Límites algebraicos del recorrido
LIMITE_DERECHA = HOME_X + 100
LIMITE_IZQUIERDA = HOME_X - 100

# VELOCIDAD: Píxeles que se desplazará el cuadrado en cada fotograma
VELOCIDAD = 4 

# --- CONTROL DE ESTADOS DE ANIMACIÓN ---
# Valores posibles: "IDLE" (Quieto), "DERECHA", "IZQUIERDA", "REGRESANDO"
estado_movimiento = "IDLE"

# BUCLE PRINCIPAL
ejecutando = True
while ejecutando:
    
    posicion_mouse = pygame.mouse.get_pos()
    
    # --- INTERCEPCIÓN DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clic izquierdo
                # Solo iniciamos la coreografía si el cuadrado está quieto ("IDLE")
                if estado_movimiento == "IDLE" and boton_rect.collidepoint(posicion_mouse):
                    estado_movimiento = "DERECHA"
                    print("🚀 [ANIMACIÓN]: Iniciando secuencia de desplazamiento.")

    # --- MOTOR DE FÍSICA / ACTUALIZACIÓN DE POSICIONES ---
    if estado_movimiento == "DERECHA":
        boton_rect.x += VELOCIDAD
        # Condicional de quiebre: si pasa el límite derecho, cambia de dirección
        if boton_rect.x >= LIMITE_DERECHA:
            boton_rect.x = LIMITE_DERECHA # Ajuste de precisión
            estado_movimiento = "IZQUIERDA"
            
    elif estado_movimiento == "IZQUIERDA":
        boton_rect.x -= VELOCIDAD
        # Condicional de quiebre: viaja hasta el extremo izquierdo (-100 px del centro)
        if boton_rect.x <= LIMITE_IZQUIERDA:
            boton_rect.x = LIMITE_IZQUIERDA
            estado_movimiento = "REGRESANDO"
            
    elif estado_movimiento == "REGRESANDO":
        boton_rect.x += VELOCIDAD
        # Condicional de acoplamiento: si vuelve a su coordenada origen, se detiene
        if boton_rect.x >= HOME_X:
            boton_rect.x = HOME_X
            estado_movimiento = "IDLE"
            print("🎯 [ANIMACIÓN]: Cuadrado ha regresado a salvo al centro.")

    # --- RENDERIZADO GRÁFICO ---
    pantalla.fill(COLOR_GRIS)
    
    # Pintamos una línea blanca guía de fondo para ver el rango del recorrido analítico
    pygame.draw.line(pantalla, COLOR_BLANCO, (LIMITE_IZQUIERDA, CENTRO_Y), (LIMITE_DERECHA + TAMANIO_BOTON, CENTRO_Y), 2)
    
    # Dibujamos nuestro cuadrado animado
    pygame.draw.rect(pantalla, COLOR_AMARILLO, boton_rect)

    pygame.display.flip()
    
    # Regulador de velocidad: El bucle se ejecutará estrictamente a 60 FPS
    reloj.tick(60)

pygame.quit()
sys.exit()