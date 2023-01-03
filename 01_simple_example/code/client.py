import string
import pygame
import typing
from player import Player

from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

def redrawWindow(player:Player, player2:Player):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.get_p()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(p, p2)

main()