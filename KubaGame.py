import copy

import Player as Player
import Board as Board


class Game:

    def __init__(self, player1, player2):
        Player.Player(player1)
        self.player1 = Player.Player(player1)
        self.player2 = Player.Player(player2)
        self.board = Board.Board()
        self.winner = None
        self.turn = None
        self.player1.previous_board = None
        self.player2.previous_board = None

    def get_player_details(self, number):
        if number == 1:
            return self.player1
        return self.player2

    def get_board_state(self):
        return self.board

    def set_board_state(self, board_state):
        self.board = board_state

    def print_board(self, board):
        for key in board:
            print(board[key])

    def get_current_turn(self):
        return self.turn

    def identify_player(self, player_num):
        if self.get_player_details(1).get_player_name() == player_num:
            return self.get_player_details(1)
        else:
            return self.get_player_details(2)


    def set_current_turn(self, player):
        self.turn = player.get_player_name()

    def get_winner(self):
        if self.winner is not None:
            return self.winner.get_player_name()
        return None

    def set_winner(self, player):
        self.winner = player

    def get_player1_previous_board(self):
        return self.player1.previous_board

    def set_player1_previous_board(self, previous_board):
        self.player1.previous_board = previous_board

    def get_player2_previous_board(self):
        return self.player2.previous_board

    def set_player2_previous_board(self, previous_board):
        self.player2.previous_board = previous_board

    def get_captured_marbles(self, number):
        return self.get_player_details(number).count

    def add_capture(self, number):
        return self.get_player_details(number).count + 1

    def get_marble(self, coordinates):

        if coordinates[0] in range(0, 7):
            if coordinates[1] in range(0, 7):
                return self.get_board_state().get_board().get(coordinates[0] + 1)[coordinates[1]]

            elif coordinates[1] == -1 or coordinates[1] == 7:
                return 'X'
            return False

        elif coordinates[0] == -1 or coordinates[0] == 7:
            # Check if col coordinate with x-coordinate hits the four corners of board (-1,-1), (-1,7), (7,-1) (7,7)
            if coordinates[1] == -1 or coordinates[1] == 7:
                return 'X'
            # Otherwise, check if it's the left side or right side of the board (such as (-1,0), (7,2), etc.)
            elif coordinates[1] in range(0, 7):
                return 'X'
            # If not, return False
            return False
        return False



    def get_marble_count(self):
        white_count = 0
        black_count = 0
        red_count = 0

        current_row = 1
        while current_row < 8:
            for marble in self.get_board_state().get_board().get(current_row):
                if marble == 'W':
                    white_count += 1
                elif marble == 'B':
                    black_count += 1
                elif marble == 'R':
                    red_count += 1
            current_row += 1

        marble_count = (white_count, black_count, red_count)
        return marble_count

    def validate_board(self, current_board, player):
        if player.get_player_color() == "W":
            if self.get_player1_previous_board() is None:
                self.set_board_state(current_board)
                self.set_player1_previous_board(current_board)
                self.set_current_turn(player.get_player_name())
                self.check_game_winner()
                return True

            else:
                old_board = self.get_player1_previous_board()
                return self.check_ko_rule(current_board, old_board, player)

        else:
            if self.get_player2_previous_board() is None:
                self.set_board_state(current_board)
                self.set_player2_previous_board(current_board)
                self.set_current_turn(player.get_player_name())
                self.check_game_winner()
                return True

            else:
                old_board = self.get_player2_previous_board()
                return self.check_ko_rule(current_board, old_board, player)

        return False

    def check_ko_rule(self, current_board, old_board, player):
        if old_board != current_board:
            self.set_board_state(current_board)
            if player.get_player_color == "W":
                self.set_player1_previous_board(current_board)
                self.turn = self.get_player_details(2).get_player_name()
            else:
                self.set_player2_previous_board(current_board)
                self.turn = self.get_player_details(1).get_player_name()

            return True

        return False

    def check_game_winner(self):

        # Scenario where 7 or more red marbles are captured.
        if self.get_captured_marbles(1) >= 7:
            self.set_winner(self.get_player_details(1).get_player_name())

        if self.get_captured_marbles(2) >= 7:
            self.set_winner(self.get_player_details(2).get_player_name())

        # Scenario where one of the player run out of his marbles
        marble_count = self.get_marble_count()
        if marble_count[0] == 0:
            if self.get_player_details(1).get_player_color() == "W":
                self.set_winner(self.get_player_details(2).get_player_name())

            elif self.get_player_details(2).get_player_color() == "W":
                self.set_winner(self.get_player_details(1).get_player_name())

        if marble_count[1] == 0:

            if self.get_player_details(1).get_player_color() == "B":
                self.set_winner(self.get_player_details(2).get_player_name())

            elif self.get_player_details(2).get_player_color() == "B":
                self.set_winner(self.get_player_details(1).get_player_name())


    def make_move(self, player_name, coordinates, direction):
        if self.identify_player(player_name):
            player = self.identify_player(player_name)
            if player.get_player_color() == "W":
                player_number = 1
            else:
                player_number = 2

            if self.winner is None:
            # If below condition fails revert the current turn to previous (Implement a new funtion that can reset the code.
                if self.get_marble(coordinates) == player.get_player_color():
                    north = self.get_marble((coordinates[0] - 1, coordinates[1]))
                    south = self.get_marble((coordinates[0] + 1, coordinates[1] -1))
                    east = self.get_marble((coordinates[0], coordinates[1]+ 1))
                    west = self.get_marble((coordinates[0], coordinates[1] -1))

                    if direction == "L":
                        if east == 'X':
                            current_board = copy.deepcopy(self.get_board_state())
                            current_row = current_board.get_board().get(coordinates[0] + 1)

                            if west == 'X':
                                current_row.pop(coordinates[1] - 1)
                                current_row.insert(coordinates[1], 'X')

                                return self.validate_board(current_board, player)

                            else:
                                # Check the empty slot on the entire row for movement.
                                empty_position = None

                                for i in range(coordinates[1], -1, -1):
                                    if current_row[i] == 'X':
                                        empty_position = i
                                        break

                                if empty_position:
                                    current_row.pop(empty_position)
                                    current_row.insert(coordinates[1], 'X')

                                    return self.validate_board(current_board, player)

                                else:
                                    popped_marble = current_row.pop(0)
                                    current_row.insert(coordinates[1], 'X')

                                    if popped_marble == 'R':
                                        self.add_capture(player_number)

                                    elif popped_marble == player.get_player_color():
                                        return False

                                    return self.validate_board(current_board, player)
                        return False

                    elif direction == 'R':
                        if west == 'X':
                            current_board = copy.deepcopy(self.get_board_state())
                            current_row = current_board.get_board().get(coordinates[0] + 1)

                            if east == 'X':
                                current_row.pop(coordinates[1] + 1)
                                current_row.insert(coordinates[1], 'X')

                                return self.validate_board(current_board, player)

                            else:
                                # Check the empty slot on the entire row for movement.
                                empty_position = None

                                for i in range(coordinates[1],len(current_board.get_board())):
                                    if current_row[i] == 'X':
                                        empty_position = i
                                        break

                                if empty_position:
                                    current_row.pop(empty_position)
                                    current_row.insert(coordinates[1], 'X')

                                    return self.validate_board(current_board, player)


                                else:
                                    popped_marble = current_row.pop(6)
                                    current_row.insert(coordinates[1], 'X')

                                    if popped_marble == 'R':
                                        self.add_capture(player_number)

                                    elif popped_marble == player.get_player_color():
                                        return False

                                    return self.validate_board(current_board, player)
                        return False

                    elif direction == "F":
                        if south == 'X':
                            current_board = copy.deepcopy(self.get_board_state())
                            current_column = list()

                            for value in current_board.get_board().values():
                                current_column.append(value[coordinates[1]])

                            if north == 'X':
                                current_column.pop(coordinates[0] - 1)
                                current_column.insert(coordinates[0], 'X')

                                return self.validate_board(current_board, player)

                            else:
                                # Check the empty slot on the entire row for movement.
                                empty_position = None

                                for i in range(coordinates[0], -1, -1):
                                    if current_column[i] == 'X':
                                        empty_position = i
                                        break

                                if empty_position:
                                    current_column.pop(empty_position)
                                    current_column.insert(coordinates[0], 'X')

                                    return self.validate_board(current_board, player)

                                else:
                                    popped_marble = current_column.pop(0)
                                    current_column.insert(coordinates[0], 'X')

                                    if popped_marble == 'R':
                                        self.add_capture(player_number)

                                    elif popped_marble == player.get_player_color():
                                        return False

                                    return self.validate_board(current_board, player)
                        return False

                    elif direction == "B":
                        if north == "X":
                            current_board = copy.deepcopy(self.get_board_state())
                            current_column = list()

                            for value in current_board.get_board().values():
                                current_column.append(value[coordinates[1]])

                            if south == 'X':
                                current_column.pop(coordinates[0] + 1)
                                current_column.insert(coordinates[0], 'X')

                                return self.validate_board(current_board, player)

                            else:
                                # Check the empty slot on the entire row for movement.
                                empty_position = None

                                for i in range(coordinates[0], len(current_board.get_board())):
                                    if current_column[i] == 'X':
                                        empty_position = i
                                        break

                                if empty_position:
                                    current_column.pop(empty_position)
                                    current_column.insert(coordinates[0], 'X')

                                    return self.validate_board(current_board, player)

                                else:
                                    popped_marble = current_column.pop(6)
                                    current_column.insert(coordinates[0], 'X')

                                    if popped_marble == 'R':
                                        self.add_capture(player_number)

                                    elif popped_marble == player.get_player_color():
                                        return False

                                    return self.validate_board(current_board, player)
                        return False

                return False


