import cv2
import pygame
import numpy as np

# ========== CONFIGURACIÓN ==========
ANCHO, ALTO = 800, 600
COLOR_PELOTA = (255, 100, 100)
RADIO_PELOTA = 25

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Controla la pelota con tu mano 🖐️")
reloj = pygame.time.Clock()

pos_x = float(ANCHO // 2)
pos_y = float(ALTO // 2)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Rangos de color de piel en HSV
PIEL_BAJO = np.array([0, 30, 60], dtype=np.uint8)
PIEL_ALTO = np.array([20, 150, 255], dtype=np.uint8)

print("🎮 Mueve tu mano frente a la cámara")
print("   - La pelota sigue tu mano")
print("   - Presiona ESC o Q para salir")

target_x = pos_x
target_y = pos_y
factor_suavizado = 0.4

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q:
                corriendo = False

    ret, frame = cap.read()
    if not ret:
        break

    # NO voltear la imagen
    frame_display = frame.copy()
    
    # Obtener dimensiones
    h_frame, w_frame = frame.shape[:2]
    
    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara_piel = cv2.inRange(hsv, PIEL_BAJO, PIEL_ALTO)
    mascara_piel = cv2.erode(mascara_piel, None, iterations=2)
    mascara_piel = cv2.dilate(mascara_piel, None, iterations=2)
    
    contornos, _ = cv2.findContours(mascara_piel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mano_detectada = False
    
    if contornos:
        contorno_mas_grande = max(contornos, key=cv2.contourArea)
        area = cv2.contourArea(contorno_mas_grande)
        
        if area > 3000:
            M = cv2.moments(contorno_mas_grande)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # CORRECCIÓN: Invertir X para que coincida con el movimiento
                cx_invertido = w_frame - cx
                
                target_x = float((cx_invertido / w_frame) * ANCHO)
                target_y = float((cy / h_frame) * ALTO)
                mano_detectada = True
                
                cv2.drawContours(frame_display, [contorno_mas_grande], -1, (0, 255, 0), 2)
                cv2.circle(frame_display, (cx, cy), 10, (0, 0, 255), -1)

    if mano_detectada:
        pos_x = pos_x + (target_x - pos_x) * factor_suavizado
        pos_y = pos_y + (target_y - pos_y) * factor_suavizado

    # Dibujar en Pygame
    pantalla.fill((30, 30, 40))
    
    pos_x_int = int(pos_x)
    pos_y_int = int(pos_y)
    
    pygame.draw.circle(pantalla, (50, 50, 60), (pos_x_int + 5, pos_y_int + 5), RADIO_PELOTA)
    pygame.draw.circle(pantalla, COLOR_PELOTA, (pos_x_int, pos_y_int), RADIO_PELOTA)
    pygame.draw.circle(pantalla, (255, 200, 200), (pos_x_int - 8, pos_y_int - 8), 8)

    fuente = pygame.font.Font(None, 36)
    status = "🖐️ Mano detectada" if mano_detectada else "❌ Mueve tu mano"
    pantalla.blit(fuente.render(status, True, (255, 255, 255)), (20, 20))
    
    # Mostrar cámara
    frame_pequeno = cv2.resize(frame_display, (320, 240))
    frame_rgb = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
    pantalla.blit(frame_surface, (ANCHO - 340, ALTO - 260))

    pygame.display.flip()
    reloj.tick(30)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
print("👋 Demostración finalizada")