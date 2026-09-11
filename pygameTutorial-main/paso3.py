# =====================================================================
# PASO 3: DIBUJO DE GEOMETRÍA PLANA (CUADRADO CENTRADO)
# =====================================================================

import pygame
import sys

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
# --- NUEVA PALETA DE COLORES (RGB) ---
COLOR_GRIS = (100, 110, 120)       # Fondo Gris Medio
COLOR_AMARILLO = (255, 215, 0)     # Cuadrado Amarillo (Gold)
# --- CONFIGURACIÓN GEOMÉTRICA DEL CUADRADO ---
TAMANIO_CUADRADO = 150  # Lado del cuadrado en píxeles

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Paso 3: Cuadrado Amarillo Centrado")

# 1. Creamos el objeto rectangular con dimensiones (X, Y, Ancho, Alto)
# Lo inicializamos temporalmente en el origen (0, 0)
cuadrado_rect = pygame.Rect(0, 0, TAMANIO_CUADRADO, TAMANIO_CUADRADO)

# 2. Centramos el objeto asignando las coordenadas medias de la pantalla
cuadrado_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)


# BUCLE PRINCIPAL
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # --- Renderizado Gráfico ---
    # Pintamos el fondo gris solicitado
    pantalla.fill(COLOR_GRIS)
    
    # Dibujamos el cuadrado amarillo en la pantalla
    # Argumentos: (Superficie destino, Color, Objeto Rect)
    pygame.draw.rect(pantalla, COLOR_AMARILLO, cuadrado_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()

#Paso 3 : Pidas las coordenadas del cuadrado antes de dibujarse.