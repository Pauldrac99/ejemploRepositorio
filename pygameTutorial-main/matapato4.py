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
pygame.display.set_caption("Laboratorio: Animación por Sprite (Aleteo) y Fondo")
reloj = pygame.time.Clock()

pygame.mouse.set_visible(False)

# --- COLORES ---
COLOR_MIRA = (255, 75, 75)       
COLOR_TEXTO = (241, 250, 238)
COLOR_PANEL = (20, 20, 20)
COLOR_FALLBACK = (58, 125, 68)   # Verde pasto retro
fuente_hud = pygame.font.SysFont("monospace", 24, bold=True)
# --- CONFIGURACIÓN DE IMAGEN DE FONDO ---
NOMBRE_FONDO = "assets/fondo.png"
if os.path.exists(NOMBRE_FONDO):
    imagen_fondo_original = pygame.image.load(NOMBRE_FONDO).convert()
    superficie_fondo = pygame.transform.scale(imagen_fondo_original, (ANCHO, ALTO))
    tiene_fondo = True
else:
    tiene_fondo = False

# --- PROCEDIMIENTO PARA CREAR EL SPRITE DE PATO EN RAM (Estilo Pixel-Art) ---
def crear_sprite_pato(alas_arriba=True):
    """Genera una superficie de 64x64 píxeles dibujando un pato de forma programática."""
    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Colores del pato
    C_CUERPO = (139, 69, 19)   # Marrón
    C_CABEZA = (34, 139, 34)   # Verde ánade real
    C_PICO = (255, 165, 0)     # Naranja
    C_ALA = (101, 67, 33)      # Marrón oscuro
    C_OJO = (0, 0, 0)
    
    # 1. Dibujar el Cuerpo (Óvalo base)
    pygame.draw.ellipse(surf, C_CUERPO, (14, 24, 36, 24))
    
    # 2. Dibujar el Cuello y Cabeza
    pygame.draw.ellipse(surf, C_CABEZA, (38, 12, 16, 20)) # Cabeza
    pygame.draw.polygon(surf, C_CABEZA, [(34, 32), (44, 22), (48, 32)]) # Cuello
    pygame.draw.circle(surf, C_OJO, (48, 17), 2) # Ojo
    
    # 3. Dibujar el Pico
    pygame.draw.polygon(surf, C_PICO, [(52, 16), (62, 20), (52, 24)])
    
    # 4. Dibujar la Ala Dinámica (Efecto de Aleteo)
    if alas_arriba:
        # Ala apuntando hacia arriba y atrás
        pygame.draw.ellipse(surf, C_ALA, (18, 8, 14, 22))
    else:
        # Ala apuntando hacia abajo
        pygame.draw.ellipse(surf, C_ALA, (18, 28, 14, 22))
        
    return surf

# --- GENERADOR DE AUDIO SINTÉTICO ---
def generar_sonido_sintetico(frecuencia_base, duracion_ms, tipo="beep"):
    frecuencia_muestreo = 44100
    num_muestras = int(frecuencia_muestreo * (duracion_ms / 1000.0))
    t = np.linspace(0, duracion_ms / 1000.0, num_muestras, False)
    
    if tipo == "disparo":
        ruido = np.random.uniform(-1, 1, num_muestras)
        onda = ruido * np.exp(-15 * t)
    elif tipo == "exito":
        onda = np.sin(2 * np.pi * frecuencia_base * t) + np.sin(2 * np.pi * (frecuencia_base * 1.25) * t)
    else:
        # Sonido cíclico para el aleteo (frecuencia baja modulada)
        onda = np.sign(np.sin(2 * np.pi * frecuencia_base * t)) * 0.5
        
    atenuacion = np.linspace(1.0, 0.0, num_muestras)
    datos_audio = (onda * atenuacion * 12000).astype(np.int16)
    datos_estereo = np.vstack((datos_audio, datos_audio)).T.copy(order='C')
    
    return pygame.mixer.Sound(buffer=datos_estereo)

sonido_disparo = generar_sonido_sintetico(80, 200, "disparo")
sonido_exito = generar_sonido_sintetico(523, 180, "exito")
sonido_aleteo = generar_sonido_sintetico(120, 60, "aleteo")

