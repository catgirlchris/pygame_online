import pygame
pygame.font.init()

from network import Network
from game import Game

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win:pygame.Surface):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(self.text, 1, (149, 125, 173))
        win.blit(text, 
                (self.x + round(self.width/2) - round(text.get_width()/2),
                 self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(win:pygame.Surface, game:Game, player_id):
    win.fill((255, 223, 211))
    
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render("Your Move", 1, (224, 187, 228),)
        win.blit(text, (80, 200))

        text = font.render("Opponent's Move", 1, (224, 187, 228))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.both_went():
            text1 = font.render(move1, 1, (254, 200, 216))
            text2 = font.render(move2, 1, (254, 200, 216))
        else:
            if game.p1_went and player_id == 0:
                text1 = font.render(move1, 1, (254, 200, 216))
            elif game.p1_went:
                text1 = font.render("Locked In", 1, (254, 200, 216))
            else:
                text1 = font.render("Waiting...", 1, (254, 200, 216))

            if game.p2_went and player_id == 1:
                text2 = font.render(move2, 1, (254, 200, 216))
            elif game.p2_went:
                text2 = font.render("Locked In", 1, (254, 200, 216))
            else:
                text2 = font.render("Waiting...", 1, (254, 200, 216))

        if player_id == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)
    
    pygame.display.update()



btns = [Button("Rock", 50, 500, (224, 187, 228)), Button("Scissors", 250, 500, (210, 145, 188)), Button("Paper", 450, 500, (254, 200, 216))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player_id = int(n.get_p())
    print("You are player", player_id)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.both_went():
            redrawWindow(win, game, player_id)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 30)
            if (game.winner() == 1 and player_id == 1) or (game.winner() == 0 and player_id == 0):
                text = font.render("You won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You lost!", 1, (255,0,0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player_id == 0:
                            if not game.p1_went:
                                n.send(btn.text)
                        else:
                            if not game.p2_went:
                                n.send(btn.text)
        redrawWindow(win, game, player_id)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    
    while run:
        clock.tick(60)
        win.fill((255, 223, 211))
        font = pygame.font.SysFont("timesnewroman", 60)
        text = font.render("Click to play!", 1, (224, 187, 228))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()

while True:
    menu_screen()