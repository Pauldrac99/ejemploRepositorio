# =====================================================================
# PASO 7 MODIFICADO: PARÁBOLA INTERACTIVA CON EFECTOS DE SONIDO
# =====================================================================

import pygame
import sys
import math

# 1. Inicialización estándar del sistema y del mezclador de audio
pygame.init()
pygame.mixer.init() # [SONIDO] Inicializa el hardware de audio de la computadora

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Paso 7: Lanzamiento Parabólico con Audio")

reloj = pygame.time.Clock()

# --- [SONIDO]: CARGA DE ARCHIVOS DE AUDIO ---
# Cargamos los sonidos en la RAM como objetos "Sound" de Pygame
try:
    sonido_disparo = pygame.mixer.Sound("disparo.mp3")
    sonido_impacto = pygame.mixer.Sound("impacto.mp3")
    # 1. Cargamos el archivo MP3 de fondo (no consume RAM, se queda apuntando al disco)
    #pygame.mixer.music.load("fondo.mp3")
    # 2. Ajustamos el volumen (un valor flotante entre 0.0 y 1.0)
    #pygame.mixer.music.set_volume(0.4)
    # 3. Reproducimos la música
    # El parámetro -1 significa "bucle infinito" (cuando termine, vuelve a empezar)
    #pygame.mixer.music.play(-1)
    print("🔊 [SISTEMA]: Efectos de sonido cargados correctamente.")
except pygame.error:
    # Salvaguarda pedagógica: Si no encuentran los archivos, el programa no se cae
    print("⚠️ [ADVERTENCIA]: No se encontraron 'disparo.wav' o 'impacto.wav'. El juego correrá en silencio.")
    sonido_disparo = None
    sonido_impacto = None
    #sonido_fondo = None

# --- PALETA DE COLORES Y GEOMETRÍA ---
COLOR_GRIS = (100, 110, 120)
COLOR_AMARILLO = (255, 215, 0)
COLOR_ROJO = (230, 57, 70)
COLOR_VERDE = (46, 204, 113)
COLOR_BLANCO = (255, 255, 255)

X_INICIAL = 10
Y_INICIAL = 500
proyectil_rect = pygame.Rect(X_INICIAL, Y_INICIAL, 10, 10)
boton_rect = pygame.Rect(ANCHO_VENTANA - 40, ALTO_VENTANA - 40, 20, 20)

GRAVEDAD = 0.25         
VELOCIDAD_INICIAL = 12  
angulo_grados = 45.0    
vx = 0.0                
vy = 0.0                
estado_juego = "CONFIGURANDO"

# BUCLE PRINCIPAL
ejecutando = True
while ejecutando:
    posicion_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
                
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if estado_juego == "CONFIGURANDO" and boton_rect.collidepoint(posicion_mouse):
                    try:
                        print("\n[CONFIGURACIÓN DE DISPARO]")
                        entrada = input(" Ingrese ángulo de elevación (0 a 90 grados): ")
                        angulo_grados = float(entrada)
                        angulo_grados = max(0.0, min(90.0, angulo_grados))
                    except ValueError:
                        angulo_grados = 45.0
                    
                    radianes = math.radians(angulo_grados)
                    vx = VELOCIDAD_INICIAL * math.cos(radianes)
                    vy = -VELOCIDAD_INICIAL * math.sin(radianes)
                    
                    estado_juego = "EN_VUELO"
                    
                    # --- [SONIDO]: REPRODUCCIÓN AL DISPARAR ---
                    if sonido_disparo:
                        sonido_disparo.play() # Se reproduce de fondo sin detener el bucle
                    
                    print(f"🚀 ¡Disparo! Ángulo: {angulo_grados}°")

    # --- MOTOR DE FÍSICA ---
    if estado_juego == "EN_VUELO":
        proyectil_rect.x += int(vx)
        proyectil_rect.y += int(vy)
        vy += GRAVEDAD 
        
        # CONDICIÓN DE LÍMITE (IMPACTO)
        if proyectil_rect.y >= Y_INICIAL or proyectil_rect.x >= ANCHO_VENTANA:
            proyectil_rect.x = X_INICIAL
            proyectil_rect.y = Y_INICIAL
            estado_juego = "CONFIGURANDO"
            
            # --- [SONIDO]: REPRODUCCIÓN AL IMPACTAR ---
            if sonido_impacto:
                sonido_impacto.play()
                
            print("🏁 [SISTEMA]: El proyectil impactó el suelo.")

    # --- RENDERIZADO GRÁFICO ---
    pantalla.fill(COLOR_GRIS)
    pygame.draw.line(pantalla, COLOR_BLANCO, (0, Y_INICIAL + 10), (ANCHO_VENTANA, Y_INICIAL + 10), 2)
    pygame.draw.rect(pantalla, COLOR_ROJO, boton_rect)
    
    if estado_juego == "CONFIGURANDO":
        rad_linea = math.radians(angulo_grados)
        LARGO_LINEA = 50
        linea_fin_x = X_INICIAL + 5 + int(LARGO_LINEA * math.cos(rad_linea))
        linea_fin_y = Y_INICIAL + 5 - int(LARGO_LINEA * math.sin(rad_linea))
        pygame.draw.line(pantalla, COLOR_VERDE, (X_INICIAL + 5, Y_INICIAL + 5), (linea_fin_x, linea_fin_y), 3)

    pygame.draw.rect(pantalla, COLOR_AMARILLO, proyectil_rect)
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()