# =====================================================================
# PASO 1: ESTRUCTURA BASE E INICIALIZACIÓN DE VENTANA EN PYGAME
# =====================================================================

import pygame
import sys

# 1. Inicializamos todos los módulos internos de hardware de Pygame
pygame.init()

# 2. Definimos las dimensiones de la pantalla (Ancho, Alto) en píxeles
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# Creamos el lienzo o superficie principal de dibujo
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Colocamos un título a la ventana del sistema
pygame.display.set_caption("Paso 1: Inicialización del Lienzo")

# 3. Definimos los colores usando el formato numérico RGB (Red, Green, Blue)
COLOR_FONDO = (30, 40, 50)  # Un azul grisáceo oscuro

# 4. BUCLE PRINCIPAL DEL JUEGO (Mantiene la ventana viva)
ejecutando = True

while ejecutando:
    # --- A. Gestión de Eventos (Entradas del usuario) ---
    # Revisamos la cola de acciones que el usuario hizo en la computadora
    for evento in pygame.event.get():
        # Si el usuario hace clic en el botón de cerrar de la ventana (X)
        if evento.type == pygame.QUIT:
            ejecutando = False

    # --- B. Renderizado Gráfico (Dibujo en el lienzo) ---
    # Limpiamos la pantalla pintando el fondo completo con nuestro color RGB
    pantalla.fill(COLOR_FONDO)

    # --- C. Actualización de Pantalla (Flip) ---
    # Pygame dibuja en un "lienzo oculto" en memoria RAM. Esta línea proyecta
    # todo el dibujo de golpe en el monitor del usuario evitando el parpadeo.
    pygame.display.flip()

# 5. Cierre limpio del programa al salir del bucle while
pygame.quit()
sys.exit()