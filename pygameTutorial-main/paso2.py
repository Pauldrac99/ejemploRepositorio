# =====================================================================
# PASO 2: TEXTO RENDERIZADO Y CENTRADO EN PYGAME
# =====================================================================

import pygame
import sys

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Paso 2: Texto Centrado")

# Colores (RGB)
COLOR_FONDO = (30, 40, 50)
COLOR_TEXTO = (241, 250, 240) # Blanco hueso

# --- CONFIGURACIÓN DEL TEXTO ---
# 1. Cargamos una fuente del sistema (None usa la tipografía por defecto de Pygame, tamaño 40)
fuente = pygame.font.SysFont(None, 40)

# 2. Renderizamos el texto. El segundo parámetro (True) activa el Antialiasing (suavizado de bordes)
superficie_texto = fuente.render("Bienvenidos al Laboratorio de Matemáticas", True, COLOR_TEXTO)

# 3. GEOMETRÍA: Obtenemos el rectángulo contenedor de la imagen de texto
rectangulo_texto = superficie_texto.get_rect()

# 4. Centramos el rectángulo usando las coordenadas medias de la ventana
rectangulo_texto.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)


# BUCLE PRINCIPAL
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Renderizado
    pantalla.fill(COLOR_FONDO)
    
    # Dibujamos ('bliteamos') el texto en la pantalla usando su rectángulo posicional
    pantalla.blit(superficie_texto, rectangulo_texto)

    pygame.display.flip()

pygame.quit()
sys.exit()

#Usar un INPUT para añadir tu nombre al texto mostrado. HOLA {NOMBRE}!!!