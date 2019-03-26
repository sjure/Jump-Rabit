import pygame
import random
import time
from classes import *

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
pink = (204, 0, 255)
darker_pink = (204, 0, 204)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255,255)

display_width = 1000
display_height = 600

clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("FlyRabbit")
bakgrunn = pygame.image.load("space.jpg")
kanin_original = pygame.image.load("kanin1.png")
kanin_kappe = pygame.image.load("kanin2.png")
kanin_swag = pygame.image.load("kanin3.png")
kanin_snoop = pygame.image.load("kanin4.png")
planet1 = pygame.image.load("planet1.png")
planet2 = pygame.image.load("planet2.png")
planet3 = pygame.image.load("planet3.png")
planet4 = pygame.image.load("planet4.png")
planet5 = pygame.image.load("planet5.png")
coin_img = pygame.image.load("coin.png")
shop_img = pygame.image.load("shop.png")
lock_img = pygame.image.load("lock.png")
green_check = pygame.image.load("greencheck.png")
intro_screen = pygame.image.load("Intro.png")

kaninen = Kanin(display_width * 0.2, display_height * 0.6)
kanin_img = Kanin_img_class(kanin_original)
planeten1 = Planet(display_width * 0.6, display_height * 0.5, planet1, -1)
planeten2 = Planet(display_width + 100, display_height * 0.7, planet2, -2)
planeten3 = Planet(display_width + 100, display_height * 0.6, planet3, -0.9)
planeten4 = Planet(display_width + 800, display_height * 0.3, planet4, -1.5)
planeten5 = Planet(display_width + 1000, display_height * 0.6, planet5, -1.35)
start_planet = Planet(display_width*0.13, display_height * 0.78, planet4, -0.7)
#planeten6 = Planet(display_width*0.5, display_height + 50, planet5, -1.35)
planeter = [planeten1, planeten2, planeten3, planeten4, planeten5, start_planet]
lock1 = Lock(display_width*0.05,display_height*0.75, lock_img, 100, kanin_swag, "lock1")
lock2 = Lock(display_width*0.36,display_height*0.75, lock_img, 250, kanin_kappe, "lock2")
lock3 = Lock(display_width*0.7,display_height*0.75, lock_img, 500, kanin_snoop, "lock3")
lock_list = [lock1,lock2,lock3]

coin1 = Coin(1500, 250, coin_img, -1, -1)
coin2 = Coin(1000, 350, coin_img, -2.5, -2)
coin_list = [coin1, coin2]
coinscore = Scores()
checkmark = Checkmark(green_check)

def hoppe(self):
    if self.bakken or self.hopp < 2:
        self.gravity = -0.5
        self.velocity = 15
        self.hopp += 1

def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def new_score(score):
    with open("highscores.txt", "w") as f:
        f.write(str(score) + "\n" + str(coinscore.coins))

def display_highscore(highscore):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Highscore: " + str(coinscore.highscore), True, blue)
    coin_text = font.render("Coins: " + str(coinscore.coins), True, blue)
    gameDisplay.blit(text, (0,100))
    gameDisplay.blit(coin_text, (0,50))

def print_subtext(string):
    largeText = pygame.font.SysFont("comicsanssms", 70)
    textSurf, textRect = text_objects(string, largeText, red)
    textRect.center = ((display_width/2), (display_height/2 + 50))
    gameDisplay.blit(textSurf, textRect)

def score(count):
    font = pygame.font.SysFont(None,50)
    text = font.render("Score: " + str(count), True, blue)
    gameDisplay.blit(text,(0,0))

def button(msg,x,y,w,h,interactive_color,active_color, text_color, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,active_color,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay,interactive_color,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText, text_color)
    textRect.center = ((x + w/2), (y + h/2))
    gameDisplay.blit(textSurf, textRect)

