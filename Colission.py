import math
import Draw
import pygame



class Collision():
    def __init__(self):
        self.projectile_type = []
        self.projectile_direction = []
        self.projectile_pos_x = []
        self.projectile_pos_y = []
        self.bloon_damage = []

    def new_projectile(self, tower_type, tower_angle, tower_pos_x, tower_pos_y, column_width):
        tower_size = 0.45*column_width
        self.projectile_type.extend([tower_type])
        self.projectile_direction.extend([tower_angle])
        tower_angle_r = math.radians(tower_angle)
        self.projectile_pos_x.extend([tower_pos_x+math.cos(tower_angle_r)*tower_size])
        self.projectile_pos_y.extend([tower_pos_y-math.sin(tower_angle_r)*tower_size])


    def update_position(self, column_width, menu_height, menu_width, W, H, window):
        for i in range(len(self.projectile_type)):
            if self.projectile_type[i] == -1:
                continue
            tower_angle_r = math.radians(self.projectile_direction[i])
            if self.projectile_type[i] == 0:
                projectile_speed = column_width/10

            if self.projectile_type[i] == 1:
                projectile_speed = column_width/8

            if self.projectile_type[i] == 2:
                projectile_speed = column_width/5
            self.projectile_pos_x[i] = self.projectile_pos_x[i] + math.cos(tower_angle_r)*projectile_speed
            self.projectile_pos_y[i] = self.projectile_pos_y[i] - math.sin(tower_angle_r)*projectile_speed

            if self.projectile_pos_x[i] < 0 or self.projectile_pos_y[i] < 0 or self.projectile_pos_x[i] > W-menu_width or self.projectile_pos_y[i] > H-menu_height:
                self.projectile_type[i] = -1
                self.projectile_direction[i] = -1
                self.projectile_pos_y[i] = -1
                self.projectile_pos_x[i] = -1
        self.projectile_type, self.projectile_direction, self.projectile_pos_x, self.projectile_pos_y = remove_bloon(self.projectile_type, self.projectile_direction, self.projectile_pos_x, self.projectile_pos_y, -1)

        Draw.draw_projectile(self.projectile_pos_x, self.projectile_pos_y, menu_height, column_width)
        #for t in range(len(self.projectile_pos_x)):
         #   pygame.draw.rect(window, (255, 255, 255),(self.projectile_pos_x[t] - W * 0.005, self.projectile_pos_y[t] + menu_height - H * 0.005, W * 0.01, H * 0.01))

    def check_collision(self, bloon_type, bloon_time, bloon_pos_x, bloon_pos_y, column_width, score, money):
        if len(self.bloon_damage) < len(bloon_type):
            if bloon_type[-1] == 1:
                self.bloon_damage.extend([1])
            elif bloon_type[-1] == 2:
                self.bloon_damage.extend([7])
            elif bloon_type[-1] == 3:
                self.bloon_damage.extend([15])

        hit_box = 0.2 * column_width


        for i in range(len(bloon_type)):
            for x in range(len(self.projectile_type)):
                if len(bloon_type) != len(bloon_pos_x) or len(bloon_type) != len(bloon_pos_y):
                    print('len diffrence in bloon')
                    print(bloon_type, len(bloon_type))
                    print(bloon_time, len(bloon_time))
                    print(bloon_pos_x, len(bloon_pos_x))
                    print(bloon_pos_y, len(bloon_pos_y))
                if len(self.projectile_type) != len(self.projectile_pos_x) or len(self.projectile_type) != len(self.projectile_pos_x):
                    print('len diffrence in projectile')



                if bloon_pos_x[i]-hit_box < self.projectile_pos_x[x] < bloon_pos_x[i] + hit_box and bloon_pos_y[i]-hit_box < self.projectile_pos_y[x] < bloon_pos_y[i] + hit_box:
                    self.bloon_damage[i] -= 1
                    if self.bloon_damage[i] <= 0:
                        bloon_type[i] = -2
                        bloon_time[i] = -2
                        bloon_pos_x[i] = -2
                        bloon_pos_y[i] = -2
                        self.bloon_damage[i] = -2
                        score += 1
                        money += 5

                    self.projectile_type[x] = -1
                    self.projectile_direction[x] = -1
                    self.projectile_pos_y[x] = -1
                    self.projectile_pos_x[x] = -1

        self.projectile_type, self.projectile_direction, self.projectile_pos_x, self.projectile_pos_y = remove_bloon(self.projectile_type, self.projectile_direction, self.projectile_pos_x, self.projectile_pos_y, -1)
        self.bloon_damage, e, r, t = remove_bloon(self.bloon_damage, [0], [0], [0],-2)
        '''try:
            self.bloon_damage.remove(-2)
        except:
            pass'''

        return bloon_type, bloon_time, bloon_pos_x, bloon_pos_y, score, money

def remove_bloon(type_, time, pos_x, pos_y, rem):
    type_ = [value for value in type_ if value != rem]
    time = [value for value in time if value != rem]
    pos_x = [value for value in pos_x if value != rem]
    pos_y = [value for value in pos_y if value != rem]

    return type_, time, pos_x, pos_y