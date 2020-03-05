import Towers

import math


class TowerRotation(object):

    def __init__(self):
        self.map_rows = 5
        self.map_columns = 5
        self.shoot = []
        self.rotation = []
        self.shoot = []

    def update(self, rows, columns):
        self.map_rows = rows
        self.map_columns = columns
        self.rotation = [[0 for x in range(self.map_columns)] for y in range(self.map_rows)]
        self.shoot = [[0 for x in range(self.map_columns)] for y in range(self.map_rows)]


    def aim(self, row_width, column_width, bloon_x, bloon_y, new_projectile):
        global rotate
        tower = Towers.return_current_towers()
        number_of_towers = 0


        '''for i in range(len(tower)):
            for j in range(len(tower[i])):
                if tower[i][j] == 0:
                    number_of_towers += 1
        if len(self.rotation) < number_of_towers:
            self.rotation.extend([])'''

        for y in range(len(tower)):
            for x in range(len(tower[y])):
                if tower[y][x] == -1:
                    pass
                else:
                    if tower[y][x] == 0:
                        rotation_speed = 5
                        max_distance = 4 * column_width
                        shoot_speed = 15 # lower is faster
                    elif tower[y][x] == 1:
                        rotation_speed = 8
                        max_distance = 5 * column_width
                        shoot_speed = 7  # lower is faster
                    elif tower[y][x] == 2:
                        rotation_speed = 15
                        max_distance = 8 * column_width
                        shoot_speed = 4  # lower is faster


                    tower_pos_x = column_width*(x+0.5)
                    tower_pos_y = row_width*(y + 0.5)

                    for h in range(len(bloon_x)):
                        bloon_range = math.sqrt((bloon_x[h]-tower_pos_x)**2 + (bloon_y[h]-tower_pos_y)**2)
                        if bloon_range > max_distance:
                            pass
                        else:


                            angle_to_bloon = math.atan2(bloon_x[h]-tower_pos_x, bloon_y[h]-tower_pos_y) * 180/math.pi -90

                            if 0 <= angle_to_bloon and angle_to_bloon <= 90:
                                pass
                            else:
                                angle_to_bloon = 90 + 270 + angle_to_bloon

                            if 180-abs(abs(angle_to_bloon - self.rotation[y][x] % 360)-180) > rotation_speed:
                                self.rotation[y][x] = self.rotation[y][x] + math.copysign(1, math.sin(math.radians(angle_to_bloon-self.rotation[y][x] % 360))) * rotation_speed

                            else:
                                self.rotation[y][x] = self.rotation[y][x] + math.copysign(1, math.sin(math.radians(angle_to_bloon - self.rotation[y][x] % 360))) * (
                                            180 - abs(abs(angle_to_bloon - self.rotation[y][x] % 360) - 180))

                                self.shoot[y][x] += 1
                                if self.shoot[y][x] >= shoot_speed:
                                    new_projectile.new_projectile(tower[y][x], self.rotation[y][x], tower_pos_x, tower_pos_y, column_width)
                                    self.shoot[y][x] = 0


                            break
        rotate = self.rotation


def return_tower_rotation():
    return rotate

