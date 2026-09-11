import cv2
import pygame
import numpy as np

# ========== CONFIGURACIÓN ==========
ANCHO, ALTO = 800, 600
COLOR_PELOTA = (255, 255, 255)  # Blanco para que se vea bien con cualquier fondo
RADIO_BASE = 25  # Tamaño base de la pelota

# ========== INICIALIZAR PYGAME ==========
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Controla la pelota con colores 🎨")
reloj = pygame.time.Clock()

pos_x = float(ANCHO // 2)
pos_y = float(ALTO // 2)
radio_actual = RADIO_BASE

# ========== INICIALIZAR CÁMARA ==========
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ========== RANGOS DE COLOR EN HSV ==========
# ROJO (tiene dos rangos porque el rojo está en ambos extremos del espectro HSV)
ROJO_BAJO1 = np.array([0, 100, 100])
ROJO_ALTO1 = np.array([10, 255, 255])
ROJO_BAJO2 = np.array([160, 100, 100])
ROJO_ALTO2 = np.array([179, 255, 255])

# AZUL
AZUL_BAJO = np.array([100, 100, 100])
AZUL_ALTO = np.array([130, 255, 255])

# AMARILLO
AMARILLO_BAJO = np.array([20, 100, 100])
AMARILLO_ALTO = np.array([35, 255, 255])

# VERDE (opcional, por si quieres agregar más colores)
VERDE_BAJO = np.array([40, 100, 100])
VERDE_ALTO = np.array([80, 255, 255])

print("🎨 Detectando objetos por color")
print("   🔴 ROJO → La pelota crece 50%")
print("   🔵 AZUL → La pelota se reduce 50%")
print("   🟡 AMARILLO → Tamaño normal")
print("   - Mueve el objeto para controlar la pelota")
print("   - Presiona ESC o Q para salir")
print("   - Presiona R para reiniciar posición")

# Variables para suavizar
target_x = pos_x
target_y = pos_y
factor_suavizado = 0.3
objeto_detectado = False

# Variable para el color detectado
color_detectado = "NINGUNO"
tamano_objeto = 0

# ========== FUNCIÓN PARA DETECTAR COLOR ==========
def detectar_color(mascara, nombre_color):
    """Detecta si hay un objeto del color especificado"""
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contornos:
        # Buscar el contorno más grande
        contorno_mas_grande = max(contornos, key=cv2.contourArea)
        area = cv2.contourArea(contorno_mas_grande)
        
        # Solo considerar si el área es suficientemente grande
        if area > 2000:  # Ajusta según el tamaño de tu objeto
            M = cv2.moments(contorno_mas_grande)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return True, cx, cy, area, contorno_mas_grande
    
    return False, 0, 0, 0, None

corriendo = True
while corriendo:
    # ---------- EVENTOS ----------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q:
                corriendo = False
            elif evento.key == pygame.K_r:
                # Reiniciar posición
                pos_x = float(ANCHO // 2)
                pos_y = float(ALTO // 2)
                target_x = pos_x
                target_y = pos_y
                print("🔄 Posición reiniciada")

    # ---------- CÁMARA ----------
    ret, frame = cap.read()
    if not ret:
        break

    # NO voltear la imagen para mantener coordenadas correctas
    frame_display = frame.copy()
    h_frame, w_frame = frame.shape[:2]
    
    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # ---------- DETECTAR COLORES ----------
    # Máscaras para cada color
    mascara_rojo1 = cv2.inRange(hsv, ROJO_BAJO1, ROJO_ALTO1)
    mascara_rojo2 = cv2.inRange(hsv, ROJO_BAJO2, ROJO_ALTO2)
    mascara_rojo = cv2.bitwise_or(mascara_rojo1, mascara_rojo2)
    
    mascara_azul = cv2.inRange(hsv, AZUL_BAJO, AZUL_ALTO)
    mascara_amarillo = cv2.inRange(hsv, AMARILLO_BAJO, AMARILLO_ALTO)
    
    # Limpiar máscaras
    mascara_rojo = cv2.erode(mascara_rojo, None, iterations=2)
    mascara_rojo = cv2.dilate(mascara_rojo, None, iterations=2)
    
    mascara_azul = cv2.erode(mascara_azul, None, iterations=2)
    mascara_azul = cv2.dilate(mascara_azul, None, iterations=2)
    
    mascara_amarillo = cv2.erode(mascara_amarillo, None, iterations=2)
    mascara_amarillo = cv2.dilate(mascara_amarillo, None, iterations=2)
    
    # ---------- DETECTAR OBJETOS ----------
    objeto_detectado = False
    color_detectado = "NINGUNO"
    cx, cy = 0, 0
    contorno_encontrado = None
    
    # 1. Detectar ROJO (prioridad más alta)
    detectado, cx, cy, area, contorno = detectar_color(mascara_rojo, "ROJO")
    if detectado:
        objeto_detectado = True
        color_detectado = "ROJO"
        contorno_encontrado = contorno
        # La pelota crece 50%
        radio_actual = RADIO_BASE * 1.5
        tamano_objeto = area
        
        # Dibujar en la cámara
        cv2.drawContours(frame_display, [contorno], -1, (0, 0, 255), 3)
        cv2.circle(frame_display, (cx, cy), 10, (0, 0, 255), -1)
        cv2.putText(frame_display, "ROJO - CRECE", (cx - 30, cy - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # 2. Detectar AZUL
    if not objeto_detectado:
        detectado, cx, cy, area, contorno = detectar_color(mascara_azul, "AZUL")
        if detectado:
            objeto_detectado = True
            color_detectado = "AZUL"
            contorno_encontrado = contorno
            # La pelota se reduce 50%
            radio_actual = RADIO_BASE * 0.5
            tamano_objeto = area
            
            cv2.drawContours(frame_display, [contorno], -1, (255, 0, 0), 3)
            cv2.circle(frame_display, (cx, cy), 10, (255, 0, 0), -1)
            cv2.putText(frame_display, "AZUL - REDUCE", (cx - 30, cy - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    
    # 3. Detectar AMARILLO
    if not objeto_detectado:
        detectado, cx, cy, area, contorno = detectar_color(mascara_amarillo, "AMARILLO")
        if detectado:
            objeto_detectado = True
            color_detectado = "AMARILLO"
            contorno_encontrado = contorno
            # Tamaño normal
            radio_actual = RADIO_BASE
            tamano_objeto = area
            
            cv2.drawContours(frame_display, [contorno], -1, (0, 255, 255), 3)
            cv2.circle(frame_display, (cx, cy), 10, (0, 255, 255), -1)
            cv2.putText(frame_display, "AMARILLO - NORMAL", (cx - 30, cy - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    # ---------- ACTUALIZAR POSICIÓN ----------
    if objeto_detectado:
        # Invertir coordenada X para que coincida con el movimiento
        cx_invertido = w_frame - cx
        target_x = float((cx_invertido / w_frame) * ANCHO)
        target_y = float((cy / h_frame) * ALTO)
        
        # Movimiento suavizado
        pos_x = pos_x + (target_x - pos_x) * factor_suavizado
        pos_y = pos_y + (target_y - pos_y) * factor_suavizado

    # ---------- DIBUJAR EN PYGAME ----------
    pantalla.fill((30, 30, 40))
    
    pos_x_int = int(pos_x)
    pos_y_int = int(pos_y)
    radio_int = int(radio_actual)
    
    # Determinar color de la pelota según el color detectado
    if color_detectado == "ROJO":
        color_pelota = (255, 50, 50)  # Rojo
    elif color_detectado == "AZUL":
        color_pelota = (50, 50, 255)  # Azul
    elif color_detectado == "AMARILLO":
        color_pelota = (255, 255, 50)  # Amarillo
    else:
        color_pelota = (200, 200, 200)  # Gris (sin objeto)
    
    # Sombra de la pelota
    pygame.draw.circle(pantalla, (50, 50, 60), (pos_x_int + 5, pos_y_int + 5), radio_int)
    
    # Cuerpo de la pelota
    pygame.draw.circle(pantalla, color_pelota, (pos_x_int, pos_y_int), radio_int)
    
    # Brillo de la pelota
    brillo_size = max(5, radio_int // 3)
    pygame.draw.circle(pantalla, (255, 255, 255), 
                      (pos_x_int - radio_int//3, pos_y_int - radio_int//3), 
                      brillo_size)
    
    # ---------- MOSTRAR INFORMACIÓN ----------
    fuente_grande = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 24)
    
    # Estado de detección
    if objeto_detectado:
        status = f"🎯 Objeto detectado: {color_detectado}"
        status_color = (0, 255, 0)
    else:
        status = "❌ No se detecta objeto"
        status_color = (255, 255, 0)
    
    status_surface = fuente_grande.render(status, True, status_color)
    pantalla.blit(status_surface, (20, 20))
    
    # Información del tamaño
    info_y = 60
    if objeto_detectado:
        tamaño_text = f"Tamaño: {radio_actual:.1f}px ({int((radio_actual/RADIO_BASE)*100)}%)"
        pantalla.blit(fuente_pequena.render(tamaño_text, True, (200, 200, 200)), (20, info_y))
        info_y += 30
        
        area_text = f"Área objeto: {tamano_objeto}px"
        pantalla.blit(fuente_pequena.render(area_text, True, (200, 200, 200)), (20, info_y))
        info_y += 30
    
    # Leyenda de colores
    leyenda_y = ALTO - 100
    colores_texto = [
        ("🟡 AMARILLO → Normal", (255, 255, 0)),
        ("🔴 ROJO → +50%", (255, 0, 0)),
        ("🔵 AZUL → -50%", (0, 0, 255))
    ]
    
    for texto, color in colores_texto:
        text_surface = fuente_pequena.render(texto, True, color)
        pantalla.blit(text_surface, (20, leyenda_y))
        leyenda_y += 25
    
    # Controles
    controles = fuente_pequena.render("ESC/Q: Salir | R: Reiniciar", True, (150, 150, 150))
    pantalla.blit(controles, (ANCHO - 250, ALTO - 30))
    
    # ---------- MOSTRAR CÁMARA EN PYGAME ----------
    # Mostrar también las máscaras para debug
    frame_pequeno = cv2.resize(frame_display, (320, 240))
    frame_rgb = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
    pantalla.blit(frame_surface, (ANCHO - 340, ALTO - 260))
    
    # Mostrar máscara pequeña para debug (opcional)
    # Combinar máscaras para mostrar
    mascara_combinada = cv2.bitwise_or(mascara_rojo, mascara_azul)
    mascara_combinada = cv2.bitwise_or(mascara_combinada, mascara_amarillo)
    mascara_pequena = cv2.resize(mascara_combinada, (160, 120))
    mascara_pequena = cv2.cvtColor(mascara_pequena, cv2.COLOR_GRAY2RGB)
    mascara_surface = pygame.surfarray.make_surface(np.rot90(mascara_pequena))
    pantalla.blit(mascara_surface, (ANCHO - 340, 20))

    pygame.display.flip()
    reloj.tick(30)

# ========== LIMPIAR ==========
cap.release()
cv2.destroyAllWindows()
pygame.quit()
print("👋 Demostración finalizada")