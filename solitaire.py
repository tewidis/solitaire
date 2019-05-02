from card import Card
from deck import Deck
from move import Move

def main():
    deck = Deck();

    # un-winnable games aren't very useful to a solver
    deck.make_winnable(); # deck.shuffle(); might not produce a winnable game.

    board = Board(deck);

    board.print();

    print('Valid moves:');

    valid_moves = board.get_valid_moves();

    board.make_move(valid_moves[0]);

    board.print();

    print(board.get_score());

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
                        build_str = build_str + append_str + '  ';
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
                suit_str = suit_str + self.suit_stacks[i][-1].get_str();
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

    # analyzes all possible moves, prints the valid ones, and returns an array of positions
    def get_valid_moves(self):
        valid_moves = [];
        card_positions = [];

        # look at the cards in the build stacks
        for i in range(len(self.build_stacks)):
            for j in range(len(self.build_stacks[i])):
                if self.build_stacks[i][j].face_up:
                    card1 = self.build_stacks[i][j];
                    for k in range(len(self.build_stacks)):
                        # see if the card can be played on any of the build stacks
                        if i != k:
                            card2 = self.build_stacks[k][-1];
                            if self.is_valid_move(card1, card2, 'build'):
                                valid_moves.append(card1.get_str() + '->' + card2.get_str());
                                new_move = Move(i, j, k, len(self.build_stacks[k])-1, 'build', 'build');
                                card_positions.append(new_move);

        # see if the card can be played on any of the suit stacks
        for i in range(len(self.build_stacks)):
            card1 = self.build_stacks[i][-1];
            for j in range(len(self.suit_stacks)):
                card2 = self.suit_stacks[j][-1];
                if self.is_valid_move(card1, card2, 'suit'):
                    valid_moves.append(card1.get_str() + '->' + card2.get_str());
                    new_move = Move(i, len(self.build_stacks[i])-1, j, len(self.suit_stacks[j])-1, 'build', 'suit');
                    card_positions.append(new_move);

        # look at the card in the talon
        card1 = self.pile[self.talon_idx];
        for i in range(len(self.build_stacks)):
            card2 = self.build_stacks[i][-1];
            if self.is_valid_move(card1, card2, 'build'):
                valid_moves.append(card1.get_str() + '->' + card2.get_str());
                new_move = Move(-1, -1, i, len(self.build_stacks[i])-1, 'talon', 'build');
                card_positions.append(new_move);

        for j in range(len(self.suit_stacks)):
            card2 = self.suit_stacks[j][-1];
            if self.is_valid_move(card1, card2, 'suit'):
                valid_moves.append(card1.get_str() + '->' + card2.get_str());
                new_move = Move(i, j, j, len(self.suit_stacks[j])-1, 'talon', 'suit');
                card_positions.append(new_move);

        # you can always flip a card from the pile to the talon
        next_talon_idx = self.talon_idx + 1 % len(self.pile);
        valid_moves.append('(' + self.pile[self.talon_idx].get_str() + '->' + self.pile[next_talon_idx].get_str() + ')');
        new_move = Move(-1, -1, -1, -1, 'talon', 'talon');
        card_positions.append(new_move);

        print(valid_moves);

        return card_positions;

    # given two positions, moves the card at pos1 onto the card at pos2
    def make_move(self, move):
        if move.src == 'build':
            if move.dest == 'build':
                for i in range(move.y1, len(self.build_stacks[move.x1])):
                    self.build_stacks[move.x2].append(self.build_stacks[move.x1][i]);
                del(self.build_stacks[move.x1][-1]);
                if len(self.build_stacks[move.x1]) != 0:
                    self.build_stacks[move.x1][-1].face_up = True;
            elif move.dest == 'suit':
                self.suit_stacks[move.x2].append(self.build_stacks[move.x1][move.y1]);
                del(self.build_stacks[move.x1][-1]);
                if len(self.build_stacks[move.x1]) != 0:
                    self.build_stacks[move.x1][-1].face_up = True;
        elif move.src == 'talon':
            if move.dest == 'build':
                self.build_stacks[move.x2].append(self.pile[self.talon_idx]);
                del(self.pile[self.talon_idx]);
            elif move.dest == 'suit':
                self.suit_stacks[move.x2].append(self.pile[self.talon_idx]);
                del(self.pile[self.talon_idx]);
            elif move.dest == 'talon':
                self.flip_card_from_pile();

    # need to assign a score to the board to train a neural net
    # the goal in draw 1 solitaire is to uncover all cards in the build stacks
    # after that, winning is trivial
    # picking the move that uncovers the most cards won't always win, but it's a start
    # certain cards being uncovered are better than others
    # * Aces can always be moved to uncover a card, so they're preferable
    # Also need to figure out a lose/give up condition. I don't think this will win every time,
    # so I need to define a time to stop trying to avoid taking too long
    # a simple way to do this is just to set a limit on the number of moves. The winning solution
    # to most games is less than 200 moves, this might be a reasonable place to start.
    def get_score(self):
        # going to start with a naive scoring system and go from there
        face_down_cards = 0;
        for i in range(len(self.build_stacks)):
            for j in range(len(self.build_stacks[i])):
                if not self.build_stacks[i][j].face_up:
                    face_down_cards = face_down_cards + 1;
        score = 28 - face_down_cards;
        return score;

if __name__ == "__main__":
    main()
