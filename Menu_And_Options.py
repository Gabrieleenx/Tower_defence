import pygame
import Draw
import User_Input
import Map_Makeing
import ast
import Save_and_Load

def menu(clock):
    global window, W, H, menu_opt
    menu_flag = True
    resolution_set = True
    menu_opt = Options()
    pygame.font.init()

    while menu_flag:

        if resolution_set:
            W, H = menu_opt.resolution()# screen resolution
            window = pygame.display.set_mode((W, H))  # sets the resolution
            Map_Makeing.load_im()
            font = pygame.font.SysFont(None, W//18)
            Map = Map_Makeing.MapBuild(window, W, H, 5)

            start_x = W * 0.6
            start_y = H * 0.35

            mapmake_x = W * 0.6
            mapmake_y = H * 0.5

            options_x = W * 0.6
            options_y = H * 0.65

            quit_x = W * 0.6
            quit_y = H * 0.8

            resolution_set = False

        window.fill((0, 0, 0))

        line = Save_and_Load.search("BACKGROUND:")
        types, rotate = Save_and_Load.read_data(line+1)
        types = ast.literal_eval(types)
        rotate = ast.literal_eval(rotate)

        Map.scale_image_menu()
        Map_Makeing.draw_map(types, rotate, window, 5, 10,  H // 5, W // 10, 0)

        mouse = User_Input.mouse()

        if text_box(mouse, start_x, start_y, 'Start', font):
            menu_flag = False

        if text_box(mouse, mapmake_x, mapmake_y, 'Create Map', font):
            while mouse[2] == 1:
                mouse = User_Input.mouse()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

            Map_Makeing.menu(clock, font, window, W, H)

        if text_box(mouse, options_x, options_y, 'Options', font):
            menu_opt.options(clock, font, window)
            resolution_set = True

        if text_box(mouse, quit_x, quit_y, 'Quit', font):
            pygame.quit()

        #text(font, 'Start', start_x, start_y)
        #text(font, 'Create Map', mapmake_x, mapmake_y)
        #text(font, 'Options', options_x, options_y)
        #text(font, 'Quit', quit_x, quit_y)

        Draw.update_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        clock.tick(60)


def menu_box(pos_x, pos_y, msg):
    global W, H

    box_length = W*0.02 + W*len(msg)*0.026
    box_height = H*0.1
    s = pygame.Surface((box_length, box_height), pygame.SRCALPHA)
    s.fill((100, 100, 100, 128))
    window.blit(s, (pos_x, pos_y))


def text(font, message, x, y):
    white = (255, 255, 255)
    text_start = font.render(message, 1, white)
    window.blit(text_start, (x, y))


class Options(object):
    global W, H

    def __init__(self):
        self.height = 720
        self.width = 1280
        self.volume = 100

    def resolution(self):

        return self.width, self.height

    def sound(self):
        return self.volume

    def options(self, clock, font, window):
        flag = True

        while flag:
            mouse = User_Input.mouse()
            window.fill((0, 0, 0))

            resolution_x = W*0.1
            resolution_y = H*0.3

            res_480_x = W*0.4
            res_480_y = H*0.3

            res_720_x = W*0.55
            res_720_y = H*0.3

            res_1080_x = W*0.7
            res_1080_y = H*0.3

            sound_x = W*0.1
            sound_y = H*0.45

            back_x = W*0.1
            back_y = H*0.6

            if text_box(mouse, back_x, back_y, 'Back and Apply', font):
                flag = False

            if text_box(mouse, res_480_x, res_480_y, '480', font):
                self.height = 480
                self.width = 848
            if text_box(mouse, res_720_x, res_720_y, '720', font):
                self.height = 720
                self.width = 1280
            if text_box(mouse, res_1080_x, res_1080_y, '1080', font):
                self.height = 1080
                self.width = 1920

            text(font, 'Resolution', resolution_x, resolution_y)
            text(font, 'Sound', sound_x, sound_y)

            if self.height == 480:
                menu_box(res_480_x - W * 0.01, res_480_y - H * 0.014, '480')
            elif self.height == 720:
                menu_box(res_720_x - W * 0.01, res_720_y - H * 0.014, '720')
            elif self.height == 1080:
                menu_box(res_1080_x - W * 0.01, res_1080_y - H * 0.014, '1080')


            pygame.draw.rect(window, (255, 255, 255), (W*0.4, H*0.48, W*0.4, H*0.01))

            if W*0.4 <= mouse[0] <= W*0.4 + W*0.4 and H*0.45 <= mouse[1] <= H*0.45 + H*0.07:
                if mouse[2] == 1:
                    self.volume = int((mouse[0]/W - 0.4)*100/0.4)

            pygame.draw.rect(window, (255, 127, 10), (W * 0.4*self.volume//100 + W*0.4, H * 0.45, W * 0.01, H * 0.07))

            Draw.update_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(60)


def start_map_selection(clock):
    global window, W, H
    flag = True
    map_choice = 0
    Map = 'MAP1'
    back = 0
    font = pygame.font.SysFont(None, W // 18)
    mousei = User_Input.Mouse()
    while flag:
        mouse = mousei.mouser()
        window.fill((0, 0, 0))
        name = ['a' for x in range(5)]
        for i in range(5):
            line = Save_and_Load.search('MAP'+str(i+1))
            name[i] = Save_and_Load.read_name(line+1)

        map1_x = W * 0.1
        map1_y = H * 0.35

        menu_box(W * 0.11, H * (0.35 + map_choice * 0.1) - H * 0.014, name[map_choice])
        clock.tick(60)
        if text_box(mouse, map1_x, map1_y, name[0], font):
            map_choice = 0
            Map = 'MAP1'
        if text_box(mouse, map1_x, map1_y + 0.1 * H, name[1], font):
            map_choice = 1
            Map = 'MAP2'
        if text_box(mouse, map1_x, map1_y + 0.2 * H, name[2], font):
            map_choice = 2
            Map = 'MAP3'
        if text_box(mouse, map1_x, map1_y + 0.3 * H, name[3], font):
            map_choice = 3
            Map = 'MAP4'
        if text_box(mouse, map1_x, map1_y + 0.4 * H, name[4], font):
            map_choice = 4
            Map = 'MAP5'

        if text_box(mouse, map1_x+0.6*W, map1_y + 0.4 * H, 'Go', font):
            flag = False

        if text_box(mouse, map1_x+0.7*W, map1_y + 0.4 * H, 'Back', font):
            back = 1
            flag = False

        Draw.update_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    return map_choice, back, Map


def text_box(mouse, x, y, msg, font):
    global W, H
    if x <= mouse[0] <= x + W * len(msg) * 0.025 and y <= mouse[1] <= y + H * 0.08:
        menu_box(x - W * 0.01, y - H * 0.014, msg)
        text(font, msg, x, y)
        if mouse[2] == 1:
            return True
        else:
            return False
    text(font, msg, x, y)


class OnScreenText:
    pass

def resolution():
    global menu_opt
    return menu_opt.resolution()


def sound():
    global menu_opt
    return menu_opt.sound()





