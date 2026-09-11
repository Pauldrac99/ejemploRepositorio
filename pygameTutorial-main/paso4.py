# =====================================================================
# PASO 4: INTERACTIVIDAD Y COLISIÓN GEOMÉTRICA (BOTÓN CON MOUSE)
# =====================================================================

import pygame
import sys

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Paso 4: Cuadrado como Botón Interactivo")

# --- PALETA DE COLORES REACTIVA ---
COLOR_GRIS = (100, 110, 120)
COLOR_AMARILLO_NORMAL = (230, 180, 0)   # Amarillo estándar
COLOR_AMARILLO_HOVER = (255, 225, 50)   # Amarillo brillante al pasar el mouse
COLOR_CLICK = (255, 255, 255)            # Blanco temporal al hacer clic

# Variable para almacenar el color dinámico del botón en cada fotograma
color_actual_boton = COLOR_AMARILLO_NORMAL

# --- CONFIGURACIÓN DEL BOTÓN GEOMÉTRICO ---
TAMANIO_BOTON = 150
boton_rect = pygame.Rect(0, 0, TAMANIO_BOTON, TAMANIO_BOTON)
boton_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)

# BUCLE PRINCIPAL
ejecutando = True
while ejecutando:
    
    # 1. Obtener la posición (X, Y) del mouse en este instante continuo
    posicion_mouse = pygame.mouse.get_pos()
    
    # --- DETECCIÓN DE EVENTOS DE HARDWARE ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        # Detectamos si el usuario PRESIONÓ un botón del mouse
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # evento.button == 1 representa estrictamente el CLIC IZQUIERDO
            if evento.button == 1:
                # Evaluamos si la coordenada del clic cayó dentro del botón
                if boton_rect.collidepoint(posicion_mouse):
                    print("🎯 [EVENTO]: ¡El botón central ha sido pulsado con éxito!")
                    color_actual_boton = COLOR_CLICK
                    
        # Detectamos cuando el usuario SUELTA el botón del mouse
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                # Retornamos al estado normal si se liberó el clic
                color_actual_boton = COLOR_AMARILLO_NORMAL

    # --- LÓGICA DE DETECCIÓN 'HOVER' (Cambio de color visual pasivo) ---
    # Si el botón no está en estado "Click" (Blanco), evaluamos si el mouse está encima
    if color_actual_boton != COLOR_CLICK:
        if boton_rect.collidepoint(posicion_mouse):
            color_actual_boton = COLOR_AMARILLO_HOVER
        else:
            color_actual_boton = COLOR_AMARILLO_NORMAL

    # --- RENDERIZADO GRÁFICO ---
    pantalla.fill(COLOR_GRIS)
    
    # Dibujamos el cuadrado usando el color calculado dinámicamente en este frame
    pygame.draw.rect(pantalla, color_actual_boton, boton_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
#Paso 4: mostrar un texto indicando el CLIC