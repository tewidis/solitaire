from card import Card

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
