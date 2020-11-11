import pygame
import time
import random

pygame.init()

white = random.choice([(255, 255, 255), (255,251,247), (251,247,255), (247,255,251), (255,246,223)])
score = random.choice([(3,51,121), (255, 255, 102), (199,137,27)])
snake = random.choice([(0, 0, 0), (47,121,11), (18,48,4)])
msg = random.choice([(213, 50, 80) ,(150,27,52), (0,0,0), (47,47,47)])
apple = random.choice([(86,217,22), (220,37,2), (132,22,1)])
back_ground = random.choice([(174,199,186), (199,186,174), (220,214,227),
							 (174,187,199), (121,73,3) , (226,220,212)])

dis_width, dis_height = 1000, 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('🍎  Friendly Sssnake!   🐛')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


events = [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],]



def the_score(score):
    value = score_font.render("Your Score: " + str(score), True, score)
    dis.blit(value, [dis_width, dis_height])


def friendly_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(back_ground)
            message("You Lost! Press ""C"" to Play Again or ""Q"" to quitQuit", msg)
            the_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event == pygame.QUIT:
                game_over = True

        for event in events:
            if event:
                if event == left:
                    x1_change = -snake_block
                    y1_change = 0
                elif event == right:
                    x1_change = snake_block
                    y1_change = 0
                elif event == up:
                    y1_change = -snake_block
                    x1_change = 0
                elif event == down:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(back_ground)
        pygame.draw.rect(dis, apple, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Head toutch body
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True


        friendly_snake(snake_block, snake_List)
        the_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
