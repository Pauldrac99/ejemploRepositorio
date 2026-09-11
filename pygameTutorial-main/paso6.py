# =====================================================================
# PASO 6: CINEMÁTICA LIBRE CONTROLADA POR TECLADO
# =====================================================================

import pygame
import sys

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Paso 6: Control por Flechas Direccionales")

reloj = pygame.time.Clock()

# --- PALETA DE COLORES ---
COLOR_GRIS = (100, 110, 120)
COLOR_AMARILLO = (230, 180, 0)

# --- CONFIGURACIÓN DEL CUADRADO ---
TAMANIO_CUADRADO = 120
cuadrado_rect = pygame.Rect(0, 0, TAMANIO_CUADRADO, TAMANIO_CUADRADO)
# Iniciamos en el centro de la pantalla
cuadrado_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)

# MAGNITUD DE VELOCIDAD: Píxeles que se desplazará por fotograma
VELOCIDAD = 6

# BUCLE PRINCIPAL
ejecutando = True
while ejecutando:
    
    # --- 1. DETECCIÓN DE INTERRUPCIONES DE HARDWARE ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        # Monitoreamos pulsaciones directas para comandos del sistema (Escape)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                print("[INFO]: Tecla ESC detectada. Saliendo del programa.")
                ejecutando = False

    # --- 2. ESCÁNER CONTINUO DEL TECLADO (MOVIMIENTO SUAVE) ---
    # Captura una lista booleana con el estado de TODAS las teclas en este instante
    teclas = pygame.key.get_pressed()
    
    # Evaluamos los estados de las flechas del cursor
    if teclas[pygame.K_LEFT]:
        cuadrado_rect.x -= VELOCIDAD  # Desplazamiento hacia el Oeste
    if teclas[pygame.K_RIGHT]:
        cuadrado_rect.x += VELOCIDAD  # Desplazamiento hacia el Este
    if teclas[pygame.K_UP]:
        cuadrado_rect.y -= VELOCIDAD  # Desplazamiento hacia el Norte (Eje Y invertido)
    if teclas[pygame.K_DOWN]:
        cuadrado_rect.y += VELOCIDAD  # Desplazamiento hacia el Sur

    # --- 3. RENDERIZADO GRÁFICO ---
    pantalla.fill(COLOR_GRIS)
    
    # Dibujamos el cuadrado en su nueva coordenada calculada
    pygame.draw.rect(pantalla, COLOR_AMARILLO, cuadrado_rect)

    pygame.display.flip()
    
    # Mantenemos la tasa de simulación a 60 FPS estables
    reloj.tick(60)

pygame.quit()
sys.exit()