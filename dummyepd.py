class EPD:
    def __init__(self):

        self.width = 800
        self.height = 480
        self.BLACK  = 0x000000   #   00  BGR
        self.WHITE  = 0xffffff   #   01
        self.YELLOW = 0x00ffff   #   10
        self.RED    = 0x0000ff   #   11

    def init(self):
        pass

    def Clear(self):
        pass

    def draw(self, *arg):
        pass

    def display(self, *arg):
        pass

    def getbuffer(self, *arg):
        pass

    def sleep(self):
        pass