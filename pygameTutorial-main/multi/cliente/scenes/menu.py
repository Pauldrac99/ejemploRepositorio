import pygame
from config import *
from renderer.drawer import draw_text

class MenuScene:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.room_code = ""
        self.status_msg = ""
        self.action = None

    def handle_event(self, event, net_client):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: self.room_code = self.room_code[:-1]
            elif event.key == pygame.K_RETURN:
                # ---> NUEVA VALIDACIÓN <---
                if not net_client.connected:
                    self.status_msg = "ERROR: Sin conexion al servidor"
                    return
                # ----------------------------
                
                if self.room_code == "":
                    net_client.send({"type": "create"})
                    self.status_msg = "Creando sala..."
                    self.action = 'create'
                else:
                    net_client.send({"type": "join", "roomId": self.room_code.upper()})
                    self.status_msg = "Uniendose..."
                    self.action = 'join'
            elif len(self.room_code) < 4 and event.unicode.isalnum(): self.room_code += event.unicode.upper()
    def draw(self):
        self.screen.fill((10, 10, 10))
        draw_text(self.screen, self.font, "PONG ONLINE", SCREEN_W//2, 100, (0,255,136), center=True)
        draw_text(self.screen, self.font, "ENTER para crear sala", SCREEN_W//2, 200, (100,100,100), center=True)
        draw_text(self.screen, self.font, "Escribe codigo y ENTER para unirte", SCREEN_W//2, 240, (100,100,100), center=True)
        input_rect = pygame.Rect(SCREEN_W//2 - 60, 280, 120, 40)
        pygame.draw.rect(self.screen, (30,30,30), input_rect)
        pygame.draw.rect(self.screen, (0,255,136), input_rect, 2)
        draw_text(self.screen, self.font, self.room_code, SCREEN_W//2, 300, (255,255,255), center=True)
        draw_text(self.screen, self.font, self.status_msg, SCREEN_W//2, 360, (150,150,150), center=True)
