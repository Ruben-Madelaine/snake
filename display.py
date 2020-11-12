import pygame
import time
import random


pygame.init()


score_c = random.choice([(3,51,121), (255, 255, 102), (199,137,27)])
snake_c = random.choice([(0, 0, 0), (47,121,11), (18,48,4)])
msg_c = random.choice([(213, 50, 80) ,(150,27,52), (0,0,0), (47,47,47)])
apple_c = random.choice([(86,217,22), (220,37,2), (132,22,1)])
back_ground_c = random.choice([(174,199,186),   (199,186,174), (220,214,227),
							   (174,187,199),   (121,73,3),    (226,220,212),
                               (255, 255, 255), (255,251,247), (251,247,255), 
                               (247,255,251),   (255,246,223)
                               ])

dis_width, dis_height = 1000, 600


dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('🍎  Friendly Sssnake!   🐛')


clock = pygame.time.Clock()


snake_block = 10
snake_speed = 15


font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


events = [
         [(0,1),(0,0)], # right
         [(0,0),(0,0)], # no action
         [(0,0),(0,0)], # no action
         [(0,0),(1,0)], # up
         [(0,0),(0,0)], # no action
         [(1,0),(0,0)], # left
         [(0,0),(0,1)], # down
         [(0,0),(0,0)], # no action
         [(0,0),(0,0)], # no action
         [(0,1),(0,0)], # right
         [(0,0),(0,0)], # no action
         [(0,1),(0,0)], # right
         [(0,0),(0,0)], # no action
         ]


def the_score(score):
    value = score_font.render("Your Score: " + str(score), True, score_c)
    dis.blit(value, [dis_width, dis_height])


def friendly_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake_c, [x[0], x[1], snake_block, snake_block])


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

    apple = [12,13]

    foodx = apple[0]
    foody = apple[1]

    while not game_over:

        while game_close == True:
            dis.fill(back_ground_c)
            message("You Lost! Press ""C"" to Play Again or ""Q"" to quitQuit", msg_c)
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
            left = [(1,0),(0,0)]
            right = [(0,1),(0,0)]
            up = [(0,0),(1,0)]
            down = [(0,0),(0,1)]

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

        dis.fill(back_ground_c)
        pygame.draw.rect(dis, apple_c, [foodx, foody, snake_block, snake_block])

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
            clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
# print(get_state)