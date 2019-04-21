import pygame
import sys
import random
#initialising pygame
pygame.init()


player_color=(255,0,0)
enemy_color=(255,255,0)
bgcolor = (158,201,229)
text_color = (0,0,0)
font_score = pygame.font.SysFont("BatangChe",35)


WIDTH_SCREEN=600
HEIGHT_SCREEN=600



player_size=45
enemy_size=16

enemy_pos_x=random.randint(0,WIDTH_SCREEN-enemy_size)


player_pos=[WIDTH_SCREEN/2,HEIGHT_SCREEN-player_size] #player_pos[0]==x-coordinate, player_pos[1]==y-coordinate
enemy_pos=[enemy_pos_x,0]   #enemy_pos[0]==x-coordinate, enemy_pos[1]==y-coordinate


enemy_list=[enemy_pos] #will contain the position of multiple enemies

SPEED_ENEMY=5

score=0

#add enemy to enemy_list
def enemy_population_control(enemy_list):
    delay = random.random()
    if len(enemy_list)<10 and delay < 0.2:
        x_pos=random.randint(0,WIDTH_SCREEN-enemy_size)
        y_pos=0
        enemy_list.append([x_pos,y_pos])

#enemy draw function
def draw_enemy(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.circle(root,enemy_color,(enemy_pos[0],enemy_pos[1]),enemy_size)


#update the position of enemy
def update_enemy_pos(enemy_list,score):
    for enemy_pos in enemy_list:
        if enemy_pos[1]>=0 and enemy_pos[1]<HEIGHT_SCREEN:
            enemy_pos[1]+=SPEED_ENEMY
        else:
            enemy_list.remove(enemy_pos)
            score+=1
    return score

# increase speed of enemy as score increases
def enemy_speed_increase(score, SPEED_ENEMY):
    if score> 20:
        SPEED_ENEMY = 8
    elif score> 30:
        SPEED_ENEMY = 12
    elif score> 40:
        SPEED_ENEMY = 15
    return SPEED_ENEMY


#detect collision function
def detect_collision(player_pos,enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y <(p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def check_collision(player_pos,enemy_list):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos,enemy_pos):
            return True
    else:
        return False


root=pygame.display.set_mode((WIDTH_SCREEN,HEIGHT_SCREEN)) #creating display
pygame.display.set_caption("Meteor Shower")#giving a caption

clock=pygame.time.Clock()

game_over=False


#game loop starts
while not game_over:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==pygame.KEYDOWN:
            x=player_pos[0]
            y=player_pos[1]
            if event.key==pygame.K_LEFT:
                x-=player_size
            if event.key==pygame.K_RIGHT:
                x+=player_size
            player_pos=[x,y]

    root.fill(bgcolor)
    SPEED_ENEMY = enemy_speed_increase(score, SPEED_ENEMY)
    enemy_population_control(enemy_list)
    score=update_enemy_pos(enemy_list,score)
    text = "Score:" + str(score)
    label = font_score.render(text,1,text_color)
    root.blit(label,(WIDTH_SCREEN-120,HEIGHT_SCREEN-580))
    print("Score:", score, "Speed Enemy:", SPEED_ENEMY)
    draw_enemy(enemy_list)
    if check_collision(player_pos,enemy_list):
        print("Game Over!!")
        game_over=True




    pygame.draw.rect(root,player_color,(player_pos[0],player_pos[1],player_size,player_size))

    clock.tick(45)
    pygame.display.update()

quit()
