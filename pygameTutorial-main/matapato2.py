import pygame
import sys
import math
import numpy as np
import os

# --- INICIALIZACIÓN ---
pygame.init()
pygame.mixer.init()

# --- CONFIGURACIÓN DE LA VENTANA ---
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laboratorio: Juego de Desestrés con Física de Pong")
reloj = pygame.time.Clock()

# Ocultamos el cursor estándar para centrar la atención en la mira custom
pygame.mouse.set_visible(False)

# --- COLORES ---
COLOR_FONDO = (40, 44, 52)      # Gris oscuro relajante / estilo editor
COLOR_MIRA = (255, 75, 75)       # Rojo brillante para la mira
COLOR_TEXTO = (241, 250, 238)
COLOR_PANEL = (20, 20, 20)
COLOR_BLANCO= (255,255,255)

# --- FUENTES ---
fuente_hud = pygame.font.SysFont("monospace", 24, bold=True)

# --- NOMBRE DEL ARCHIVO DE IMAGEN ---
# Recomienda a tus alumnos colocar la foto en la misma carpeta con este nombre:
NOMBRE_IMAGEN = "assets\objetivo.png"

# --- GENERADOR DE AUDIO SINTÉTICO (RAM) ---
def generar_sonido_sintetico(frecuencia_base, duracion_ms, tipo="beep"):
    frecuencia_muestreo = 44100
    num_muestras = int(frecuencia_muestreo * (duracion_ms / 1000.0))
    t = np.linspace(0, duracion_ms / 1000.0, num_muestras, False)
    
    if tipo == "disparo":
        # Ruido blanco explosivo decreciente (Efecto de impacto fuerte)
        ruido = np.random.uniform(-1, 1, num_muestras)
        rampa = np.exp(-15 * t)
        onda = ruido * rampa
    elif tipo == "exito":
        # Acorde ascendente rápido de dos tonos (Estímulo positivo)
        onda = np.sin(2 * np.pi * frecuencia_base * t) + np.sin(2 * np.pi * (frecuencia_base * 1.25) * t)
    else:
        # Sonido seco para rebotes en paredes
        onda = np.sin(2 * np.pi * frecuencia_base * np.exp(-10 * t))

    atenuacion = np.linspace(1.0, 0.0, num_muestras)
    datos_audio = (onda * atenuacion * 12000).astype(np.int16)
    datos_estereo = np.vstack((datos_audio, datos_audio)).T.copy(order='C')
    
    return pygame.mixer.Sound(buffer=datos_estereo)

# Inicializar los sonidos en la memoria
sonido_disparo = generar_sonido_sintetico(80, 200, "disparo")
sonido_exito = generar_sonido_sintetico(523, 180, "exito") # Nota Do5
sonido_rebote = generar_sonido_sintetico(180, 80, "rebote")

# --- CLASE: OBJETIVO MOVIL (Física Vectorial de Pong) ---
class ObjetivoMovil:
    def __init__(self):
        # Dimensión recomendada para la foto en el laboratorio
        self.ancho_target = 80
        self.alto_target = 80
        
        # Intentar cargar la imagen real; si no existe, creamos un sustituto visual temporal
        if os.path.exists(NOMBRE_IMAGEN):
            imagen_original = pygame.image.load(NOMBRE_IMAGEN).convert_alpha()
            # Ajuste geométrico: escalamos la foto al tamaño exacto de píxeles ideal
            self.superficie = pygame.transform.scale(imagen_original, (self.ancho_target, self.alto_target))
        else:
            # Fallback didáctico por si el alumno no ha puesto la foto aún
            self.superficie = pygame.Surface((self.ancho_target, self.alto_target))
            self.superficie.fill((255, 165, 0)) # Cuadro naranja de advertencia
            pygame.draw.rect(self.superficie, COLOR_BLANCO, (0, 0, self.ancho_target, self.alto_target), 3)
            
        self.rect = self.superficie.get_rect()
        self.velocidad_base = 6
        self.reiniciar()

    def reiniciar(self):
        # Aparece en una ubicación aleatoria de la mitad superior
        self.rect.x = np.random.randint(100, ANCHO - 100)
        self.rect.y = np.random.randint(100, ALTO // 2)
        
        # Descomposición angular aleatoria para que su rumbo cambie en cada ciclo
        angulo = math.radians(np.random.uniform(20, 70))
        self.vx = self.velocidad_base * math.cos(angulo) * np.random.choice([-1, 1])
        self.vy = self.velocidad_base * math.sin(angulo) * np.random.choice([-1, 1])

    def actualizar(self):
        # Traslación rectilínea continua
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # --- REBOTES ELASTICOS ESTILO PONG ---
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx *= -1
            sonido_rebote.play()
        elif self.rect.right >= ANCHO:
            self.rect.right = ANCHO
            self.vx *= -1
            sonido_rebote.play()

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy *= -1
            sonido_rebote.play()
        elif self.rect.bottom >= ALTO - 60: # Evitar tocar el marco inferior del menú
            self.rect.bottom = ALTO - 60
            self.vy *= -1
            sonido_rebote.play()

    def dibujar(self, superficie):
        superficie.blit(self.superficie, self.rect)


# --- CLASE: MIRA RETÍCULA ---
class MiraTelescopica:
    def __init__(self):
        self.radio = 24

    def dibujar(self, superficie, pos_mouse):
        mx, my = pos_mouse
        # Geometría de la mira: Círculos concéntricos y retícula de cruz
        pygame.draw.circle(superficie, COLOR_MIRA, (mx, my), self.radio, 2)
        pygame.draw.circle(superficie, COLOR_MIRA, (mx, my), 3, 0)
        pygame.draw.line(superficie, COLOR_MIRA, (mx - self.radio - 4, my), (mx + self.radio + 4, my), 2)
        pygame.draw.line(superficie, COLOR_MIRA, (mx, my - self.radio - 4), (mx, my + self.radio + 4), 2)


# --- VARIABLES DE CONTROL ---
objetivo = ObjetivoMovil()
mira = MiraTelescopica()

impactos = 0
intentos = 0

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    
    pos_mouse = pygame.mouse.get_pos()
    
    # 1. ENTRADA DE EVENTOS (Input por Polling/Event)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clic izquierdo (Fuego)
                sonido_disparo.play()
                intentos += 1
                
                # Intersección geométrica del punto del clic con la caja delimitadora de la foto
                if objetivo.rect.collidepoint(pos_mouse):
                    sonido_exito.play()
                    impactos += 1
                    # Aumentamos muy sutilmente la velocidad para retar el estrés del jugador
                    objetivo.velocidad_base += 0.4
                    objetivo.reiniciar()
                    
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

    # 2. ACTUALIZACIÓN MATEMÁTICA
    objetivo.actualizar()

    # 3. RENDERIZADO EN PANTALLA
    pantalla.fill(COLOR_FONDO)
    
    # Renderizar el objetivo móvil (la fotografía escalada)
    objetivo.dibujar(pantalla)
    
    # Renderizar la mira encima (sistema de profundidad Z-order)
    mira.dibujar(pantalla, pos_mouse)
    
    # --- RENDERIZADO DEL HUD INFERIOR ---
    pygame.draw.rect(pantalla, COLOR_PANEL, (0, ALTO - 60, ANCHO, 60))
    
    txt_hud = f"IMPACTOS EXITOSOS: {impactos}  |  TOTAL DISPAROS: {intentos}"
    surface_hud = fuente_hud.render(txt_hud, True, COLOR_TEXTO)
    pantalla.blit(surface_hud, (20, ALTO - 42))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()