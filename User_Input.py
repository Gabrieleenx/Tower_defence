import pygame


def mouse():

    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    return pos[0], pos[1], click[0]

class Mouse(object):

    def __init__(self):
        self.click = 0

    def mouser(self):
        clicker = 0
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0] == 0:
            self.click = 0

        if self.click == 0:
            clicker = click[0]
            if clicker == 1:
                self.click = 1

        return pos[0], pos[1], clicker
