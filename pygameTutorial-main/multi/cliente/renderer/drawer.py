import pygame
from config import *

def draw_paddle(screen, paddle, color):
    pygame.draw.rect(screen, color, (paddle['x'], paddle['y'], paddle['width'], paddle['height']), border_radius=5)

def draw_ball(screen, ball):
    pygame.draw.circle(screen, BALL_COLOR, (int(ball['x']), int(ball['y'])), ball['radius'])

def draw_center_line(screen):
    for y in range(0, SCREEN_H, 20): pygame.draw.rect(screen, (30, 30, 30), (SCREEN_W // 2 - 1, y, 2, 10))

def draw_score(screen, font, score):
    txt1 = font.render(str(score['p1']), True, P1_COLOR)
    txt2 = font.render(str(score['p2']), True, P2_COLOR)
    screen.blit(txt1, (SCREEN_W // 4 - txt1.get_width()//2, 20))
    screen.blit(txt2, (3 * SCREEN_W // 4 - txt2.get_width()//2, 20))

def draw_text(screen, font, text, x, y, color=FONT_COLOR, center=False):
    txt = font.render(text, True, color)
    if center: screen.blit(txt, (x - txt.get_width()//2, y - txt.get_height()//2))
    else: screen.blit(txt, (x, y))
