import Save_and_Load
import ast
import Menu_And_Options
import math


class Path(object):

    def __init__(self):
        self.W, self.H = 100, 100
        self.map_len = 0
        self.start_x = 0
        self.start_y = 0
        self.type = []
        self.rotation = []
        self.x_coord = []
        self.y_coord = []
        self.direction = []
        self.row_width = 1
        self.column_width = 1


    def setup(self, name):
        self.W, self.H = 100, 100
        self.map_len = 0
        self.start_x = 0
        self.start_y = 0
        self.type = []
        self.rotation = []
        self.x_coord = []
        self.y_coord = []
        self.direction = []
        self.row_width = 1
        self.column_width = 1
        self.W, self.H = Menu_And_Options.resolution()
        line = Save_and_Load.search(name)
        block_type, block_rotation = Save_and_Load.read_data(line+2)
        block_type = ast.literal_eval(block_type)
        block_rotation = ast.literal_eval(block_rotation)
        rows = len(block_type)
        columns = round((rows + 1) * 16.0 / 9.0 - 1)
        tools_row_width = int((1.0 / 6.0) * self.H)
        tools_col_width = int((1.0 / 11.0) * self.W)
        self.row_width = (self.H - tools_row_width) // rows
        self.column_width = (self.W - tools_col_width) // columns
        row_width = self.row_width
        column_width = self.column_width

        # calculates the lenght of the road. in number of blocks, and position of block in first column
        map_len = 0
        start_y = []
        for i in range(len(block_type)):
            for j in range(len(block_type[i])):
                if block_type[i][j] == 2 or block_type[i][j] == 1:
                    map_len += 1
                    if j == 0:
                        start_y.extend([i])

        self.map_len = map_len

        # find the start block
        for k in range(len(start_y)):
            start_ans = road(block_type[start_y[k]][0], 0, 1, block_rotation[start_y[k]][0], 0, 0, -1, start_y[k], row_width, column_width, 0)
            if start_ans == 0:
                self.start_x = 0
                self.start_y = start_y[k]
                #print('start', self.start_y)

        # build path

        self.type = [block_type[self.start_y][self.start_x]]
        self.rotation = [block_rotation[self.start_y][self.start_x]]
        self.x_coord = [self.start_x]
        self.y_coord = [self.start_y]
        x, y = 0, (self.start_y+0.5)*row_width
        #print('number of road segments',self.map_len)
        for k in range(self.map_len):
            x, y, direction = road(self.type[k], 1, 1, self.rotation[k], x, y, self.x_coord[k], self.y_coord[k], row_width, column_width, 0)
            self.direction.extend([direction])
            #print('type',self.type[k])
            #print('updated position', x, y)
            if k < self.map_len-1:
                if y == self.y_coord[k]*row_width:
                    self.x_coord.extend([self.x_coord[k]])
                    self.y_coord.extend([self.y_coord[k]-1])
                elif y == self.y_coord[k]*row_width + row_width:
                    self.x_coord.extend([self.x_coord[k]])
                    self.y_coord.extend([self.y_coord[k] + 1])
                elif x == self.x_coord[k]*column_width:
                    self.x_coord.extend([self.x_coord[k]-1])
                    self.y_coord.extend([self.y_coord[k]])
                elif x == self.x_coord[k] * column_width + column_width:
                    self.x_coord.extend([self.x_coord[k] + 1])
                    self.y_coord.extend([self.y_coord[k]])
                #print('iteration, starts with 1,  ', k+1, '  end line')
                #print(' ')


                self.type.extend([block_type[self.y_coord[k + 1]][self.x_coord[k + 1]]])
                self.rotation.extend([block_rotation[self.y_coord[k + 1]][self.x_coord[k + 1]]])

        return block_type, block_rotation, rows, columns, self.row_width, self.column_width, tools_row_width, tools_col_width

    def bloon_pos(self, bloon_type, bloon_time, life, level):
        x_pos = []
        y_pos = []
        for i in range(len(bloon_type)):
            if level <= 8:
                t_block = (25 - level*3) + 5
            else:
                t_block = 5
            t_lockal = bloon_time[i] % t_block
            '''if bloon_type[i] == 1:
                t_block = 30
                t_lockal = bloon_time[i] % t_block
            elif bloon_type[i] == 2:
                t_block = 30
                t_lockal = bloon_time[i] % t_block
            elif bloon_type[i] == 3:
                t_block = 30
                t_lockal = bloon_time[i] % t_block
            #else:
             #   continue'''

            k = bloon_time[i] // t_block

            if k+1 > self.map_len:
                bloon_type[i] = -1
                bloon_time[i] = -1

            if bloon_type[i] != -1:
                x_updated, y_updated, derp = road(self.type[k], t_lockal, t_block, self.rotation[k], 0, 0, self.x_coord[k], self.y_coord[k], self.row_width, self.column_width, self.direction[k])
                x_pos.extend([x_updated])
                y_pos.extend([y_updated])
            elif bloon_type[i] == -1:
                x_pos.extend([-1]), y_pos.extend([-1])
                life -= 1
        return bloon_type, bloon_time, x_pos, y_pos, life

