def main():
    deck = Deck();

    deck.shuffle();

    board = Board(deck);

    board.print();

    test_is_valid_move(board);

class Board:
    # creates a solitare board
    def __init__(self, deck):
        self.talon_idx = 0;
        self.pile = [];
        self.suit_stacks = [[], [], [], []];
        self.build_stacks = [[], [], [], [], [], [], []];
        for i in range (0,7):
            for j in range(0,i+1):
                self.build_stacks[i].append(deck.get_next());

        for i in range(0,24):
            self.pile.append(deck.get_next());

    # prints out the board
    def print(self):
        max_len = 0;
        for i in range(0, len(self.build_stacks)):
            if len(self.build_stacks[i]) > max_len:
                max_len = len(self.build_stacks[i]);

        print('Build stacks:')
        for i in range(0, max_len):
            build_str = '';
            for j in range(len(self.build_stacks)):
                if i >= len(self.build_stacks[j]):
                    build_str = build_str + '    ';
                else:
                    if len(self.build_stacks[j][i].get_str()) == 2:
                        build_str = build_str + self.build_stacks[j][i].get_str() + '  ';
                    else:
                        build_str = build_str + self.build_stacks[j][i].get_str() + ' ';
            print(build_str);

        print('Talon:');
        self.pile[self.talon_idx].print();

        print('Suit stacks:');
        suit_str = '';
        for i in range(len(self.suit_stacks)):
            if len(self.suit_stacks[i]) == 0:
                suit_str = suit_str + '[ ]';
            else:
                suit_str = suit_str + self.suit_stacks[i].get_str();
        print(suit_str);

        print('Pile:')
        pile_str = '';
        if len(self.pile) == 0:
            print('[ ]');
        else:
            for i in range(len(self.pile)):
                pile_str = pile_str + self.pile[i].get_str() + ' ';
        print(pile_str);

    def flip_card_from_pile(self):
        self.talon_idx = (self.talon_idx + 1) % len(self.pile);

    # this tests if playing card1 on card2 is a valid move
    def is_valid_move(self, card1, card2, dest):
        # are we playing it on a build_stack or suit_stack?
        if dest == 'build':
            # this is the general case
            if card1.color != card2.color and card1.value == card2.value - 1:
                return True;
            # if card1 is a king and card2 is empty, it's valid
            elif card1.value == 13 and card2.value == -1:
                return True;
            else:
                return False;
        elif dest == 'suit':
            # general case
            if card1.suit == card2.suit and card1.value == card2.value + 1:
                return True;
            # if card1 is an ace and card2 is empty, it's valid
            elif card1.value == 1 and card2.value == -1:
                return True;
            else:
                return False;

class Deck:
    # makes a new deck of cards
    # the deck will be in order until shuffled
    def __init__(self):
        self.list = [];
        self.idx = -1;
        suits = ['C', 'D', 'H', 'S'];
        for i in suits:
            for j in range(1,14):
                if i == 'C' or i == 'S':
                    self.list.append(Card(j, i, 'Black'));
                elif i == 'D' or i == 'H':
                    self.list.append(Card(j, i, 'Red'));

    # prints out the deck
    def print(self):
        for i in self.list:
           i.print();

    # shuffles the deck randomly
    def shuffle(self):
        from random import shuffle;
        shuffle(self.list);

    # returns the next card from the top of the deck
    def get_next(self):
        if self.idx > len(self.list):
            print('Exceeded end of deck');
            return;

        self.idx = self.idx + 1;
        return self.list[self.idx];

class Card:
    # makes a new card consisting of a suit and value
    # 1 is Ace, 11 is Jack, 12 is Queen, 13 is King
    # this makes comparisons between cards easy
    # a value of -1 is used to represent an empty space
    def __init__(self, value, suit, color):
        self.value = value;
        self.suit = suit;
        self.color = color;

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

if __name__ == "__main__":
    main()
