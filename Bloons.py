import random
import Map_And_Path
import pygame

class Bloons(object):

    def __init__(self, path):
        self.path = path
        self.bloon_type = []
        self.bloon_time = []
        self.bloon_pos_x = []
        self.bloon_pos_y = []
        self.bloon_counter_1 = 0
        self.level = 50
        self.random_1 = 50

    def update(self, bloon_type, bloon_time, life, level, level_hold):
        self.level = int(1 + 100 / (level**1.1 +1))
        self.random_1 = int(1+ 100 / (level*2+1))
        #print(self.level)
        self.bloon_type = bloon_type
        self.bloon_time = bloon_time
        if level_hold:

            self.bloon_counter_1 += 1

            if self.bloon_counter_1 >= self.random_1:
                self.bloon_type.extend([random.randint(1, 3)])
                self.bloon_time.extend([0])
                self.bloon_counter_1 = 0
                self.random_1 = random.randint(self.level, self.level + 50)

        self.bloon_time = [x + 1 for x in self.bloon_time]

        self.bloon_type, self.bloon_time, self.bloon_pos_x, self.bloon_pos_y, life = self.path.bloon_pos(self.bloon_type, self.bloon_time, life, level)

        return life

    def bloon_return(self):
        return self.bloon_pos_x, self.bloon_pos_y, self.bloon_type, self.bloon_time
