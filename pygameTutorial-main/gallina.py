# =====================================================================
# LABORATORIO 2D: TRANSFORMACIÓN MULTIPLICATIVA EN EL ORIGEN (CENTRO)
# =====================================================================
import pygame
import sys
import os

# --- INICIALIZACIÓN ---
pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laboratorio 2D: Transformación Multiplicativa de la Gallina")
reloj = pygame.time.Clock()

# --- DEFINICIÓN CARTESIANA DEL ORIGEN ---
# Definimos el centro de la pantalla como nuestro origen (0, 0)
ORIGEN_X = ANCHO_VENTANA // 2
ORIGEN_Y = ALTO_VENTANA // 2

# --- COLORES ---
COLOR_GRIS = (60, 63, 65)
COLOR_BLANCO = (255, 255, 255)
COLOR_AMARILLO = (255, 215, 0)
COLOR_TEXTO = (200, 200, 200)

# --- FUENTES Y SPRITE (EMOJI) ---
fuente_datos = pygame.font.SysFont("monospace", 18)
fuente_gallina = pygame.font.SysFont("segoe ui emoji", 60) # Fuente especial para emojis
superficie_gallina = fuente_gallina.render("🐔", True, COLOR_BLANCO)
gallina_rect = superficie_gallina.get_rect()

# --- VARIABLES CARTESIANAS INICIALES (Respecto al origen) ---
# Empezamos en el centro de la pantalla (nuestro origen matemático)
x_cartesiana = 1.0
y_cartesiana = 1.0

# Actualizamos la posición inicial en pantalla (coordenadas de Pygame)
gallina_rect.center = (ORIGEN_X + int(x_cartesiana), ORIGEN_Y - int(y_cartesiana))

# Variables para guardar los inputs del teclado
input_a = ""
input_b = ""
ingresando_a = True # Estado: True para ingresar 'a', False para ingresar 'b'
mensaje_sistema = "Ingrese multiplicador 'a' (X) y presione ENTER."

