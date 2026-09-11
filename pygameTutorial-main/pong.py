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
pygame.display.set_caption("Laboratorio: Pong Clásico (Álgebra y Trigonometría)")
reloj = pygame.time.Clock()

# --- COLORES ---
COLOR_FONDO = (30, 30, 30)
COLOR_ROJO = (230, 57, 70)     # Jugador Izquierdo
COLOR_AZUL = (69, 123, 157)    # Jugador Derecho
COLOR_BLANCO = (241, 250, 238)
COLOR_LINEA = (100, 100, 100)

# --- FUENTES ---
fuente_marcador = pygame.font.SysFont("monospace", 60, bold=True)
fuente_info = pygame.font.SysFont("monospace", 18)

# --- GENERADOR DE EFECTOS DE SONIDO SINTÉTICOS (En Tiempo Real) ---
def generar_sonido_sintetico(frecuencia, duracion_ms, tipo="beep"):
    """Genera un efecto de sonido en la memoria RAM usando NumPy sin archivos externos."""
    frecuencia_muestreo = 44100
    num_muestras = int(frecuencia_muestreo * (duracion_ms / 1000.0))
    
    # Arreglo de tiempo
    t = np.linspace(0, duracion_ms / 1000.0, num_muestras, False)
    
    # Onda senoidal base
    if tipo == "golpe":
        # Caída de frecuencia para simular un rebote opaco
        f = frecuencia * np.exp(-15 * t)
        onda = np.sin(2 * np.pi * f * t)
    else:
        # Onda cuadrada limpia para el marcador/reinicio
        onda = np.sign(np.sin(2 * np.pi * frecuencia * t))
        
    # Suavizado de bordes (Fade out) para evitar clics de audio abruptos
    atenuacion = np.linspace(1.0, 0.0, num_muestras)
    datos_audio = (onda * atenuacion * 16383).astype(np.int16)
    
    # Convertir a sonido estéreo duplicando canales
    datos_estereo = np.vstack((datos_audio, datos_audio)).T.copy(order='C')
    
    return pygame.mixer.Sound(buffer=datos_estereo)

# Pre-cargar sonidos en caché
sonido_rebote_paleta = generar_sonido_sintetico(440, 100, "beep")
sonido_rebote_pared = generar_sonido_sintetico(220, 80, "golpe")
sonido_punto = generar_sonido_sintetico(587, 300, "beep")

# --- ENTIDADES DEL JUEGO ---
class Paleta:
    def __init__(self, x, color):
        self.ancho = 15
        self.alto = 90
        self.x = x
        self.y = ALTO // 2 - self.alto // 2
        self.velocidad = 7
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def mover(self, arriba, abajo):
        if arriba and self.y > 0:
            self.y -= self.velocidad
        if abajo and self.y < ALTO - self.alto:
            self.y += self.velocidad
        self.rect.y = self.y

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect, border_radius=4)


