class rectangle:
    def __init__(self, x, y, size_x, size_y):
        self.x, self.y = x, y
        self.left, self.right, self.top, self.bottom = x-size_x, x+size_x, y+size_y, y-size_y

    def check_collide(self, rect):

        if self.left > rect.right:
            return False
        if self.right < rect.left:
            return False
        if self.top < rect.bottom:
            return False
        if self.bottom > rect.top:
            return False
        return True