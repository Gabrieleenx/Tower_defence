# Import images...
import pygame
import Menu_And_Options
import Towers
import Aim
import math

def load_im():
    global window, tower_1, tower_2, tower_3, backdrop, bloon_1, bloon_2, bloon_3, projectile
    W, H = Menu_And_Options.resolution()
    pygame.display.set_mode((W, H))  # sets the resolution
    tower_1 = pygame.image.load("Game_assets/Towers/tower1.png").convert_alpha()
    tower_2 = pygame.image.load("Game_assets/Towers/tower2.png").convert_alpha()
    tower_3 = pygame.image.load("Game_assets/Towers/tower3.png").convert_alpha()
    bloon_1 = pygame.image.load("Game_assets/Bloons/bloon1.png").convert_alpha()
    bloon_2 = pygame.image.load("Game_assets/Bloons/bloon2.png").convert_alpha()
    bloon_3 = pygame.image.load("Game_assets/Bloons/bloon3.png").convert_alpha()
    projectile = pygame.image.load("Game_assets/Towers/bullet.png").convert_alpha()
    backdrop = pygame.image.load("Game_assets/Ground/background.png").convert()
    window = pygame.display.set_mode((W, H))  # sets the resolution


def scale_image_menu(W, H):
    global tower_1_menu, tower_2_menu, tower_3_menu, backdrop_menu
    rows = 5
    columns = round((rows + 1) * 16.0 / 9.0 - 1)

    row_width = H // rows
    column_width = W // columns

    tower_1_menu = pygame.transform.scale(tower_1, (column_width-5, row_width-8))
    tower_2_menu = pygame.transform.scale(tower_2, (column_width-5, row_width-8))
    tower_3_menu = pygame.transform.scale(tower_3, (column_width-5, row_width-8))
    backdrop_menu = pygame.transform.scale(backdrop, (W, H))



def scale_image(row_width, column_width):
    global tower_1_im, tower_2_im, tower_3_im, bloon_1_im, bloon_2_im, bloon_3_im, projectile_im
    tower_1_im = pygame.transform.scale(tower_1, (column_width + 1, row_width + 1))
    tower_2_im = pygame.transform.scale(tower_2, (column_width + 1, row_width + 1))
    tower_3_im = pygame.transform.scale(tower_3, (column_width + 1, row_width + 1))
    projectile_im = pygame.transform.scale(projectile, (column_width //8, row_width //8))

    bloon_1_im = pygame.transform.scale(bloon_1, (column_width , row_width ))
    bloon_2_im = pygame.transform.scale(bloon_2, (column_width , row_width ))
    bloon_3_im = pygame.transform.scale(bloon_3, (column_width , row_width ))



def towers_menu(column_width, columns, tools_row_width, tower_selected):
    #window.fill((0, 0, 0))

    window.blit(tower_1_menu, (column_width * columns, tools_row_width * 0))
    window.blit(tower_2_menu, (column_width * columns, tools_row_width * 1))
    window.blit(tower_3_menu, (column_width * columns, tools_row_width * 2))
    if tower_selected == 0:
        image = tower_1_menu
    elif tower_selected == 1:
        image = tower_2_menu
    elif tower_selected == 2:
        image = tower_3_menu
    window.blit(image, (0, 0))


def draw_towers(rows, row_width, column_width, menu_height):

    towers = Towers.return_current_towers()
    rotate = Aim.return_tower_rotation()

    for k in range(len(towers)):
        for i in range(round((rows + 1) * 16.0 / 9.0 - 1)):
            flag = False
            if towers[k][i] == 0:

                image = tower_1_im
                flag = True

            if towers[k][i] == 1:

                image = tower_2_im
                flag = True

            if towers[k][i] == 2:

                image = tower_3_im
                flag = True


            if flag:
                image = pygame.transform.rotate(image, rotate[k][i])

                alpha = abs(rotate[k][i]) % 90

                beta = abs(rotate[k][i]) % 180

                gamma = math.copysign(1, rotate[k][i])

                if gamma == 1:
                    pass
                if gamma == -1:
                    alpha = 90 - alpha
                    beta = 180 - beta

                if beta < 90:
                    top_length = column_width
                    side_length = row_width
                else:
                    top_length = row_width
                    side_length = column_width

                alpha_r = math.radians(alpha)

                y_new = top_length*math.sin(alpha_r) + (math.cos(alpha_r)*side_length - math.sin(alpha_r)*top_length)/2
                x_new = (math.sin(alpha_r)*side_length + math.cos(alpha_r)*top_length)/2
                dy = round(y_new - side_length/2)
                dx = round(x_new - top_length/2)



                window.blit(image, (column_width * i - dx, row_width * k + menu_height - dy))

def draw_background():
    window.blit(backdrop_menu, (0, 0))



def draw_bloons(bloon_type, bloon_x, bloon_y, tool_row_widht, col_width):
    for t in range(len(bloon_type)):
        if bloon_type[t] == 1:
            image = bloon_1_im
        elif bloon_type[t] == 2:
            image = bloon_2_im
        elif bloon_type[t] == 3:
            image = bloon_3_im

        window.blit(image, (bloon_x[t]-col_width//2, bloon_y[t]+tool_row_widht-col_width//2))


def text(font, message, x, y):
    white = (255, 255, 255)
    text_start = font.render(message, 1, white)
    window.blit(text_start, (x, y))

def draw_projectile(pos_x, pos_y, menu_heigth, col_width):
    for t in range(len(pos_x)):
        window.blit(projectile_im, (pos_x[t]-col_width//16, pos_y[t] + menu_heigth-col_width//16))


def update_window():
    pygame.display.update()



