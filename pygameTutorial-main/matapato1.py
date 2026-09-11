import pygame
import sys
import math
import numpy as np

# --- INICIALIZACIÓN ---
pygame.init()
pygame.mixer.init()

# --- CONFIGURACIÓN DE LA VENTANA ---
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laboratorio: Mata Patos con Física de Pong")
reloj = pygame.time.Clock()

# Ocultamos el cursor del sistema para usar nuestra propia mira interactiva
pygame.mouse.set_visible(False)

# --- COLORES ---
COLOR_CIELO = (58, 125, 68)     # Verde pasto/cacería retro
COLOR_BLANCO = (255, 255, 255)
COLOR_MIRA = (230, 57, 70)       # Rojo brillante para la mira
COLOR_TEXTO = (241, 250, 238)
COLOR_PANEL = (20, 20, 20)

# --- FUENTES ---
fuente_hud = pygame.font.SysFont("monospace", 24, bold=True)
fuente_assets = pygame.font.SysFont("segoe ui emoji", 50)

# --- GENERADOR DE AUDIO SINTÉTICO (RAM) ---
def generar_sonido_sintetico(frecuencia_base, duracion_ms, tipo="beep"):
    frecuencia_muestreo = 44100
    num_muestras = int(frecuencia_muestreo * (duracion_ms / 1000.0))
    t = np.linspace(0, duracion_ms / 1000.0, num_muestras, False)
    
    if tipo == "disparo":
        # Ruido blanco decreciente + caída de frecuencia extrema (Explosión)
        ruido = np.random.uniform(-1, 1, num_muestras)
        rampa = np.exp(-12 * t)
        onda = ruido * rampa
    elif tipo == "cuac":
        # Onda cuadrada con modulación rápida (Simula un graznido/aleteo)
        onda = np.sign(np.sin(2 * np.pi * frecuencia_base * t) * np.sin(2 * np.pi * 5 * t))
    else:
        # Rebote estándar
        onda = np.sin(2 * np.pi * frecuencia_base * t)

    atenuacion = np.linspace(1.0, 0.0, num_muestras)
    datos_audio = (onda * atenuacion * 16383).astype(np.int16)
    datos_estereo = np.vstack((datos_audio, datos_audio)).T.copy(order='C')
    
    return pygame.mixer.Sound(buffer=datos_estereo)

# Caché de efectos de sonido
sonido_disparo = generar_sonido_sintetico(100, 250, "disparo")
sonido_cuac = generar_sonido_sintetico(300, 150, "cuac")
sonido_caida = generar_sonido_sintetico(150, 400, "beep")

# --- CLASE: PATO (Basado en la física de la bola de Pong) ---
class Pato:
    def __init__(self):
        self.superficie = fuente_assets.render("🦆", True, COLOR_BLANCO)
        self.rect = self.superficie.get_rect()
        self.velocidad_base = 6
        self.reiniciar()

    def reiniciar(self):
        # El pato reaparece abajo en el centro (como si saliera de los arbustos)
        self.rect.centerx = ANCHO // 2
        self.rect.centery = ALTO - 100
        
        # Trayectoria angular hacia arriba (Ángulo entre 30 y 150 grados)
        angulo = math.radians(np.random.uniform(30, 150))
        
        # Componentes vectoriales (Física de Pong, Y va negativo hacia arriba)
        self.vx = self.velocidad_base * math.cos(angulo)
        self.vy = -self.velocidad_base * math.sin(angulo)

    def actualizar(self):
        # Movimiento rectilíneo continuo
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # --- REBOTES ESTILO PONG (Paredes laterales y techo) ---
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx *= -1
            sonido_cuac.play()
        elif self.rect.right >= ANCHO:
            self.rect.right = ANCHO
            self.vx *= -1
            sonido_cuac.play()

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy *= -1
            sonido_cuac.play()
        elif self.rect.bottom >= ALTO - 60: # Rebota antes de tocar el panel inferior
            self.rect.bottom = ALTO - 60
            self.vy *= -1
            sonido_cuac.play()

    def dibujar(self, superficie):
        # Voltear el asset horizontalmente según la dirección vector X
        if self.vx > 0:
            superficie_volteada = pygame.transform.flip(self.superficie, True, False)
        else:
            superficie_volteada = self.superficie
        superficie.blit(superficie_volteada, self.rect)


# --- CLASE: MIRA TELESCÓPICA ---
class Mira:
    def __init__(self):
        self.radio = 20

    def dibujar(self, superficie, pos_mouse):
        mx, my = pos_mouse
        # Dibujar círculos concéntricos de la mira
        pygame.draw.circle(superficie, COLOR_MIRA, (mx, my), self.radio, 2)
        pygame.draw.circle(superficie, COLOR_MIRA, (mx, my), 4, 0)
        # Líneas de cruz de precisión
        pygame.draw.line(superficie, COLOR_MIRA, (mx - self.radio - 5, my), (mx + self.radio + 5, my), 2)
        pygame.draw.line(superficie, COLOR_MIRA, (mx, my - self.radio - 5), (mx, my + self.radio + 5), 2)


# --- INSTANCIACIÓN Y VARIABLES ---
pato_objetivo = Pato()
mira_jugador = Mira()

puntos = 0
disparos_totales = 0

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    
    posicion_mouse = pygame.mouse.get_pos()
    
    # 1. CONTROL DE EVENTOS (Input de Disparo)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clic izquierdo detectado
                sonido_disparo.play()
                disparos_totales += 1
                
                # Verificamos colisión del punto del mouse con la bounding box del pato
                if pato_objetivo.rect.collidepoint(posicion_mouse):
                    sonido_caida.play()
                    puntos += 1
                    # Aumentamos la velocidad de forma incremental para el siguiente pato
                    pato_objetivo.velocidad_base += 0.5
                    pato_objetivo.reiniciar()
                    
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

    # 2. ACTUALIZACIÓN DE LÓGICA (Física de la Bola/Pato)
    pato_objetivo.actualizar()

    # 3. RENDERIZADO GRÁFICO
    pantalla.fill(COLOR_CIELO)
    
    # Dibujamos al pato
    pato_objetivo.dibujar(pantalla)
    
    # Dibujamos la mira interactiva encima del pato (sistema de capas)
    mira_jugador.dibujar(pantalla, posicion_mouse)
    
    # --- RENDERIZADO DEL HUD (Panel Inferior) ---
    pygame.draw.rect(pantalla, COLOR_PANEL, (0, ALTO - 60, ANCHO, 60))
    
    # Cálculos de precisión del laboratorio
    precision = (puntos / disparos_totales * 100) if disparos_totales > 0 else 0.0
    
    txt_hud = f"PATOS DERRIBADOS: {puntos}  |  DISPAROS: {disparos_totales}  |  PRECISIÓN: {precision:.1f}%"
    surface_hud = fuente_hud.render(txt_hud, True, COLOR_TEXTO)
    pantalla.blit(surface_hud, (20, ALTO - 42))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()