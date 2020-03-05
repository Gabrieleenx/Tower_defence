import pygame
import Draw
import User_Input
import Save_and_Load
import ast
import Menu_And_Options



def load_im():
    global turn_1, grass_1, road_1, arrow_right, arrow_left
    W, H = Menu_And_Options.resolution()
    pygame.display.set_mode((W, H))  # sets the resolution
    turn_1 = pygame.image.load("Game_assets/Ground/turn1.png").convert()
    grass_1 = pygame.image.load("Game_assets/Ground/grass1.png").convert()
    road_1 = pygame.image.load("Game_assets/Ground/road1.png").convert()
    arrow_right = pygame.image.load("Game_assets/Ground/arrow_right.png").convert()
    arrow_left = pygame.image.load("Game_assets/Ground/arrow_left.png").convert()


def menu(clock, font, window, W, H):
    flag = True
    pygame.display.set_mode((W, H))  # sets the resolution
    map_build = MapBuild(window, W, H,5)
    name = ['a' for x in range(5)]

    Map = 'MAP1'
    save_num = 0


    while flag:
        mouse = User_Input.mouse()
        window.fill((0, 0, 0))

        for i in range(5):
            line = Save_and_Load.search('MAP'+str(i+1))
            name[i] = Save_and_Load.read_name(line+1)

        new_x = W * 0.6
        new_y = H * 0.35

        edit_x = W * 0.6
        edit_y = H * 0.5

        back_x = W * 0.6
        back_y = H * 0.8

        map1_x = W * 0.1
        map1_y = H * 0.35

        Menu_And_Options.menu_box(W * 0.11, H * (0.35 + save_num * 0.1) - H * 0.014, name[save_num])

        if Menu_And_Options.text_box(mouse, map1_x, map1_y, name[0], font):
            Map = 'MAP1'
            save_num = 0
        if Menu_And_Options.text_box(mouse, map1_x, map1_y+0.1*H, name[1], font):
            Map = 'MAP2'
            save_num = 1
        if Menu_And_Options.text_box(mouse, map1_x, map1_y+0.2*H, name[2], font):
            Map = 'MAP3'
            save_num = 2
        if Menu_And_Options.text_box(mouse, map1_x, map1_y+0.3*H, name[3], font):
            Map = 'MAP4'
            save_num = 3
        if Menu_And_Options.text_box(mouse, map1_x, map1_y+0.4*H, name[4], font):
            Map = 'MAP5'
            save_num = 4

        if Menu_And_Options.text_box(mouse, new_x, new_y, 'Create New Map', font):
            map_build.create_new(Map, clock, font)
            map_build.scale_image()
            map_build.create_map(clock, font, W, H)

        if Menu_And_Options.text_box(mouse, edit_x, edit_y, 'Edit Map', font):
            map_build.edit(Map)
            map_build.scale_image()
            while True: #just a delay for mouse click
                mouse = User_Input.mouse()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                if mouse[2] == 0:
                    break

            map_build.create_map(clock, font, W, H)

        if Menu_And_Options.text_box(mouse, back_x, back_y, 'Back', font):
            flag = False
            while mouse[2] == 1:
                mouse = User_Input.mouse()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

        Draw.update_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        clock.tick(60)