def road(block_type, t_local, t_block, rotation, x_enemy, y_enemy, x_block, y_block, row_width, column_width, direction):
    rot = math.radians(rotation)
    x_local = 0
    y_local = 0
    directions = 0

    if x_block == -1:

        if block_type == 1: #turn
            x1, y1 = math.cos(rot), math.sin(rot)
            x2, y2 = math.cos(rot-math.pi/2), math.sin(rot-math.pi/2)
        else:
            x1, y1 = math.cos(rot), math.sin(rot)
            x2, y2 = math.cos(rot-math.pi), math.sin(rot-math.pi)

        if x1 <= -0.9 or x2 <= -0.9:
            return 0
        else:
            return 1
    else:

        if block_type == 1:  # turn
            y_1 = -math.cos(rot)*(- 0.5*row_width) + row_width * y_block + row_width * 0.5
            x_1 = -math.cos(rot-math.pi/2)*(- 0.5*column_width) + column_width * x_block + column_width * 0.5

            y_2 = math.cos(rot+math.pi/2) * (0.5 * row_width) + row_width * y_block + row_width * 0.5
            x_2 = math.cos(rot) * (0.5 * column_width) + column_width * x_block + column_width * 0.5
            #print('yeah ', math.cos(rot-math.pi/2))
            if direction == 0:
                if round(x_1,5) == x_enemy and round(y_1,5) == y_enemy:
                    directions = 1
                elif round(x_2 , 5) == x_enemy and round(y_2,5) == y_enemy:
                    t_local = t_block - t_local
                    directions = 2
                else:
                    print('Error in direction turn', x_1, y_1, x_2, y_2)
                    print('enemy, ', x_enemy, y_enemy)
            else:
                if direction == 1:
                    pass
                elif direction == 2:
                    t_local = t_block - t_local

            if t_local <= 0.5*t_block:
                y_local = -math.cos(rot)*((t_local/t_block*row_width) - 0.5*row_width)
                x_local = -math.cos(rot-math.pi/2)*((t_local/t_block)*column_width - 0.5*column_width)
                #print(-math.cos(rot+math.pi/2))
                #print('local.x', x_local)
            else:
                y_local = math.cos(rot+math.pi/2) * ((t_local / t_block) * row_width - 0.5 * row_width)
                x_local = math.cos(rot) * ((t_local / t_block) * column_width - 0.5 * column_width)
                #print('local.x', x_local)

        elif block_type == 2:  # straight
            y_1 = math.cos(rot - math.pi / 2) * (- 0.5 * row_width) + row_width*y_block + row_width*0.5
            x_1 = math.cos(rot) * (- 0.5 * column_width) + column_width*x_block + column_width*0.5

            y_2 = math.cos(rot - math.pi / 2) * (row_width - 0.5 * row_width) + row_width*y_block + row_width*0.5
            x_2 = math.cos(rot) * (column_width - 0.5 * column_width) + column_width*x_block + column_width*0.5
            if direction == 0:
                if round(x_1,5) == x_enemy and round(y_1,5) == y_enemy:
                    directions = 1
                elif round(x_2,5) == x_enemy and round(y_2,5) == y_enemy:
                    t_local = t_block-t_local
                    directions = 2
                else:
                    print('Error in direction straight', x_1, y_1, x_2, y_2)
                    print('enemy, ', x_enemy, y_enemy)
            else:
                if direction == 1:
                    pass
                elif direction == 2:
                    t_local = t_block - t_local

            y_local = math.cos(rot - math.pi/2) * ((t_local / t_block) * row_width - 0.5 * row_width)
            x_local = math.cos(rot) * ((t_local / t_block) * column_width - 0.5 * column_width)
        #print('local, rot, x, y', math.cos(rot), x_local, y_local)


        x_updated = column_width*x_block + column_width*0.5 + x_local

        y_updated = row_width*y_block + row_width*0.5 + y_local

    return round(x_updated, 5), round(y_updated, 5), directions




