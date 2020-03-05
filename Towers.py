
class Tower(object):

    def __init__(self):
        self.choice = 0
        self.placed_towers = []
        self.map_rows = 5
        self.map_columns = 10
        self.map_row_width = 10
        self.map_col_width = 10

    def update(self, rows, columns, row_width, col_width):
        global towers
        self.map_rows = rows
        self.map_columns = columns
        self.map_row_width = row_width
        self.map_col_width = col_width
        self.placed_towers = [[-1 for x in range(self.map_columns)] for y in range(self.map_rows)]
        towers = self.placed_towers

    def tower_selection(self, mouse_x, mouse_y, map_type, money):
        global towers
        if mouse_x >= self.map_columns and mouse_x >= 10:
            if mouse_y <= 2:
                self.choice = mouse_y
        elif mouse_y == 0:
            pass
        elif map_type[mouse_y-1][mouse_x] != 3:
            pass
        else:
            if money >= 50*(self.choice*2+1)**2:
                self.placed_towers[mouse_y - 1][mouse_x] = self.choice
                money -= 50*(self.choice*2+1)**2
            else:
                pass
        towers = self.placed_towers

        return money, self.choice


def return_current_towers():
    return towers

