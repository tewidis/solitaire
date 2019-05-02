from card import Card

class Deck:
    # makes a new deck of cards
    # the deck will be in order until shuffled
    def __init__(self):
        self.list = [];
        self.idx = -1;
        suits = ['C', 'D', 'H', 'S']; # clubs, diamonds, hearts, spades
        for i in suits:
            for j in range(1,14):
                if i == 'C' or i == 'S':
                    self.list.append(Card(j, i, 'Black', False));
                elif i == 'D' or i == 'H':
                    self.list.append(Card(j, i, 'Red', False));

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

    # makes a deck that is guaranteed to be winnable
    def make_winnable(self):
        # the idea here is that, for draw 1, you can start from a winning position and
        # randomly put them in different positions on the board. I think it will work, the
        # only tricky part is getting from the board position to the deck such that, when
        # dealt, the board is winnable. I think this is the right place for this function though.
        from random import randint;

        winning_suit_stacks = [[], [], [], []];
        pile = [];
        build_stacks = [[], [], [], [], [], [], []];

        suits = ['C', 'D', 'H', 'S']; # clubs, diamonds, hearts, spades
        for i in range(0,4):
            for j in range(1,14):
                if suits[i] == 'C' or suits[i] == 'S':
                    winning_suit_stacks[i].append(Card(j, suits[i], 'Black', False));
                elif suits[i] == 'D' or suits[i] == 'H':
                    winning_suit_stacks[i].append(Card(j, suits[i], 'Red', False));

        for i in range(0,52):
            stack = randint(0,3);
            while len(winning_suit_stacks[stack]) == 0:
                stack = randint(0,3);

            reroll = True;
            while reroll:
                dest = randint(0,7);
                if dest == 0 and len(build_stacks[dest]) == 1:
                    reroll = True;
                elif dest == 1 and len(build_stacks[dest]) == 2:
                    reroll = True;
                elif dest == 2 and len(build_stacks[dest]) == 3:
                    reroll = True;
                elif dest == 3 and len(build_stacks[dest]) == 4:
                    reroll = True;
                elif dest == 4 and len(build_stacks[dest]) == 5:
                    reroll = True;
                elif dest == 5 and len(build_stacks[dest]) == 6:
                    reroll = True;
                elif dest == 6 and len(build_stacks[dest]) == 7:
                    reroll = True;
                elif dest == 7 and len(pile) == 24:
                    reroll = True;
                else:
                    reroll = False;

            if dest == 7:
                pile.append(winning_suit_stacks[stack][len(winning_suit_stacks[stack])-1]);
            else:
                build_stacks[dest].append(winning_suit_stacks[stack][len(winning_suit_stacks[stack])-1]);

            del(winning_suit_stacks[stack][len(winning_suit_stacks[stack])-1]);

        self.list = [];
        # make the deck
        for i in range(0,7):
            for j in range(0,i+1):
                self.list.append(build_stacks[i][j]);

        for i in range(0,24):
            self.list.append(pile[i]);

