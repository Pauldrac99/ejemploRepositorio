import pygame
import sys
from config import *
from network.client import NetworkClient
from scenes.menu import MenuScene
from renderer.drawer import *

def main():
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Pong Online - Cliente")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24, bold=True)
    
    # Fuente gigante para la cuenta regresiva
    big_font = pygame.font.SysFont("Arial", 80, bold=True)

    net = NetworkClient(SERVER_URL)
    net.connect()

    current_scene = "menu"
    menu = MenuScene(screen, font)
    game_state = None
    room_id = ""
    countdown_val = None  # NUEVA VARIABLE: Guarda el 3, 2, 1, GO

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if current_scene == "menu": menu.handle_event(event, net)
            elif current_scene == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: net.send({"type": "input", "key": "up", "pressed": True})
                    if event.key == pygame.K_DOWN: net.send({"type": "input", "key": "down", "pressed": True})
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP: net.send({"type": "input", "key": "up", "pressed": False})
                    if event.key == pygame.K_DOWN: net.send({"type": "input", "key": "down", "pressed": False})

        for msg in net.get_messages():
            msg_type = msg.get("type")
            if current_scene == "menu":
                if msg_type == "created":
                    room_id = msg["roomId"]; current_scene = "waiting"
                elif msg_type == "joined":
                    # CORRECCIÓN CRÍTICA: Antes decía "waiting". Ahora va directo a "playing"
                    room_id = msg["roomId"]; current_scene = "playing"
                elif msg_type == "error":
                    menu.status_msg = msg["message"]; menu.action = None
            elif current_scene == "waiting":
                if msg_type == "opponentJoined": current_scene = "playing"
            elif current_scene == "playing":
                if msg_type == "state": 
                    game_state = msg["state"]
                    # Cuando el juego empiece a correr de verdad, borramos el texto del GO
                    if game_state['running']: countdown_val = None 
                elif msg_type == "countdown": 
                    countdown_val = str(msg["value"]) # Capturamos el 3, 2, 1, GO
                elif msg_type == "gameover": current_scene = "gameover"

        # --- DIBUJO ---
        screen.fill(BG_COLOR)
        
        if current_scene == "menu": 
            menu.draw()
            
        elif current_scene == "waiting":
            draw_text(screen, font, "SALA: " + room_id, SCREEN_W//2, SCREEN_H//2 - 40, (0,255,136), center=True)
            draw_text(screen, font, "Esperando oponente...", SCREEN_W//2, SCREEN_H//2 + 20, (150,150,150), center=True)
            
        elif current_scene == "playing":
            # Si ya llegaron los datos del juego, dibujamos el campo
            if game_state:
                draw_center_line(screen)
                draw_score(screen, font, game_state['score'])
                draw_paddle(screen, game_state['paddle1'], P1_COLOR)
                draw_paddle(screen, game_state['paddle2'], P2_COLOR)
                if game_state['resetTimer'] <= 0: draw_ball(screen, game_state['ball'])
            
            # Si estamos en cuenta regresiva, la dibujamos encima de todo
            if countdown_val:
                draw_text(screen, big_font, countdown_val, SCREEN_W//2, SCREEN_H//2, (0,255,136), center=True)

        elif current_scene == "gameover":
            draw_text(screen, font, "FIN DEL JUEGO", SCREEN_W//2, SCREEN_H//2, (255,255,255), center=True)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__": main()