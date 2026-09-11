# =====================================================================
# GEOMETRÍA DINÁMICA: ROTACIÓN DE UN TRIÁNGULO EN PYGAME
# =====================================================================

import pygame
import sys
import math

# --- 1. CONFIGURACIÓN E INICIALIZACIÓN DE ENTORNO ---
pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laboratorio de Geometría: Rotación de Triángulos")

# Colores en formato RGB
COLOR_FONDO = (29, 53, 87)       # Azul oscuro
COLOR_TRIANGULO = (168, 218, 220) # Azul claro / Turquesa
COLOR_CENTRO = (230, 57, 70)     # Rojo (Pivote)

# --- 2. CONFIGURACIÓN GEOMÉTRICA DEL TRIÁNGULO ---
# Definimos un tamaño en píxeles que represente analíticamente el "Lado = 1"
LADO_PIXELES = 150 

# Calculamos la altura de un triángulo equilátero usando Pitágoras: h = lado * sqrt(3)/2
altura_triangulo = LADO_PIXELES * (math.sqrt(3) / 2)

# Vértices originales relativos al centro de gravedad (pivote) del triángulo
VERTICES_ORIGINALES = [
    (0, -2/3 * altura_triangulo),                  # Vértice Superior (A)
    (-LADO_PIXELES / 2, 1/3 * altura_triangulo),   # Vértice Inferior Izquierdo (B)
    (LADO_PIXELES / 2, 1/3 * altura_triangulo)     # Vértice Inferior Derecho (C)
]

# El centro de la pantalla será nuestro eje de traslación espacial
CENTRO_X = ANCHO_VENTANA // 2
CENTRO_Y = ALTO_VENTANA // 2


# --- 3. FUNCIÓN DE PROCESAMIENTO GEOMÉTRICO (MATRIZ DE ROTACIÓN) ---
def rotar_y_trasladar_vertices(vertices, grados, centro_x, centro_y):
    """
    Toma los vértices originales, los rota un ángulo alfa respecto al origen (0,0)
    y luego los desplaza al centro de coordenadas de la pantalla de Pygame.
    """
    radianes = math.radians(grados)
    nuevos_vertices = []
    
    for x, y in vertices:
        # 1. Aplicación de la fórmula de rotación analítica
        x_rotado = x * math.cos(radianes) - y * math.sin(radianes)
        y_rotado = x * math.sin(radianes) + y * math.cos(radianes)
        
        # 2. Traslación al plano de la pantalla (Transformación de coordenadas)
        x_final = x_rotado + centro_x
        y_final = y_rotado + centro_y
        
        nuevos_vertices.append((x_final, y_final))
        
    return nuevos_vertices


# --- 4. BUCLE PRINCIPAL DE LA APLICACIÓN ---
angulo_actual = 0.0
ejecutando = True

print("========================================================")
print("     CONTROL REMOTO DE ROTACIÓN EN PYGAME ACTIVADO      ")
print("========================================================")
print("Instrucciones:")
print(" - Introduce el ángulo de giro en esta terminal.")
print(" - Haz clic en la ventana de Pygame para ver el resultado.")
print(" - Presiona la tecla 'ESC' dentro de la ventana para Salir.")
print("========================================================")

while ejecutando:
    # --- Gestión de Eventos de Hardware ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        # Detectar la pulsación de teclas de escape
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                print("\n[INFO]: Tecla ESC presionada. Cerrando laboratorio.")
                ejecutando = False

    # --- Solicitar ángulo por Consola de forma síncrona ---
    try:
        entrada = input(f"\nÁngulo actual: {angulo_actual}° | Ingrese nuevo ángulo de rotación: ")
        angulo_actual = float(entrada)
    except ValueError:
        print("❌ Entrada inválida. Por favor, introduzca un número flotante o entero.")
        continue

    # --- Renderizado Gráfico ---
    # Limpiamos la pantalla pintando el fondo
    pantalla.fill(COLOR_FONDO)
    
    # Calculamos la posición de los nuevos puntos geométricos
    vertices_dibujo = rotar_y_trasladar_vertices(VERTICES_ORIGINALES, angulo_actual, CENTRO_X, CENTRO_Y)
    
    # Dibujamos el triángulo rotado en el lienzo
    pygame.draw.polygon(pantalla, COLOR_TRIANGULO, vertices_dibujo, width=4)
    
    # Dibujamos un pequeño círculo en el centro que representa el pivote de rotación
    pygame.draw.circle(pantalla, COLOR_CENTRO, (CENTRO_X, CENTRO_Y), 5)
    
    # Actualizamos el frame de la pantalla para mostrar los cambios
    pygame.display.flip()

# Cierre ordenado de los módulos de hardware
pygame.quit()
sys.exit()