# BUCLE PRINCIPAL (Bucle infinito)
ejecutando = True
while ejecutando:
    
    # --- 1. GESTIÓN DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        elif evento.type == pygame.KEYDOWN:
            # Condición de detención: Tecla Esc
            if evento.key == pygame.K_ESCAPE:
                print("🛑 [SISTEMA]: ESC presionado. Saliendo del programa.")
                ejecutando = False
            
            # Condición de transformación: Tecla Enter
            elif evento.key == pygame.K_RETURN:
                if ingresando_a:
                    # Cambiar a input de 'b'
                    if input_a == "": input_a = "1.0" # Valor por defecto
                    ingresando_a = False
                    mensaje_sistema = "Ingrese multiplicador 'b' (Y) y presione ENTER."
                else:
                    # Ejecutar transformación matricial
                    if input_b == "": input_b = "1.0" # Valor por defecto
                    try:
                        multiplicador_a = float(input_a)
                        multiplicador_b = float(input_b)
                        
                        # Guardar coordenadas viejas para mostrar en pantalla
                        x_vieja = x_cartesiana
                        y_vieja = y_cartesiana
                        
                        # --- MOTOR DE TRANSFORMACIÓN (Álgebra Lineal) ---
                        # Multiplicamos las coordenadas actuales por el par (a, b)
                        x_cartesiana = x_cartesiana * multiplicador_a
                        y_cartesiana = y_cartesiana * multiplicador_b
                        
                        # Actualizar mensaje del sistema
                        print(f"🐔 [TRANSFORMACIÓN]: ( {x_vieja:.1f}, {y_vieja:.1f} ) * [ {multiplicador_a}, {multiplicador_b} ] = ( {x_cartesiana:.1f}, {y_cartesiana:.1f} )")
                        mensaje_sistema = f"Transformación: ({x_vieja:.1f},{y_vieja:.1f}) * [{multiplicador_a},{multiplicador_b}] = ({x_cartesiana:.1f},{y_cartesiana:.1f})"
                        
                        # Resetear inputs para la siguiente transformación
                        input_a = ""
                        input_b = ""
                        ingresando_a = True # Volver a pedir 'a'
                        
                    except ValueError:
                        print("❌ [ERROR]: Por favor ingrese números válidos.")
                        input_a = ""
                        input_b = ""
                        ingresando_a = True
                        mensaje_sistema = "Error. Ingrese multiplicador 'a' y presione ENTER."

            # Captura de números y punto decimal
            elif evento.key == pygame.K_BACKSPACE:
                if ingresando_a: input_a = input_a[:-1]
                else: input_b = input_b[:-1]
            elif evento.unicode.isdigit() or evento.unicode == ".":
                if ingresando_a: input_a += evento.unicode
                else: input_b += evento.unicode

    # --- 2. ACTUALIZACIÓN DEL SPRITE (Sincronización Pygame-Cartesiana) ---
    # Convertimos las coordenadas matemáticas a píxeles de pantalla de Pygame
    # Nota: Eje Y invertido en pantallas, por eso restamos la y_cartesiana
    pygame_x = ORIGEN_X + int(x_cartesiana)
    pygame_y = ORIGEN_Y - int(y_cartesiana)
    gallina_rect.center = (pygame_x, pygame_y)

    # --- 3. RENDERIZADO GRÁFICO ---
    pantalla.fill(COLOR_GRIS)
    
    # Dibujar los Ejes Cartesianos guía (Centro)
    pygame.draw.line(pantalla, COLOR_BLANCO, (ORIGEN_X, 0), (ORIGEN_X, ALTO_VENTANA), 1) # Eje Y
    pygame.draw.line(pantalla, COLOR_BLANCO, (0, ORIGEN_Y), (ANCHO_VENTANA, ORIGEN_Y), 1) # Eje X

    # Dibujar la gallina 🐔 en su nueva posición
    pantalla.blit(superficie_gallina, gallina_rect)
    
    # --- RENDERIZADO DEL PANEL DE DATOS ---
    # Título
    surface_titulo = fuente_datos.render("LABORATORIO 2D: TRANSFORMACIÓN MULTIPLICATIVA", True, COLOR_BLANCO)
    pantalla.blit(surface_titulo, (20, 15))
    
    # Coordenadas Actuales (Matemáticas, respecto al origen)
    txt_coords = f"Posición Gallina 🐔 (respecto al origen): ( X: {x_cartesiana:.1f} , Y: {y_cartesiana:.1f} )"
    surface_coords = fuente_datos.render(txt_coords, True, COLOR_AMARILLO)
    pantalla.blit(surface_coords, (20, 45))
    
    # Panel de Input de Usuario
    txt_input_a = f"Multiplicador 'a' (X): {'*' * len(input_a)} ({input_a}) " if ingresando_a else f"Multiplicador 'a' (X): {input_a}"
    txt_input_b = f"Multiplicador 'b' (Y): {'*' * len(input_b)} ({input_b}) " if not ingresando_a else f"Multiplicador 'b' (Y): {input_b}"
    
    color_a = COLOR_BLANCO if ingresando_a else COLOR_TEXTO
    color_b = COLOR_BLANCO if not ingresando_a else COLOR_TEXTO
    
    surface_input_a = fuente_datos.render(txt_input_a, True, color_a)
    surface_input_b = fuente_datos.render(txt_input_b, True, color_b)
    surface_mensaje = fuente_datos.render(f"SISTEMA: {mensaje_sistema}", True, COLOR_TEXTO)
    
    pantalla.blit(surface_input_a, (20, 85))
    pantalla.blit(surface_input_b, (20, 110))
    pantalla.blit(surface_mensaje, (20, 140))
    
    # Instrucción de salida
    surface_esc = fuente_datos.render("[Presione ESC para salir]", True, COLOR_BLANCO)
    pantalla.blit(surface_esc, (ANCHO_VENTANA - 240, ALTO_VENTANA - 30))

    pygame.display.flip()
    reloj.tick(60) # Mantener tasa de refresco estable

pygame.quit()
sys.exit()