def empty_button(object,active_color, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect_width = 6
    if object.x + object.width > mouse[0] > object.x and object.y + object.height > mouse[1] > object.y:
        pygame.draw.rect(gameDisplay, active_color, (object.x - rect_width/2,object.y+rect_width/2,object.width+rect_width/2,object.height+rect_width/2), rect_width)
        if click[0] == 1 and action != None:
            action()

def kollisjon_gravity(var, spiller):
    if var:
        if spiller.velocity < 0:
            spiller.gravity = 0
            spiller.velocity = 0
        if spiller.falling:
            spiller.bakken = True
            spiller.hopp = 0
    if not var:
        spiller.gravity = -0.5
        spiller.bakken = False

def kollisjon(spiller, planet):
    if planet.x <= spiller.x <= planet.x + planet.width or planet.x <= spiller.x + spiller.width <= planet.x + planet.width:
        if planet.y - 10 <= spiller.y + spiller.height <= planet.y + planet.height +10 and (spiller.falling or spiller.bakken):
            return True
        else:
            return False
    else:
        return False

def kollisjon_med_alle(spiller):
    x = 0
    for planet in planeter:
        if kollisjon(spiller, planet):
            x = 1
            kollisjon_gravity(True, spiller)
    if x == 0:
        kollisjon_gravity(False, spiller)

def stop():
    pygame.quit()
    quit()

def crash(current_score):
    crashed = True
    largeText = pygame.font.SysFont("cosmicsansms", 75)
    TextSurf, TextRect = text_objects("Du er utenfor banen", largeText, red)
    TextRect.center = ((display_width/2), (display_height/2)-50)
    gameDisplay.blit(TextSurf, TextRect)
    score(int(current_score))
    display_highscore(int(coinscore.highscore))

    if current_score > int(coinscore.highscore):
        new_score(current_score)
    else:
        new_score(coinscore.highscore)

    while crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Spill igjen!", 150, 450, 220, 100,pink, darker_pink, white, game_loop)
        button("Quit", 600, 450, 220, 100, pink, darker_pink, white, stop)
        button("Shop", 375, 450, 220, 100, pink, darker_pink, white, shop)
        pygame.display.update()
        clock.tick(15)

def quit_game():
    pygame.quit()
    quit()

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(intro_screen,(0,0))
        #button(msg, x, y, w, h, interactive_color, active_color, text_color, action=None)
        button("Play!", display_width*0.05, display_height*0.7, 100,70,pink, darker_pink,white, game_loop)
        button("Shop!", display_width*0.45, display_height*0.4, 100,70, pink, darker_pink, white, shop)
        button("QUIT", display_width*0.85, display_height*0.7, 100, 70, pink,darker_pink,white, quit_game)
        pygame.display.update()
        clock.tick(15)

def display_coins_shop():
    font = pygame.font.SysFont(None, 120)
    coin_text = font.render(str(coinscore.coins), True, cyan)
    gameDisplay.blit(coin_text, (370, 35))

def shop():
    with open("highscores.txt", "r") as f:
        coinscore.highscore, coinscore.coins = int(f.readline()), int(f.readline())
    with open("Purchases.txt") as f:
        lock1.locked, lock2.locked, lock3.locked = bool(int(f.readline())),bool(int(f.readline())), bool(int(f.readline()))
    shopping = True
    while shopping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(shop_img, (0, 0))
        button("Play!", display_width * 0.40, display_height * 0.23, 100, 70, pink, darker_pink, white, game_loop)
        button("QUIT", display_width * 0.50, display_height * 0.23, 100, 70, pink, darker_pink, white, quit_game)
        display_coins_shop()
        lock1.render(gameDisplay)
        lock2.render(gameDisplay)
        lock3.render(gameDisplay)
        coinscore.lock = lock1
        empty_button(lock1,darker_pink,purchase)
        coinscore.lock = lock2
        empty_button(lock2,darker_pink,purchase)
        coinscore.lock = lock3
        empty_button(lock3,darker_pink,purchase)
        checkmark.render(gameDisplay)
        pygame.display.update()
        clock.tick(30)

def print_large_text(string):
    largeText = pygame.font.SysFont("cosmicsansms", 75)
    TextSurf, TextRect = text_objects(string, largeText, pink)
    TextRect.center = ((display_width / 2), (display_height / 2) - 50)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(1)

def purchase():
    item = coinscore.lock
    if not item.locked:
        kanin_img.img = item.rabit_img
        checkmark.render(gameDisplay, item.name)
    elif int(coinscore.coins) >= int(item.price) and item.locked:
        coinscore.coins -= item.price
        item.locked = False
        update_purchases()
        kanin_img.img = item.rabit_img
        new_score(coinscore.highscore)
        checkmark.render(gameDisplay, item.name)
        print_large_text("Kjøpt!")
    elif int(coinscore.coins) < int(item.price):
        print_large_text("Du har ikke nok coins :(")

def update_purchases():
    with open("Purchases.txt", "w") as f:
        f.write(str(int(bool(lock1.locked))) + "\n" + str(int(bool(lock2.locked))) + "\n" + str(int(bool(lock3.locked))))

def render_kanin_og_planeter(ekstra = None):
    for planet in planeter:
        planet.render(gameDisplay)
        if ekstra != None:
            ekstra.render(gameDisplay)
    kaninen.render(kanin_img, gameDisplay)

def level_up():
    kaninen.speed += 1
    for planet in planeter:
        planet.speed -= 0.4
    kaninen.hopp = 2
    largeText = pygame.font.SysFont("cosmicsansms", 60)
    TextSurf, TextRect = text_objects("NEXT LEVEL MANN!", largeText, darker_pink)
    TextRect.center = ((display_width / 2), (display_height / 2) - 50)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

def coin_movement(coin):
    if coin.x + coin.width < 0:
        coin.x = display_width + 500
        coin.y = random.randrange(0, display_height - coin.height)
        coin.xspeed = random.randrange(-2, -1) - 1.5 * random.random()
        coin.yspeed = random.randrange(-2, -1) - 1.5 * random.random()
        coin.taken = False
    if coin.y <= 0 or coin.y >= display_height - coin.height:
        coin.yspeed = -coin.yspeed

def coin_collision(coin, player):
    if coin.x < player.x + player.width < coin.x + coin.width or coin.x < player.x < coin.x + coin.width:
        if coin.y < player.y + player.height < coin.y + coin.height or coin.y < player.y < coin.y + coin.height:
            if not coin.taken:
                coin.taken = True
                coinscore.coins += 1



def game_loop():
    x_change = 0
    number_of_loops = 0
    gameExit = False
    button_pressed = False
    current_level = 0
    kaninen = Kanin(display_width * 0.2, display_height * 0.6)
    start_planet.x, start_planet.y = display_width*0.13, display_height * 0.78
    with open("highscores.txt", "r") as f:
        coinscore.highscore, coinscore.coins = int(f.readline()), int(f.readline())
    while not button_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                button_pressed = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    hoppe(kaninen)
                    button_pressed = True
        gameDisplay.blit(bakgrunn, (0, 0))
        render_kanin_og_planeter(start_planet)
        pygame.display.update()
        clock.tick(30)

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_change = kaninen.speed
                elif event.key == pygame.K_LEFT:
                    x_change = -kaninen.speed
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    hoppe(kaninen)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        kaninen.x += x_change
        if (number_of_loops %2==0):
            gameDisplay.blit(bakgrunn, (0, 0))

        kaninen.update()
        current_score = number_of_loops // 100

        for planet in planeter: #render planeter og spawne dem på nytt
            if planet.x + planet.width < 0:
                planet.x = display_width + 500
                planet.y = random.randrange(50, display_height + 50)
            planet.x += planet.speed
            planet.render(gameDisplay)

        for coin in coin_list:
            coin.x += coin.xspeed
            coin.y += coin.yspeed
            coin_collision(coin, kaninen)
            coin.render(gameDisplay) #oppdaterer posisjon
            coin_movement(coin) #sjekker om posisjon er utenfor brettet og spawner på nytt

        kaninen.render(kanin_img, gameDisplay)
        kollisjon_med_alle(kaninen)


        if kaninen.y > display_height + 100: #skjekker om crash
            if current_score > int(coinscore.highscore):
                print_subtext("Ny ToppScore: " + str(current_score))
            crash(current_score)
        number_of_loops += 1


        if (current_score // 20) - current_level >=1:
            current_level += 1
            level_up()

        score(current_score)
        display_highscore(coinscore.highscore)
        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()
