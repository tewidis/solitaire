from card import Card
from deck import Deck

def main():
    deck = Deck();

    deck.shuffle();

    board = Board(deck);

    board.print();

    print('Valid moves:');

    print(board.get_valid_moves());

class Board:
    # creates a solitare board
    def __init__(self, deck):
        self.talon_idx = 0;
        self.pile = [];
        self.suit_stacks = [[], [], [], []];
        self.build_stacks = [[], [], [], [], [], [], []];
        for i in range (0,7):
            for j in range(0,i+1):
                next_card = deck.get_next();
                if j == i:
                    next_card.flip();
                self.build_stacks[i].append(next_card);

        for i in range(0,24):
            self.pile.append(deck.get_next());

        self.suit_stacks[0].append(Card(-1, 'C', '', True));
        self.suit_stacks[1].append(Card(-1, 'D', '', True));
        self.suit_stacks[2].append(Card(-1, 'H', '', True));
        self.suit_stacks[3].append(Card(-1, 'S', '', True));

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
                    if not self.build_stacks[j][i].face_up:
                        append_str = '--';
                    else:
                        append_str = self.build_stacks[j][i].get_str();
                    if len(self.build_stacks[j][i].get_str()) == 2:
                        build_str = build_str + append_str + '  ';
                    else:
                        build_str = build_str + append_str + ' ';
            print(build_str);

        print('Talon:');
        self.pile[self.talon_idx].print();

        print('Suit stacks:');
        suit_str = '';
        for i in range(len(self.suit_stacks)):
            if self.suit_stacks[i][-1].value == -1:
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

    # increments the talon pointer to get the next card
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
            # if card1 is an ace and card2 is empty and same suit, it's valid
            # the same suit is a trick to reduce the move search space for Aces
            elif card1.value == 1 and card2.value == -1 and card1.suit == card2.suit:
                return True;
            else:
                return False;

    # analyzes all possible moves and returns a list of all valid moves
    def get_valid_moves(self):
        valid_moves = [];
        # look at the cards in the build stacks
        for i in range(len(self.build_stacks)):
            for j in range(len(self.build_stacks[i])):
                if self.build_stacks[i][j].face_up:
                    card1 = self.build_stacks[i][j];
                    # see if the card can be played on any of the build stacks
                    for j in range(len(self.build_stacks)):
                        if i != j:
                            card2 = self.build_stacks[j][-1];
                            if self.is_valid_move(card1, card2, 'build'):
                                valid_moves.append(card1.get_str() + '->' + card2.get_str());

            # see if the card can be played on any of the suit stacks
            for j in range(len(self.suit_stacks)):
                card2 = self.suit_stacks[j][-1];
                if self.is_valid_move(card1, card2, 'suit'):
                    valid_moves.append(card1.get_str() + '->' + card2.get_str());

        # look at the card in the talon
        card1 = self.pile[self.talon_idx];
        for i in range(len(self.build_stacks)):
            card2 = self.build_stacks[j][-1];
            if self.is_valid_move(card1, card2, 'build'):
                valid_moves.append(card1.get_str() + '->' + card2.get_str());

        for j in range(len(self.suit_stacks)):
            card2 = self.suit_stacks[j][-1];
            if self.is_valid_move(card1, card2, 'suit'):
                valid_moves.append(card1.get_str() + '->' + card2.get_str());

        # you can always flip a card from the pile to the talon
        next_talon_idx = self.talon_idx + 1 % len(self.pile);
        valid_moves.append('(' + self.pile[self.talon_idx].get_str() + '->' + self.pile[next_talon_idx].get_str() + ')');

        return valid_moves;

if __name__ == "__main__":
    main()
