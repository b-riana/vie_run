import pygame
import time
import random
pygame.font.init() # initializes font module

# CONST VARIABLES
WIDTH, HEIGHT = 1000, 800; #pixel size

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 120

PLAYER_VEL = 7

BUG_WIDTH = 50
BUG_HEIGHT = 100

BUG_VEL = 3

SNAKE_WIDTH = 80
SNAKE_HEIGHT = 40

SNAKE_VEL = 2

FONT = pygame.font.SysFont("arial", 30, bold = True)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vie Run")

# CHARACTTER LOADING
BG = pygame.transform.scale(pygame.image.load("fixedGrass.png"), (WIDTH, HEIGHT)) #scales image
VIE = pygame.transform.scale(pygame.image.load("betterVie.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)) #scales image
BUG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("betterBug.png"), (BUG_WIDTH, BUG_HEIGHT)), 180) #scales image
SNAKE = pygame.transform.scale(pygame.image.load("betterSnake.png"), (SNAKE_WIDTH, SNAKE_HEIGHT))

def draw(player, elapsed_time, bugs, bugs_eaten, snakes):
    WIN.blit(BG, (0,0)) # image/object, coordinate
    
    WIN.blit(VIE, player, area=None, special_flags=0)
    
    text_bg = pygame.Rect(0, 0, 200, 100)
    pygame.draw.rect(WIN, "black", text_bg)
    text_bg2 = pygame.Rect(5, 5, 190, 90)
    pygame.draw.rect(WIN, "grey", text_bg2)
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "black")
    WIN.blit(time_text, (10,10))
    
    bug_text = FONT.render(f"Bugs eaten: {bugs_eaten}", 1, "black")
    WIN.blit(bug_text, (10, 50))
    
    #pygame.draw.rect(WIN, "red", player) # source, color (string or rgb), rectangle var
    
    for bug in bugs:
        WIN.blit(BUG, bug, area=None, special_flags=0)
        
    for snake in snakes:
        WIN.blit(SNAKE, snake, area=None, special_flags=0)
    
    pygame.display.update() # refreshes and applies drawing

def main():
    run = True
    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time() #gets current time
    elapsed_time = 0
    
    bug_add_increment = 1600
    bug_count = 0
    bugs = []
    
    eat = False
    bugs_eaten = 0
    
    snake_add_increment = 2000
    snake_count = 0
    snakes = []
    
    bit = False
    
    # INTO CARD
    intro_txt = FONT.render("Lvl I: Play as Vie, dodge the snakes and eat the bugs!", 1, "white")
            
    WIN.blit(intro_txt, (WIDTH/2 - intro_txt.get_width()/2, HEIGHT/2 - intro_txt.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)
    
    while run:
        bug_count += clock.tick(60)
        snake_count += clock.tick(60)
        elapsed_time = time.time() - start_time # seconds since start
        
        if bug_count > bug_add_increment:
            bug_add = random.randint(0,3)
            for _ in range(bug_add):
                bug_x = random.randint(0, WIDTH - BUG_WIDTH)
                bug = pygame.Rect(bug_x, -BUG_HEIGHT, BUG_WIDTH, BUG_HEIGHT)
                bugs.append(bug)
                
            bug_count = 0
            bug_add_increment = max(200, bug_add_increment - 50) # starts at 2000, decrements by 50 getting faster
        
        if snake_count > snake_add_increment:
            snake_add = random.randint(0,4)
            for _ in range(snake_add):
                snake_y = random.randint(90, HEIGHT - SNAKE_HEIGHT - 15)
                snake = pygame.Rect(-SNAKE_WIDTH, snake_y, SNAKE_WIDTH, SNAKE_HEIGHT)
                snakes.append(snake)
                
            snake_count = 0
            snake_add_increment = max(200, snake_add_increment - 70) # starts at 2000, decrements by 50 getting faster
        
        ## Checking for quit action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        # Moves vie
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0: # Checking if left arrow key was pressed
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0: # Checking if left arrow key was pressed
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            player.y += PLAYER_VEL

            
        # Moves snakes
        for bug in bugs[:]: # makes copy of list
            bug.y += BUG_VEL
            if bug.y > HEIGHT:
                bugs.remove(bug)
            elif bug.y + bug.height >= player.y and bug.colliderect(player):
                bugs.remove(bug)
                eat = True
                bugs_eaten += 1
                break
            
        # Moves snakes
        for snake in snakes[:]: # makes copy of list
            snake.x += SNAKE_VEL
            if snake.x > WIDTH:
                snakes.remove(snake)
            elif snake.x + snake.width >= player.x and snake.colliderect(player):
                snakes.remove(snake)
                bit = True
                break
        
        draw(player, elapsed_time, bugs, bugs_eaten, snakes)
        
        if bit:
            lose_txt = FONT.render("Vie got bit!", 1, "white")
            lose_bg = pygame.Rect(WIDTH/2 - lose_txt.get_width()/2-10, HEIGHT/2 - lose_txt.get_height()/2-10, 140, 60)
            pygame.draw.rect(WIN, "black", lose_bg)
            
            WIN.blit(lose_txt, (WIDTH/2 - lose_txt.get_width()/2, HEIGHT/2 - lose_txt.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        
        
        if bugs_eaten == 15:
            win_txt = FONT.render("Vie is full!", 1, "white")
            win_bg = pygame.Rect(WIDTH/2 - win_txt.get_width()/2-10, HEIGHT/2 - win_txt.get_height()/2-10, 140, 60)
            pygame.draw.rect(WIN, "black", win_bg)
            
            WIN.blit(win_txt, (WIDTH/2 - win_txt.get_width()/2, HEIGHT/2 - win_txt.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)

            break
    
    pygame.quit()
    
    
if __name__ == "__main__": #ensures file is directly executed rather than imported
    main()