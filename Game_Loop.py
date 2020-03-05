import pygame
import Menu_And_Options
import Map_And_Path
import Draw
import Bloons
import Map_Makeing
import User_Input
import Towers
import Aim
import Colission

def main():

    clock = pygame.time.Clock()         # creates a instance that keeps track of time
    pygame.font.init()                   # enables text in pygame

    game = True         # keeps the gameloop going
    menu_flag = True
    select_flag = False
    calc_path_flag = False
    game_running = False

    Tower = Towers.Tower()
    aim = Aim.TowerRotation()
    collison = Colission.Collision()

    game_speed = 30
    path = Map_And_Path.Path()


    mouse_obj = User_Input.Mouse()

    while game:


        if menu_flag:
            Menu_And_Options.menu(clock)
            select_flag = True
            menu_flag = False


        # chose map

        if select_flag:
            map_choice, back, map_name = Menu_And_Options.start_map_selection(clock)
            select_flag = False
            if back == 1:
                menu_flag = True
            else:
                calc_path_flag = True
            W, H = Menu_And_Options.resolution()
            window = pygame.display.set_mode((W, H))  # sets the resolution
       # window.fill((0, 0, 0))
        # calculate path
        if calc_path_flag:
            type_, rotate, rows, columns, row_width, column_width, menu_height, menu_width = path.setup(map_name)
            bloon = Bloons.Bloons(path)
            calc_path_flag = False
            Map = Map_Makeing.MapBuild(window, W, H, rows)
            game_running = True
            Map_Makeing.load_im()
            Map.edit(map_name)
            Map.scale_image()

            Draw.load_im()
            Draw.scale_image_menu(W, H)
            Draw.scale_image(row_width, column_width)
            Tower.update(rows, columns, row_width, column_width)
            aim.update(rows, columns)

            bloon_type = []
            bloon_time = []

            score = 0
            money = 150
            life = 3
            level_score = 20
            levels = 0
            level_hold = True
            level = 0
            levelq = 0
            font = pygame.font.SysFont(None, int(W / 25))
            tower_selected = 0

        if game_running:
            Draw.draw_background()
            levelq = (score+levelq*level_score) // level_score

            if levelq > levels:
                if level_score < 260:
                    level_score += int(level_score*0.9)
                else:
                    level_score += 200

                levels = levelq
                level_hold = False
                #print('levelscore', level_score)
            if len(bloon_type) == 0:
                level_hold = True
                level = levelq
                life = 3

           # if level > current_level:






            if life <= 0:
                game_running = False
                menu_flag = True
            mouse = mouse_obj.mouser()
            mouse_x, mouse_y = Map_Makeing.detect_box(mouse, row_width, column_width, rows, columns, menu_height,
                                                      menu_width, H, W)
            Map_Makeing.draw_map(type_, rotate, window, rows, columns, row_width, column_width, menu_height)


            # game
            life = bloon.update(bloon_type, bloon_time, life, level, level_hold)

            pos_x, pos_y, bloon_type, bloon_time = bloon.bloon_return()

            bloon_type, bloon_time, pos_x, pos_y = remove_bloon(bloon_type, bloon_time, pos_x, pos_y, -1)



            if mouse[2] == 1:
                money, tower_selected = Tower.tower_selection(mouse_x, mouse_y, type_, money)
            Draw.towers_menu(column_width, columns, menu_height, tower_selected)
            aim.aim(row_width, column_width, pos_x, pos_y, collison)

            Draw.draw_towers(rows, row_width, column_width, menu_height)

            collison.update_position(column_width, menu_height, menu_width, W, H, window)


            bloon_type, bloon_time, pos_x, pos_y, score, money = collison.check_collision(bloon_type, bloon_time, pos_x, pos_y, column_width, score, money)



            bloon_type, bloon_time, pos_x, pos_y = remove_bloon(bloon_type, bloon_time, pos_x, pos_y, -2)


            #print(clock.get_fps())
            Draw.draw_bloons(bloon_type, pos_x, pos_y, menu_height, column_width)
            #for t in range(len(pos_x)):
                #pygame.draw.rect(window, (255, 255, 255), (pos_x[t]-W*0.025, pos_y[t]+menu_height-H*0.025, W * 0.05, H * 0.05))

            Draw.text(font, 'Money '+ str(money), W*0.7, H*0.09)
            Draw.text(font, 'Score '+ str(score), W*0.7, H*0.02)
            Draw.text(font, 'Level '+ str(level), W*0.5, H*0.02)
            Draw.text(font, 'Life '+ str(life), W*0.5, H*0.09)
            Draw.text(font, '50', W*0.92, H*0.15)
            Draw.text(font, '450', W*0.92, H*0.3)
            Draw.text(font, '1250', W*0.92, H*0.5)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        Draw.update_window()
        clock.tick(game_speed)      # sets the fps



def remove_bloon(type_, time, pos_x, pos_y, rem):
    type_ = [value for value in type_ if value != rem]
    time = [value for value in time if value != rem]
    pos_x = [value for value in pos_x if value != rem]
    pos_y = [value for value in pos_y if value != rem]

    return type_, time, pos_x, pos_y


main()