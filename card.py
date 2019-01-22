class Card:
    # makes a new card consisting of a suit and value
    # 1 is Ace, 11 is Jack, 12 is Queen, 13 is King
    # this makes comparisons between cards easy
    # a value of -1 is used to represent an empty space
    def __init__(self, value, suit, color, face_up):
        self.value = value;
        self.suit = suit;
        self.color = color;
        self.face_up = face_up;

    # gets a string representation of the card
    def get_str(self):
        if self.value == 1:
            return 'A' + self.suit;
        elif self.value == 11:
            return 'J' + self.suit;
        elif self.value == 12:
            return 'Q' + self.suit;
        elif self.value == 13:
            return 'K' + self.suit;
        else:
            return str(self.value) + self.suit;

    # prints out the card
    def print(self):
       print(self.get_str())

    # flips a card over
    def flip(self):
        self.face_up = not self.face_up;