class Bola:
    def __init__(self):
        self.radio = 10
        self.velocidad_base = 7
        self.reiniciar()

    def reiniciar(self):
        self.x = ANCHO // 2
        self.y = ALTO // 2
        
        # Trigonometría básica: Ángulo de salida aleatorio entre -45 y 45 grados
        # Multiplicado por una dirección aleatoria (izquierda o derecha)
        angulo = math.radians(np.random.uniform(-45, 45))
        direccion = np.random.choice([-1, 1])
        
        # Descomposición vectorial: velocidad en componentes X e Y
        self.vx = self.velocidad_base * math.cos(angulo) * direccion
        self.vy = self.velocidad_base * math.sin(angulo)

    def actualizar(self, paleta_izq, paleta_der):
        puntos_cambiados = 0 # 1 para punto Izq, 2 para punto Der
        
        # Movimiento lineal continuo (Física Euleriana básica)
        self.x += self.vx
        self.y += self.vy

        # --- COLISIÓN CON TECHO Y SUELO (Reflexión en Y) ---
        if self.y - self.radio <= 0:
            self.y = self.radio
            self.vy *= -1
            sonido_rebote_pared.play()
        elif self.y + self.radio >= ALTO:
            self.y = ALTO - self.radio
            self.vy *= -1
            sonido_rebote_pared.play()

        # Crear una bounding box temporal para la bola en Pygame
        bola_rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

        # --- COLISIÓN CON PALETA IZQUIERDA (Rojo) ---
        if bola_rect.colliderect(paleta_izq.rect) and self.vx < 0:
            sonido_rebote_paleta.play()
            # Factor de transferencia de momento angular: según dónde golpee la bola en la paleta
            impacto_relativo = (self.y - (paleta_izq.y + paleta_izq.alto / 2)) / (paleta_izq.alto / 2)
            angulo_rebote = impacto_relativo * math.radians(50) # Máximo 50 grados de desviación
            
            self.vx = self.velocidad_base * math.cos(angulo_rebote)
            self.vy = self.velocidad_base * math.sin(angulo_rebote)
            # Incrementar ligeramente la velocidad para aumentar la dificultad del rally
            self.vx *= 1.05
            self.vy *= 1.05

        # --- COLISIÓN WITH PALETA DERECHA (Azul) ---
        if bola_rect.colliderect(paleta_der.rect) and self.vx > 0:
            sonido_rebote_paleta.play()
            impacto_relativo = (self.y - (paleta_der.y + paleta_der.alto / 2)) / (paleta_der.alto / 2)
            angulo_rebote = impacto_relativo * math.radians(50)
            
            self.vx = -self.velocidad_base * math.cos(angulo_rebote)
            self.vy = self.velocidad_base * math.sin(angulo_rebote)
            self.vx *= 1.05
            self.vy *= 1.05

        # --- CONDICIONES DE ANOTACIÓN (Límites Laterales) ---
        if self.x < 0:
            sonido_punto.play()
            puntos_cambiados = 2 # Punto para el jugador Derecho (Azul)
            self.reiniciar()
        elif self.x > ANCHO:
            sonido_punto.play()
            puntos_cambiados = 1 # Punto para el jugador Izquierdo (Rojo)
            self.reiniciar()
            
        return puntos_cambiados

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, COLOR_BLANCO, (int(self.x), int(self.y)), self.radio)


# --- INSTANCIACIÓN DE OBJETOS ---
paleta_izquierda = Paleta(30, COLOR_ROJO)
paleta_derecha = Paleta(ANCHO - 30 - 15, COLOR_AZUL)
bola_juego = Bola()

puntaje_izq = 0
puntaje_der = 0

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    
    # 1. GESTIÓN DE EVENTOS E INPUTS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Reinicio manual del tablero
                puntaje_izq = 0
                puntaje_der = 0
                bola_juego.reiniciar()
                sonido_punto.play()

    # Mapeo de estados del teclado continuo (Polling)
    teclas = pygame.key.get_pressed()
    
    # Controles Jugador Izquierdo (W / S)
    paleta_izquierda.mover(teclas[pygame.K_w], teclas[pygame.K_s])
    # Controles Jugador Derecho (Cursores Flecha Arriba / Abajo)
    paleta_derecha.mover(teclas[pygame.K_UP], teclas[pygame.K_DOWN])

    # 2. ACTUALIZACIÓN DE LÓGICA FÍSICA
    resultado_punto = bola_juego.actualizar(paleta_izquierda, paleta_derecha)
    if resultado_punto == 1:
        puntaje_izq += 1
    elif resultado_punto == 2:
        puntaje_der += 1

    # 3. RENDERIZADO GRÁFICO
    pantalla.fill(COLOR_FONDO)
    
    # Red de Enmedio (Línea punteada clásica)
    for y in range(0, ALTO, 30):
        pygame.draw.rect(pantalla, COLOR_LINEA, (ANCHO // 2 - 2, y, 4, 15))

    # Dibujar Elementos dinámicos
    paleta_izquierda.dibujar(pantalla)
    paleta_derecha.dibujar(pantalla)
    bola_juego.dibujar(pantalla)

    # Renderizar los Marcadores (Texto)
    texto_izq = fuente_marcador.render(str(puntaje_izq), True, COLOR_ROJO)
    texto_der = fuente_marcador.render(str(puntaje_der), True, COLOR_AZUL)
    pantalla.blit(texto_izq, (ANCHO // 4 - texto_izq.get_width() // 2, 30))
    pantalla.blit(texto_der, (3 * ANCHO // 4 - texto_der.get_width() // 2, 30))

    # Barra de instrucciones inferior
    texto_ayuda = fuente_info.render("[W/S] Rojo  |  [▲/▼] Azul  |  [ESPACIO] Reiniciar todo", True, COLOR_LINEA)
    pantalla.blit(texto_ayuda, (ANCHO // 2 - texto_ayuda.get_width() // 2, ALTO - 30))

    # Actualizar Pantalla y regular FPS
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()