class MapBuild(object):

    def __init__(self, window, W, H, rows):
        self.window = window
        self.W = W
        self.H = H
        self.line = 0
        self.choice = 0
        self.rows = rows
        self.tools_row_width = int((1.0/6.0)*H)
        self.tools_col_width = int((1.0/11.0)*W)
        self.columns = round((self.rows+1)*16.0/9.0 - 1)
        self.row_width = (H-self.tools_row_width) // (self.rows)
        self.column_width = (W-self.tools_col_width) // (self.columns)
        self.rotate = [[0 for x in range(self.columns)] for y in range(self.rows)]
        self.type = [[0 for x in range(self.columns)] for y in range(self.rows)]
        self.rotation = 0



    def scale_image(self):
        global road_1_im, road_1_im_r, grass_1_im, grass_1_im_r, turn_1_im_r, turn_1_im, arrow_left_im, arrow_right_im
        global turn_1_tool, turn_1_tool_r, road_1_tool, road_1_tool_r, grass_1_tool, grass_1_tool_r

        turn_1_im = pygame.transform.scale(turn_1, (self.column_width, self.row_width))
        turn_1_im_r = pygame.transform.scale(turn_1, (self.row_width, self.column_width))

        road_1_im = pygame.transform.scale(road_1, (self.column_width, self.row_width))
        road_1_im_r = pygame.transform.scale(road_1, (self.row_width, self.column_width))

        grass_1_im = pygame.transform.scale(grass_1, (self.column_width, self.row_width))
        grass_1_im_r = pygame.transform.scale(grass_1, (self.row_width, self.column_width))

        turn_1_tool = pygame.transform.scale(turn_1, (self.tools_col_width, self.tools_row_width))
        turn_1_tool_r = pygame.transform.scale(turn_1, (self.tools_row_width, self.tools_col_width))

        road_1_tool = pygame.transform.scale(road_1, (self.tools_col_width, self.tools_row_width))
        road_1_tool_r = pygame.transform.scale(road_1, (self.tools_row_width, self.tools_col_width))

        grass_1_tool = pygame.transform.scale(grass_1, (self.tools_col_width, self.tools_row_width))
        grass_1_tool_r = pygame.transform.scale(grass_1, (self.tools_row_width, self.tools_col_width))

        arrow_left_im = pygame.transform.scale(arrow_left, (self.tools_col_width, self.tools_row_width))
        arrow_right_im = pygame.transform.scale(arrow_right, (self.tools_col_width, self.tools_row_width))

    def scale_image_menu(self):
        global road_1_im, road_1_im_r, grass_1_im, grass_1_im_r, turn_1_im_r, turn_1_im, arrow_left_im, arrow_right_im
        self.rows = 5
        self.columns = round((self.rows + 1) * 16.0 / 9.0 - 1)

        self.row_width = self.H // (self.rows)
        self.column_width = self.W // (self.columns)

        turn_1_im = pygame.transform.scale(turn_1, (self.column_width+1, self.row_width+1))
        turn_1_im_r = pygame.transform.scale(turn_1, (self.row_width+1, self.column_width+1))

        road_1_im = pygame.transform.scale(road_1, (self.column_width+1, self.row_width+1))
        road_1_im_r = pygame.transform.scale(road_1, (self.row_width+1, self.column_width+1))

        grass_1_im = pygame.transform.scale(grass_1, (self.column_width+1, self.row_width+1))
        grass_1_im_r = pygame.transform.scale(grass_1, (self.row_width+1, self.column_width+1))

        arrow_left_im = pygame.transform.scale(arrow_left, (self.column_width+1, self.row_width+1))
        arrow_right_im = pygame.transform.scale(arrow_right, (self.column_width+1, self.row_width+1))


    def create_new(self, maps, clock, font):
        flag = True
        while flag:
            mouse = User_Input.mouse()
            self.window.fill((0, 0, 0))

            back_x = self.W * 0.6
            back_y = self.H * 0.8

            num_x = self.W * 0.3
            num_y = self.H * 0.45

            if Menu_And_Options.text_box(mouse, back_x, back_y, 'Apply', font):
                flag = False
                while mouse[2] == 1:
                    mouse = User_Input.mouse()
                    clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()

            self.rows = number_of_rows(self.window, self.H, self.W, mouse, self.rows)
            self.columns = round((self.rows + 1) * 16.0 / 9.0 - 1)
            self.row_width = (self.H - self.tools_row_width) // (self.rows)
            self.column_width = (self.W - self.tools_col_width) // (self.columns)
            self.rotate = [[0 for x in range(self.columns)] for y in range(self.rows)]
            self.type = [[0 for x in range(self.columns)] for y in range(self.rows)]
            Menu_And_Options.text(font, str(self.rows), num_x, num_y)

            Draw.update_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(60)

        self.type = [[0 for x in range(self.columns)] for y in range(self.rows)]
        self.line = Save_and_Load.search(maps)
        Save_and_Load.read_data(self.line+2)


    def edit(self, map):
        self.line = Save_and_Load.search(map)
        self.type, self.rotate = Save_and_Load.read_data(self.line+2)
        self.type = ast.literal_eval(self.type)
        self.rotate = ast.literal_eval(self.rotate)
        self.rows = len(self.type)
        self.columns = round((self.rows + 1) * 16.0 / 9.0 - 1)
        self.row_width = (self.H - self.tools_row_width) // self.rows
        self.column_width = (self.W - self.tools_col_width) // self.columns

    def create_map(self, clock, font, W, H):
        image = None
        flag = True
        while flag:
            mouse = User_Input.mouse()
            self.window.fill((0, 0, 0))
            pos = detect_box(mouse, self.row_width, self.column_width, self.rows, self.columns, self.tools_row_width, self.tools_col_width, self.H, self.W)
            Menu_And_Options.text(font, "Exit", self.column_width*0.01 + self.column_width * self.columns, self.tools_row_width*0.4 + self.tools_row_width * 5)
            Menu_And_Options.text(font, "Save", self.column_width*0.01 + self.column_width * self.columns, self.tools_row_width*0.4 + self.tools_row_width * 4)
            if mouse[2] == 1:
                if pos[1] == 0:
                    if pos[0] == 9:
                        self.rotation -= 90
                    if pos[0] == 8:
                        self.rotation += 90
                    while mouse[2] == 1:
                        clock.tick(60)
                        mouse = User_Input.mouse()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                if pos[0] >= self.columns and pos[0] >= 10:
                    self.choice = pos[1]+1
                    if self.choice == 6:
                        flag = False
                    if self.choice == 5:
                        Save_and_Load.write_data(self.line, str(self.type), str(self.rotate))
                elif pos[1] == 0:
                    pass
                else:
                    self.type[pos[1]-1][pos[0]] = self.choice
                    self.rotate[pos[1]-1][pos[0]] = self.rotation

            if self.choice == 1:
                if self.rotation % 180 == 0:
                    image = turn_1_tool
                else:
                    image = turn_1_tool_r

            elif self.choice == 2:
                if self.rotation % 180 == 0:
                    image = road_1_tool
                else:
                    image = road_1_tool_r
            elif self.choice == 3:
                if self.rotation % 180 == 0:
                    image = grass_1_tool
                else:
                    image = grass_1_tool_r

            if image:
                image_rot = pygame.transform.rotate(image, self.rotation)
                self.window.blit(image_rot, (0, 0))

            if self.type:
                draw_map(self.type, self.rotate, self.window, self.rows, self.columns, self.row_width, self.column_width,  self.tools_row_width)
            self.window.blit(grass_1_tool, (self.column_width * self.columns, self.tools_row_width * 2))
            self.window.blit(road_1_tool, (self.column_width * self.columns, self.tools_row_width * 1))
            self.window.blit(turn_1_tool, (self.column_width * self.columns, self.tools_row_width * 0))
            self.window.blit(arrow_right_im, (self.tools_col_width * 9, self.row_width * 0))
            self.window.blit(arrow_left_im, (self.tools_col_width * 8, self.row_width * 0))

            draw_grid(self.W, self.H, self.rows, self.columns, self.row_width, self.column_width, self.window, self.tools_row_width, self.tools_col_width)
            pygame.draw.line(self.window, (255, 255, 255), (self.column_width * self.columns, 0), (self.column_width * self.columns, H), 5)
            Draw.update_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(60)


