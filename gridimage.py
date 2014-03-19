import constants

class GridImage():

    def __init__(self, pos, surface, value):
        self.pos = pos
        self.surface = surface
        self.value = value

    def check_click(self, click_pos):
        if (self.pos[0] * constants.IMAGE_SIZE
            <= click_pos[0] <
            self.pos[0] * constants.IMAGE_SIZE + constants.IMAGE_SIZE and
            self.pos[1] * constants.IMAGE_SIZE <=
            click_pos[1] <
            self.pos[1] * constants.IMAGE_SIZE + constants.IMAGE_SIZE):
            return True
        else:
            return False

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "<GridImage pos={0}, val={1}>".format(self.pos, self.value)