def main():
    game = Game(('PlayerA', 'W'), ('PlayerB', 'B'))
    game.print_board(game.get_board_state().get_board())
    print("\nMarble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))

    print((6, 6), 'L')
    print(game.make_move('PlayerA', (6, 6), 'L'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((6, 0), 'R')
    print(game.make_move('PlayerB', (6, 0), 'R'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((6, 5), 'L')
    print(game.make_move('PlayerA', (6, 5), 'L'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((6, 1), 'R')
    print(game.make_move('PlayerB', (6, 1), 'R'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((6, 5), 'L')
    print(game.make_move('PlayerA', (6, 5), 'L'))  # ko rule should apply and return false
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())  # Should be PlayerA
    print((6, 4), 'F')
    print(game.make_move('PlayerA', (6, 4), 'F'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((5, 0), 'R')
    print(game.make_move('PlayerB', (5, 0), 'R'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((5, 4), 'F')
    print(game.make_move('PlayerA', (5, 4), 'F'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((5, 1), 'R')
    print(game.make_move('PlayerB', (5, 1), 'R'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((0, 0), 'B')
    print(game.make_move('PlayerA', (0, 0), 'B'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((5, 2), 'R')
    print(game.make_move('PlayerB', (5, 2), 'R'))  # B pushes off 1 'W'
    print(game.get_marble_count())  # (7,8,13)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((1, 0), 'B')
    print(game.make_move('PlayerA', (1, 0), 'B'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((5, 3), 'R')
    print(game.make_move('PlayerB', (5, 3), 'R'))  # B pushes off 1 'W'
    print(game.get_marble_count())  # (6,8,13)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((3, 0), 'B')
    print(game.make_move('PlayerA', (3, 0), 'R'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((5, 5), 'B')
    print(game.make_move('PlayerB', (5, 5), 'B'))  # B pushes off 1 'W'
    print(game.get_marble_count())  # (5,8,13)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((3, 1), 'R')
    print(game.make_move('PlayerA', (3, 1), 'R'))  # W pushes off 1 'R'
    print(game.get_marble_count())  # (5,8,12)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((1, 6), 'L')
    print(game.make_move('PlayerB', (1, 6), 'L'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((3, 2), 'R')
    print(game.make_move('PlayerA', (3, 2), 'R'))  # W pushes off 1 'R'
    print(game.get_marble_count())  # (5,8,11)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((1, 5), 'L')
    print(game.make_move('PlayerB', (1, 5), 'L'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((3, 3), 'R')
    print(game.make_move('PlayerA', (3, 3), 'R'))  # W pushes off 1 'R'
    print(game.get_marble_count())  # (5,8,10)
    # print(game.get_captured_marbles())  # Returns 3 (of 7)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((1, 4), 'L')
    print(game.make_move('PlayerB', (1, 4), 'L'))  # B pushes off 1 'W'
    print(game.get_marble_count())  # (4,8,10)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((3, 4), 'R')
    print(game.make_move('PlayerA', (3, 4), 'R'))  # W pushes off 1 'R'
    print(game.get_marble_count())  # (4,8,9)
    #print(game.get_captured_marbles()) # Returns 4 (of 7)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((1, 3), 'L')
    print(game.make_move('PlayerB', (1, 3), 'L'))  # B pushes off 1 'R'
    print(game.get_marble_count())  # (4,8,8)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((3, 5), 'R')
    print(game.make_move('PlayerA', (3, 5), 'R'))  # W pushes off 1 'R'
    print(game.get_marble_count())  # (4,8,7)
    # print(game.get_captured_marbles())  # Returns 5 (of 7)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((0, 6), 'F')
    print(game.make_move('PlayerB', (0, 6), 'F'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((2, 0), 'F')
    print(game.make_move('PlayerA', (2, 0), 'F'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((1, 6), 'B')
    print(game.make_move('PlayerB', (1, 6), 'B'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((1, 0), 'F')
    print(game.make_move('PlayerA', (1, 0), 'F'))  # W pushes off 1 'R'
    print(game.get_marble_count())  # (4,8,6)
    #print(game.get_captured_marbles())  # Returns 6 (of 7)
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((0, 5), 'B')
    print(game.make_move('PlayerB', (0, 5), 'B'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((4, 6), 'B')
    print(game.make_move('PlayerA', (4, 6), 'B'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print((1, 5), 'B')
    print(game.make_move('PlayerB', (1, 5), 'B'))  # True
    game.print_board(game.get_board_state().get_board())
    print(game.get_current_turn())
    print(game.get_winner())  # None (no winner yet)
    print((5, 6), 'B')
    print(game.make_move('PlayerA', (5, 6), 'B'))  # Win step
    #print(game.get_captured_marbles())  # Returns 7 (of 7)
    print(game.get_winner())  # PlayerA
    game.print_board(game.get_board_state().get_board())


if __name__ == '__main__':
    main()
