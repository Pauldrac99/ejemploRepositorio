# =====================================================================
# VARIACIÓN PASO 4: ESCÁNER DE COORDENADAS EN TIEMPO REAL
# =====================================================================

import pygame
import sys

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Variación Paso 4: Escáner de Coordenadas Cartesianas")

# --- PALETA DE COLORES ---
COLOR_GRIS = (100, 110, 120)
COLOR_AMARILLO_NORMAL = (230, 180, 0)
COLOR_AMARILLO_HOVER = (255, 225, 50)
COLOR_CLICK = (255, 255, 255)
COLOR_TEXTO = (251, 255, 250)
COLOR_TEXTO_PANEL = (40, 50, 60)

color_actual_boton = COLOR_AMARILLO_NORMAL

# --- CONFIGURACIÓN DE FUENTES ---
# Cargamos una fuente pequeña para las coordenadas
fuente_datos = pygame.font.SysFont("monospace", 16) 

# --- CONFIGURACIÓN DEL BOTÓN GEOMÉTRICO ---
TAMANIO_BOTON = 160
boton_rect = pygame.Rect(0, 0, TAMANIO_BOTON, TAMANIO_BOTON)
boton_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)

# BUCLE PRINCIPAL
ejecutando = True
while ejecutando:
    
    # 1. Capturamos la posición (X, Y) del puntero en este fotograma
    posicion_mouse = pygame.mouse.get_pos()
    x_mouse, y_mouse = posicion_mouse
    
    # --- DETECCIÓN DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clic izquierdo
                if boton_rect.collidepoint(posicion_mouse):
                    color_actual_boton = COLOR_CLICK
                    
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                color_actual_boton = COLOR_AMARILLO_NORMAL

    # --- LÓGICA HOVER ---
    if color_actual_boton != COLOR_CLICK:
        if boton_rect.collidepoint(posicion_mouse):
            color_actual_boton = COLOR_AMARILLO_HOVER
        else:
            color_actual_boton = COLOR_AMARILLO_NORMAL

    # --- RENDERIZADO GRÁFICO ---
    pantalla.fill(COLOR_GRIS)
    
    # 1. Dibujamos el cuadrado central
    pygame.draw.rect(pantalla, color_actual_boton, boton_rect)
    
    # 2. PROCESAMIENTO DE TEXTO DINÁMICO (Se calcula en cada frame)
    # Cadenas de texto con los datos analíticos
    txt_mouse = f"Puntero Mouse : X = {x_mouse:<3} | Y = {y_mouse:<3}"
    txt_cuadrado = f"Caja Botón    : X_izq={boton_rect.left} | X_der={boton_rect.right} | Y_sup={boton_rect.top} | Y_inf={boton_rect.bottom}"
    txt_colision = f"¿Colisión?    : {boton_rect.collidepoint(posicion_mouse)}"
    
    # Renderizamos los strings a superficies de píxeles
    surface_txt_mouse = fuente_datos.render(txt_mouse, True, COLOR_TEXTO)
    surface_txt_cuadrado = fuente_datos.render(txt_cuadrado, True, COLOR_TEXTO)
    surface_txt_colision = fuente_datos.render(txt_colision, True, COLOR_TEXTO)
    
    # 3. Dibujamos un panel oscuro de fondo en la zona superior para leer bien los datos
    pygame.draw.rect(pantalla, COLOR_TEXTO_PANEL, (0, 0, ANCHO_VENTANA, 120))
    
    # Proyectamos las tres líneas de texto en la zona superior (con desfase en Y)
    pantalla.blit(surface_txt_mouse, (20, 15))
    pantalla.blit(surface_txt_cuadrado, (20, 45))
    pantalla.blit(surface_txt_colision, (20, 75))

    pygame.display.flip()

pygame.quit()
sys.exit()