class Move:
    # contains all of the information required to make a move
    # x1, y1 specify the position on the board of the source card
    # x2, y2 specify the position on the board of the destination card
    # src indicates the card is coming from a build stack, suit stack, or talon
    # dest indicates whether the card is going to a build_ stack or suit stack
    def __init__(self, x1, y1, x2, y2, src, dest):
        self.x1 = x1;
        self.y1 = y1;
        self.x2 = x2;
        self.y2 = y2;
        self.src = src;
        self.dest = dest;

    def print(self):
        print('(' + str(self.x1) + ',' + str(self.y1) + ') -> (' + str(self.x2) + ',' + str(self.y2) + ') ' + self.src + ' ' + self.dest);
