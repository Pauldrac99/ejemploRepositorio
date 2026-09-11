import pygame
import sys
import os

# --- INICIALIZACIÓN ---
pygame.init()

# --- CONFIGURACIÓN DE LA VENTANA ---
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laboratorio: Mapas basados en Texturas de Tiles")
reloj = pygame.time.Clock()

# --- COLORES ---
COLOR_FONDO = (30, 40, 45)      
COLOR_TEXTO = (240, 240, 240)
COLOR_PANEL = (15, 15, 15)

# --- CONFIGURACIÓN DEL PISO (Mitad de pantalla: Y = 300) ---
Y_PISO = ALTO // 2  # 300
ALTO_PISO = 40
ANCHO_TILE = 80     

# Recomienda a tus alumnos colocar una textura con este nombre:
NOMBRE_TILE = "assets/sprites/tiles/2.png"

# Mapa de bloques: 1 = Hay bloque de imagen, 0 = Vacío (Agujero)
MAPA_PISO = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# --- FUENTES ---
fuente_hud = pygame.font.SysFont("monospace", 18, bold=True)

# --- CARGAR Y CONFIGURAR LA TEXTURA DEL TILE ---
if os.path.exists(NOMBRE_TILE):
    # .convert() es ideal aquí porque los bloques del piso suelen ser opacos
    imagen_tile_original = pygame.image.load(NOMBRE_TILE).convert()
    # Forzamos geométricamente el escalado al tamaño de la celda de la rejilla (80x40)
    superficie_tile = pygame.transform.scale(imagen_tile_original, (ANCHO_TILE, ALTO_PISO))
else:
    # Respaldo didáctico en RAM si el alumno aún no crea el archivo "tile_piso.png"
    superficie_tile = pygame.Surface((ANCHO_TILE, ALTO_PISO))
    superficie_tile.fill((100, 150, 100)) # Bloque verde
    pygame.draw.rect(superficie_tile, (60, 100, 60), (0, 0, ANCHO_TILE, ALTO_PISO), 2) # Borde


# --- CARGA SECUENCIAL DE SPRITES DEL JUGADOR (1 a 8) ---
sprites_caminar = []
dimension_personaje = (64, 64)

for i in range(1, 9):
    nombre_archivo = f"assets/sprites/cat/Walk ({i}).png"
    if os.path.exists(nombre_archivo):
        img = pygame.image.load(nombre_archivo).convert_alpha()
        sprites_caminar.append(pygame.transform.scale(img, dimension_personaje))
else:
    for i in range(1, 9):
        surf_temp = pygame.Surface(dimension_personaje, pygame.SRCALPHA)
        pygame.draw.rect(surf_temp, (0, 150, 255), (16, 10, 32, 40))
        pygame.draw.rect(surf_temp, (255, 255, 255), (20, 50, 8, 14 if i % 2 == 0 else 6))
        pygame.draw.rect(surf_temp, (255, 255, 255), (36, 50, 8, 6 if i % 2 == 0 else 14))
        sprites_caminar.append(surf_temp)

# --- CLASE: PERSONAJE ---
class Personaje:
    def __init__(self):
        self.sprites = sprites_caminar
        self.frame_actual = 0
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.cadencia_animacion = 80 
        
        self.ancho = dimension_personaje[0]
        self.alto = dimension_personaje[1]
        self.x = 100
        self.y = Y_PISO - self.alto
        
        self.vel_x = 4
        self.vel_y = 0
        self.gravedad = 0.6
        
        self.mirando_derecha = True
        self.en_movimiento = False
        self.cayendo = False

    def actualizar(self, input_teclas):
        self.en_movimiento = False
        dx = 0
        
        if input_teclas[pygame.K_LEFT]:
            dx = -self.vel_x
            self.mirando_derecha = False
            self.en_movimiento = True
        elif input_teclas[pygame.K_RIGHT]:
            dx = self.vel_x
            self.mirando_derecha = True
            self.en_movimiento = True

        self.x += dx
        if self.x < 0:
            self.x = 0  
        elif self.x > ANCHO - self.ancho:
            self.x = ANCHO - self.ancho  

        centro_x = self.x + (self.ancho // 2)
        indice_bloque = int(centro_x // ANCHO_TILE)
        indice_bloque = max(0, min(indice_bloque, len(MAPA_PISO) - 1))
        
        sobre_linea_piso = (self.y + self.alto >= Y_PISO) and (self.y + self.alto <= Y_PISO + 10)
        
        if sobre_linea_piso and MAPA_PISO[indice_bloque] == 1 and not self.cayendo:
            self.y = Y_PISO - self.alto
            self.vel_y = 0
        else:
            self.vel_y += self.gravedad
            self.y += int(self.vel_y)
            if self.y > Y_PISO:
                self.cayendo = True 

        if self.en_movimiento and not self.cayendo and (self.y + self.alto == Y_PISO):
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_frame > self.cadencia_animacion:
                self.frame_actual = (self.frame_actual + 1) % len(self.sprites)
                self.tiempo_ultimo_frame = tiempo_actual
        else:
            self.frame_actual = 0

    def dibujar(self, superficie):
        sprite_actual = self.sprites[self.frame_actual]
        if not self.mirando_derecha:
            sprite_actual = pygame.transform.flip(sprite_actual, True, False)
        superficie.blit(sprite_actual, (self.x, self.y))


# --- INSTANCIACIÓN ---
jugador = Personaje()

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            if evento.key == pygame.K_r:
                jugador.x = 100
                jugador.y = Y_PISO - jugador.alto
                jugador.vel_y = 0
                jugador.cayendo = False

    teclas = pygame.key.get_pressed()
    jugador.actualizar(teclas)

    # 3. RENDERIZADO GRÁFICO
    pantalla.fill(COLOR_FONDO)
    
    # --- RENDERIZADO EN CADENA DE TILES REPETIDOS (Blitting iterativo) ---
    for i, bloque in enumerate(MAPA_PISO):
        if bloque == 1:
            tile_x = i * ANCHO_TILE
            # Dibujamos la textura escalada en la coordenada X correspondiente
            pantalla.blit(superficie_tile, (tile_x, Y_PISO))

    # Dibujar Personaje por encima de las texturas
    jugador.dibujar(pantalla)
    
    # HUD Inferior
    pygame.draw.rect(pantalla, COLOR_PANEL, (0, ALTO - 50, ANCHO, 50))
    txt_hud = "Controles: [← / →] Moverse  |  Presiona [R] para reiniciar"
    surface_hud = fuente_hud.render(txt_hud, True, COLOR_TEXTO)
    pantalla.blit(surface_hud, (20, ALTO - 34))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()