def number_of_rows(window, H, W, mouse, number):
    pygame.draw.rect(window, (255, 255, 255), (W * 0.4, H * 0.48, W * 0.4, H * 0.01))

    if W * 0.4 <= mouse[0] <= W * 0.4 + W * 0.4 and H * 0.45 <= mouse[1] <= H * 0.45 + H * 0.07:
        if mouse[2] == 1:
            number = int((mouse[0] / W - 0.4) * 8 / 0.4)+4

    pygame.draw.rect(window, (255, 127, 10), (W * 0.4 * (number-4) // 8 + W * 0.4, H * 0.45, W * 0.01, H * 0.07))
    return number


def draw_grid(W, H, rows, columns, row_width, column_width, window, tool_row, tool_col):

    x = 0
    y = int(0.168*H)

    for l in range(columns):
        x = x + column_width
        pygame.draw.line(window, (255, 255, 255), (x, tool_row), (x, H))

    for l in range(rows):
        y = y + row_width
        pygame.draw.line(window, (255, 255, 255), (0, y), (W-tool_col, y))


def detect_box(mouse, row_width, column_width, rows, columns, menu_row, menu_col, H, W):

    if int(mouse[1]) >= menu_row and int(mouse[0]) <= (W-menu_col):
        pos_x = int(mouse[0] / column_width)
        pos_y = int((mouse[1]-menu_row) / row_width) + 1
    elif int(mouse[0]) <= (W-menu_col):
        pos_x = int(mouse[0] / menu_col)
        pos_y = 0
    else:
        if columns >= 10:
            pos_x = columns + 1
        else:
            pos_x = 10
        pos_y = int((mouse[1]) / menu_row)

    return pos_x, pos_y


def draw_map(type, rotate, window, rows, columns, row_width, column_width, menu_height):

    for i in range(columns):
        for k in range(rows):
            flag = False
            if type[k][i] == 1:
                if rotate[k][i] % 180 == 0:
                    image = turn_1_im
                else:
                    image = turn_1_im_r
                flag = True
            elif type[k][i] == 2:
                if rotate[k][i] % 180 == 0:
                    image = road_1_im
                else:
                    image = road_1_im_r
                flag = True
            elif type[k][i] == 3:
                if rotate[k][i] % 180 == 0:
                    image = grass_1_im
                else:
                    image = grass_1_im_r
                flag = True

            if flag:
                image_rot = pygame.transform.rotate(image, rotate[k][i])
                window.blit(image_rot, (column_width * i, row_width * k + menu_height))

