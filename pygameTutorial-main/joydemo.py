import pygame
import serial
import serial.tools.list_ports
import threading
import time
import queue

# ============ CONFIGURACIÓN ============
PUERTO = "COM6"       # Cambia por tu puerto COM entrante Bluetooth
BAUDIOS = 9600
ANCHO = 800
ALTO = 600
FPS = 60
VELOCIDAD = 5         # Píxeles por frame al moverse
VELOCIDAD_RETORNO = 3 # Píxeles por frame al volver al centro

# ============ HILO DE LECTURA SERIE ============
class LectorSerie(threading.Thread):
    def __init__(self, puerto, baudios):
        super().__init__(daemon=True)
        self.puerto = serial.Serial(port=puerto, baudrate=baudios, timeout=0.1)
        self.cola_comandos = queue.Queue()
        self.ejecutando = True
        self.ultimo_comando = "S"  # S = STOP (comando por defecto)
        
    def run(self):
        buffer = ""
        while self.ejecutando:
            try:
                if self.puerto.in_waiting > 0:
                    byte = self.puerto.read(1).decode('utf-8', errors='ignore')
                    if byte == '\n':  # Delimitador de mensaje
                        comando = buffer.strip().upper()
                        if comando:
                            self.ultimo_comando = comando
                            print(f"Comando recibido: {comando}")
                        buffer = ""
                    else:
                        buffer += byte
                time.sleep(0.001)
            except Exception as e:
                print(f"Error lectura: {e}")
                break
                
    def detener(self):
        self.ejecutando = False
        if self.puerto.is_open:
            self.puerto.close()

# ============ JUEGO PRINCIPAL ============
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Control por Bluetooth - Pygame")
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 36)
    
    # Posición inicial del cuadrado (centro)
    centro_x, centro_y = ANCHO // 2, ALTO // 2
    cuadrado_x, cuadrado_y = centro_x, centro_y
    tam_cuadrado = 50
    
    # Iniciar lector serie
    try:
        lector = LectorSerie(PUERTO, BAUDIOS)
        lector.start()
        print(f"✓ Conectado a {PUERTO}")
    except Exception as e:
        print(f"✗ Error al abrir puerto: {e}")
        return
    
    ejecutando = True
    comando_actual = "S"
    
    while ejecutando:
        # Eventos de Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
        
        # Leer último comando del puerto serie
        comando_actual = lector.ultimo_comando
        
        # Mover cuadrado según comando
        if comando_actual == "U" or comando_actual == "UP":
            cuadrado_y -= VELOCIDAD
        elif comando_actual == "D" or comando_actual == "DOWN":
            cuadrado_y += VELOCIDAD
        elif comando_actual == "L" or comando_actual == "LEFT":
            cuadrado_x -= VELOCIDAD
        elif comando_actual == "R" or comando_actual == "RIGHT":
            cuadrado_x += VELOCIDAD
        else:
            # Regresar al centro suavemente
            if cuadrado_x < centro_x:
                cuadrado_x += VELOCIDAD_RETORNO
            elif cuadrado_x > centro_x:
                cuadrado_x -= VELOCIDAD_RETORNO
                
            if cuadrado_y < centro_y:
                cuadrado_y += VELOCIDAD_RETORNO
            elif cuadrado_y > centro_y:
                cuadrado_y -= VELOCIDAD_RETORNO
        
        # Limitar posición a la pantalla
        cuadrado_x = max(0, min(ANCHO - tam_cuadrado, cuadrado_x))
        cuadrado_y = max(0, min(ALTO - tam_cuadrado, cuadrado_y))
        
        # Dibujar
        pantalla.fill((30, 30, 30))  # Fondo oscuro
        
        # Dibujar marca del centro
        pygame.draw.circle(pantalla, (100, 100, 100), (centro_x, centro_y), 5)
        
        # Dibujar cuadrado (cambia de color según dirección)
        colores = {
            "U": (0, 200, 255),    # Azul - arriba
            "UP": (0, 200, 255),
            "D": (255, 100, 0),    # Naranja - abajo
            "DOWN": (255, 100, 0),
            "L": (0, 255, 100),    # Verde - izquierda
            "LEFT": (0, 255, 100),
            "R": (255, 255, 0),    # Amarillo - derecha
            "RIGHT": (255, 255, 0),
            "S": (200, 200, 200),  # Gris - quieto
            "STOP": (200, 200, 200)
        }
        color = colores.get(comando_actual, (200, 200, 200))
        pygame.draw.rect(pantalla, color, (cuadrado_x, cuadrado_y, tam_cuadrado, tam_cuadrado))
        
        # Mostrar comando actual
        texto = fuente.render(f"Comando: {comando_actual}", True, (255, 255, 255))
        pantalla.blit(texto, (10, 10))
        
        pygame.display.flip()
        reloj.tick(FPS)
    
    # Limpiar
    lector.detener()
    pygame.quit()

if __name__ == "__main__":
    main()