# --- CLASE: PATO ANIMADO ---
class PatoAnimado:
    def __init__(self):
        # Cargamos los dos fotogramas de la animación creados por software
        self.frame_arriba = crear_sprite_pato(alas_arriba=True)
        self.frame_abajo = crear_sprite_pato(alas_arriba=False)
        
        # Guardamos los fotogramas en una lista (Matriz de animación)
        self.animacion = [self.frame_arriba, self.frame_abajo]
        self.indice_frame = 0
        
        # Temporizador interno para controlar la velocidad del aleteo
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.velocidad_aleteo = 150 # Milisegundos por cada cambio de ala
        
        self.rect = self.frame_arriba.get_rect()
        self.velocidad_base = 5
        self.reiniciar()

    def reiniciar(self):
        self.rect.x = np.random.randint(100, ANCHO - 100)
        self.rect.y = np.random.randint(100, ALTO // 2)
        angulo = math.radians(np.random.uniform(25, 65))
        self.vx = self.velocidad_base * math.cos(angulo) * np.random.choice([-1, 1])
        self.vy = self.velocidad_base * math.sin(angulo) * np.random.choice([-1, 1])

    def actualizar(self):
        # Movimiento espacial
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # --- MÁQUINA DE ESTADOS DE LA ANIMACIÓN (Frecuencia de Aleteo) ---
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_aleteo:
            # Intercambiar entre frame 0 y frame 1 usando aritmética modular
            self.indice_frame = (self.indice_frame + 1) % len(self.animacion)
            self.tiempo_ultimo_frame = tiempo_actual
            sonido_aleteo.play() # El sonido se sincroniza con el golpe de ala

        # --- REBOTES PONG ---
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx *= -1
        elif self.rect.right >= ANCHO:
            self.rect.right = ANCHO
            self.vx *= -1

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy *= -1
        elif self.rect.bottom >= ALTO - 60:
            self.rect.bottom = ALTO - 60
            self.vy *= -1

    def dibujar(self, superficie):
        # Seleccionar el fotograma actual
        sprite_actual = self.animacion[self.indice_frame]
        
        # Volteo geométrico: Si viaja a la izquierda (vx < 0), invertimos el sprite
        if self.vx < 0:
            sprite_actual = pygame.transform.flip(sprite_actual, True, False)
            
        superficie.blit(sprite_actual, self.rect)


# --- CLASE: MIRA ---
class MiraTelescopica:
    def __init__(self):
        self.radio = 24

    def dibujar(self, superficie, pos_mouse):
        mx, my = pos_mouse
        pygame.draw.circle(superficie, COLOR_MIRA, (mx, my), self.radio, 2)
        pygame.draw.circle(superficie, COLOR_MIRA, (mx, my), 3, 0)
        pygame.draw.line(superficie, COLOR_MIRA, (mx - self.radio - 4, my), (mx + self.radio + 4, my), 2)
        pygame.draw.line(superficie, COLOR_MIRA, (mx, my - self.radio - 4), (mx, my + self.radio + 4), 2)


# --- INSTANCIACIÓN ---
pato = PatoAnimado()
mira = MiraTelescopica()
impactos = 0
intentos = 0

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    
    pos_mouse = pygame.mouse.get_pos()
    
    # 1. CAPTURA DE INPUTS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                sonido_disparo.play()
                intentos += 1
                if pato.rect.collidepoint(pos_mouse):
                    sonido_exito.play()
                    impactos += 1
                    pato.velocidad_base += 0.5
                    # Aumentamos también la frecuencia del aleteo conforme se vuelve más rápido
                    pato.velocidad_aleteo = max(60, pato.velocidad_aleteo - 10)
                    pato.reiniciar()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

    # 2. ACTUALIZACIÓN DE LÓGICA
    pato.actualizar()

    # 3. RENDERIZADO
    if tiene_fondo:
        pantalla.blit(superficie_fondo, (0, 0))
    else:
        pantalla.fill(COLOR_FALLBACK)
        
    pato.dibujar(pantalla)
    mira.dibujar(pantalla, pos_mouse)
    
    # HUD
    pygame.draw.rect(pantalla, COLOR_PANEL, (0, ALTO - 60, ANCHO, 60))
    txt_hud = f"IMPACTOS: {impactos}  |  TOTAL DISPAROS: {intentos}"
    surface_hud = fuente_hud.render(txt_hud, True, COLOR_TEXTO)
    pantalla.blit(surface_hud, (20, ALTO - 42))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()