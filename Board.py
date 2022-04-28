

class Board:

    def __init__(self):
        self.board_game = {
            1: ['W', 'W', 'X', 'X', 'X', 'B', 'B'],
            2: ['W', 'W', 'X', 'R', 'X', 'B', 'B'],
            3: ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
            4: ['X', 'R', 'R', 'R', 'R', 'R', 'X'],
            5: ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
            6: ['B', 'B', 'X', 'R', 'X', 'W', 'W'],
            7: ['B', 'B', 'X', 'X', 'X', 'W', 'W']
        }

    def get_board(self):
        return self.board_game
