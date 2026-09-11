import cv2
import pygame
import numpy as np

# ========== CONFIGURACIÓN ==========
ANCHO, ALTO = 800, 600
COLOR_PELOTA = (255, 100, 100)
RADIO_PELOTA = 25

# ========== INICIALIZAR PYGAME ==========
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Controla la pelota con tu mano 🖐️")
reloj = pygame.time.Clock()

# Posición inicial - Asegurar que sean números enteros
pos_x = float(ANCHO // 2)
pos_y = float(ALTO // 2)

# ========== INICIALIZAR CÁMARA ==========
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ========== VARIABLES PARA DETECCIÓN DE PIEL ==========
# Rangos de color de piel en HSV
PIEL_BAJO = np.array([0, 30, 60], dtype=np.uint8)
PIEL_ALTO = np.array([20, 150, 255], dtype=np.uint8)

print("🎮 Mueve tu mano frente a la cámara")
print("   - La pelota sigue tu mano")
print("   - Presiona ESC o Q para salir")

# Variables para suavizar
target_x = float(pos_x)
target_y = float(pos_y)
factor_suavizado = 0.4

corriendo = True
while corriendo:
    # ---------- EVENTOS ----------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q:
                corriendo = False

    # ---------- CÁMARA ----------
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: No se puede acceder a la cámara")
        break

    frame = cv2.flip(frame, 1)
    frame_display = frame.copy()
    
    # Convertir a HSV para detección de color de piel
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Crear máscara para piel
    mascara_piel = cv2.inRange(hsv, PIEL_BAJO, PIEL_ALTO)
    
    # Limpiar la máscara
    mascara_piel = cv2.erode(mascara_piel, None, iterations=2)
    mascara_piel = cv2.dilate(mascara_piel, None, iterations=2)
    
    # Encontrar contornos
    contornos, _ = cv2.findContours(mascara_piel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mano_detectada = False
    
    if contornos:
        # Buscar el contorno más grande (la mano)
        contorno_mas_grande = max(contornos, key=cv2.contourArea)
        area = cv2.contourArea(contorno_mas_grande)
        
        # Solo considerar si el área es suficientemente grande
        if area > 3000:
            # Obtener el centro del contorno
            M = cv2.moments(contorno_mas_grande)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Convertir a coordenadas de Pygame - Asegurar que sean floats
                target_x = float((cx / 640) * ANCHO)
                target_y = float((cy / 480) * ALTO)
                mano_detectada = True
                
                # Dibujar en el frame de la cámara
                cv2.drawContours(frame_display, [contorno_mas_grande], -1, (0, 255, 0), 2)
                cv2.circle(frame_display, (cx, cy), 10, (0, 0, 255), -1)

    # ---------- ACTUALIZAR POSICIÓN ----------
    if mano_detectada:
        pos_x = pos_x + (target_x - pos_x) * factor_suavizado
        pos_y = pos_y + (target_y - pos_y) * factor_suavizado
        
        # Asegurar que los valores sean floats
        pos_x = float(pos_x)
        pos_y = float(pos_y)

    # ---------- DIBUJAR EN PYGAME ----------
    pantalla.fill((30, 30, 40))
    
    # Convertir a int para dibujar - Asegurar que son números únicos
    pos_x_int = int(pos_x)
    pos_y_int = int(pos_y)
    
    # Pelota con efecto
    # Sombra
    pygame.draw.circle(pantalla, (50, 50, 60), (pos_x_int + 5, pos_y_int + 5), RADIO_PELOTA)
    # Cuerpo
    pygame.draw.circle(pantalla, COLOR_PELOTA, (pos_x_int, pos_y_int), RADIO_PELOTA)
    # Brillo
    pygame.draw.circle(pantalla, (255, 200, 200), (pos_x_int - 8, pos_y_int - 8), 8)

    # Información
    fuente_grande = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 24)
    
    if mano_detectada:
        status = "🖐️ Mano detectada"
        status_color = (0, 255, 0)
    else:
        status = "❌ Mueve tu mano frente a la cámara"
        status_color = (255, 255, 0)
    
    status_surface = fuente_grande.render(status, True, status_color)
    pantalla.blit(status_surface, (20, 20))
    
    # Mostrar coordenadas
    coords_text = f"Pos: ({pos_x_int}, {pos_y_int})"
    pantalla.blit(fuente_pequena.render(coords_text, True, (200, 200, 200)), (20, 60))
    
    # Controles
    controles = fuente_pequena.render("ESC/Q: Salir", True, (150, 150, 150))
    pantalla.blit(controles, (ANCHO - 150, ALTO - 40))
    
    # ---------- MOSTRAR CÁMARA EN PYGAME ----------
    frame_pequeno = cv2.resize(frame_display, (320, 240))
    frame_rgb = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
    pantalla.blit(frame_surface, (ANCHO - 340, ALTO - 260))

    pygame.display.flip()
    reloj.tick(30)

# ========== LIMPIAR ==========
cap.release()
cv2.destroyAllWindows()
pygame.quit()
print("👋 Demostración finalizada")