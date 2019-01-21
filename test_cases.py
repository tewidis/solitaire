class test_cases:
    def __init__(self):
        print('Initialize')

    def test_is_valid_move(board):
        if board.is_valid_move(Card(3, 'D', 'Red'), Card(4, 'C', 'Black'), 'build'):
            print('PASS');
        if board.is_valid_move(Card(13, 'D', 'Red'), Card(-1, '', ''), 'build'):
            print('PASS');
        if not board.is_valid_move(Card(3, 'D', 'Red'), Card(4, 'D', 'Red'), 'build'):
            print('PASS');
        if board.is_valid_move(Card(3, 'D', 'Red'), Card(2, 'D', 'Red'), 'suit'):
            print('PASS');
        if board.is_valid_move(Card(1, 'D', 'Red'), Card(-1, '', ''), 'suit'):
            print('PASS');
        if not board.is_valid_move(Card(3, 'D', 'Red'), Card(4, 'C', 'Black'), 'suit'):
            print('PASS');


