"""
Do refer the readme file and the pdf document for the better understanding of the code and analysis.
"""



import copy
import Player as Player
import Board as Board


class Game:
    """
    Game Class that keeps players, board_state, winner, turn,
    players previous board states
    Number 1 - Player 1
    Number 2 - Player 2
    """

    def __init__(self, player1, player2):
        self.player1 = Player.Player(player1) # Track Player 1
        self.player2 = Player.Player(player2)  # Track Player 2
        self.board = Board.Board()  # Track Board
        self.winner = None
        self.turn = None
        self.player1.previous_board = None  # Track the board state of for player 1
        self.player2.previous_board = None  # Track the board state of for player 2

    def get_player_details(self, number):
        """
        If 1 return player 1, else return player 2
        :param number:
        :return:
        """
        if number == 1:
            return self.player1
        return self.player2

    def get_board_state(self):
        return self.board

    def set_board_state(self, board_state):
        self.board = board_state

    def print_board(self, board):
        """
        Print the board for understanding purpose.
        :param board:
        :return:
        """
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
            return self.winner
        return None

    def set_winner(self, player_name):
        self.winner = player_name

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
        """
        Adds the cpature marble count.
        :param number:
        :return:
        """
        return self.get_player_details(number).set_player_count()

    def get_marble(self, coordinates):

        if coordinates[0] in range(0, 7):
            if coordinates[1] in range(0, 7):
                return self.get_board_state().get_board().get(coordinates[0] + 1)[coordinates[1]]

            elif coordinates[1] == -1 or coordinates[1] == 7:
                return 'X'
            return False

        elif coordinates[0] == -1 or coordinates[0] == 7:
            # Check if col coordinate with x-coordinate hits the four corners of board
            if coordinates[1] == -1 or coordinates[1] == 7:
                return 'X'
            # Check if it's the left side or right side of the board
            elif coordinates[1] in range(0, 7):
                return 'X'
            # If not, return False
            return False
        return False

    def get_marble_count(self):
        """
        Calculate an each marble count and return it as a tuple.
        :return: Tuple
        """
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
        """
        It validates the board, called inside the make move function.
        It also validates the ko rule condition
        :param current_board:
        :param player:
        :return: Bool
        """
        if player.get_player_color() == "W":
            if self.get_player1_previous_board() is None:
                self.set_board_state(current_board)
                self.set_player1_previous_board(self.get_board_state().get_board())
                self.set_current_turn(self.get_player_details(2))
                self.check_game_winner()
                return True

            else:
                old_board = self.get_player1_previous_board()
                return self.check_ko_rule(current_board, old_board, player)

        else:
            if self.get_player2_previous_board() is None:
                self.set_board_state(current_board)
                self.set_player2_previous_board(self.get_board_state().get_board())
                self.set_current_turn(self.get_player_details(1))
                self.check_game_winner()
                return True

            else:
                old_board = self.get_player2_previous_board()
                return self.check_ko_rule(current_board, old_board, player)

        return False

    def check_ko_rule(self, current_board, old_board, player):
        """
        Compare the old board with the current board based on the player supplied
        :param current_board:
        :param old_board:
        :param player:
        :return: Bool
        """
        if old_board != current_board.get_board():
            self.set_board_state(current_board)
            if player.get_player_color() == "W":
                self.set_player1_previous_board(self.get_board_state().get_board())
                self.turn = self.get_player_details(2).get_player_name()
            else:
                self.set_player2_previous_board(self.get_board_state().get_board())
                self.turn = self.get_player_details(1).get_player_name()

            self.check_game_winner()
            return True

        print("Ko rule is violated at this move")
        return False

    def check_game_winner(self):
        """
        Check in case a winner is based on 2 scenarios:-

        1) Scenario where 7 or more red marbles are captured.
        2) Scenario where one of the player run out of marbles.

        :return:
        """

        if self.get_captured_marbles(1) >= 7:
            self.set_winner(self.get_player_details(1).get_player_name())

        if self.get_captured_marbles(2) >= 7:
            self.set_winner(self.get_player_details(2).get_player_name())


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
        """
        It allows the player to make a move. Depending on the provided coordinates and
        the direction from (Left, Right, Forward, Backward) - the board is updated is accordingly.
        validate board function is also called.
        :param player_name:
        :param coordinates:
        :param direction:
        :return:
        """

        if self.identify_player(player_name):
            player = self.identify_player(player_name)
            if player.get_player_color() == "W":
                # This is used for updating the turn to second player or vice versa.
                player_number = 2
            else:
                player_number = 1
            # If there is no winner, then only perfrom this.
            if self.winner is None:
                # Condition to check that the player is moving it's own marble
                if self.get_marble(coordinates) == player.get_player_color():
                    # Identify the freedom from the choosen coordinates.
                    north = self.get_marble((coordinates[0] - 1, coordinates[1]))
                    south = self.get_marble((coordinates[0] + 1, coordinates[1]))
                    east = self.get_marble((coordinates[0], coordinates[1] + 1))
                    west = self.get_marble((coordinates[0], coordinates[1] -1))

                    # Depending upon the directions there are 4 scenarios - (L,R, F, B)

                    if direction == "L":
                        if east == 'X':
                            current_board = copy.deepcopy(self.get_board_state())
                            current_row = current_board.get_board().get(coordinates[0] + 1)

                            if west == 'X':
                                current_row.pop(coordinates[1] - 1)
                                current_row.insert(coordinates[1], 'X')
                                # Validate the board
                                return self.validate_board(current_board, player)

                            else:
                                # Check the empty slot on the entire row towards left for the shifting.
                                empty_position = None

                                for i in range(coordinates[1], -1, -1):
                                    if current_row[i] == 'X':
                                        empty_position = i
                                        break

                                if empty_position:
                                    current_row.pop(empty_position)
                                    current_row.insert(coordinates[1], 'X')

                                    # Validate the board
                                    return self.validate_board(current_board, player)

                                # In case there are no empty slots in the entire row,
                                # then check if the last element is Red marble or not.
                                else:
                                    popped_marble = current_row.pop(0)
                                    current_row.insert(coordinates[1], 'X')
                                    # If popped marble is red then it is a capture.
                                    if popped_marble == 'R':
                                        if player_number == 2:
                                            self.add_capture(1)
                                        else:
                                            self.add_capture(2)

                                    elif popped_marble == player.get_player_color():
                                        return False

                                    # Validate the board
                                    return self.validate_board(current_board, player)
                        print("Move is invalid")
                        return False

                    elif direction == 'R':
                        if west == 'X':
                            current_board = copy.deepcopy(self.get_board_state())
                            current_row = current_board.get_board().get(coordinates[0] + 1)

                            if east == 'X':
                                current_row.pop(coordinates[1] + 1)
                                current_row.insert(coordinates[1], 'X')

                                # Validate the board
                                return self.validate_board(current_board, player)

                            else:
                                # Check the empty slot on the entire row towards the right for shifting.
                                empty_position = None

                                for i in range(coordinates[1],len(current_board.get_board())):
                                    if current_row[i] == 'X':
                                        empty_position = i
                                        break

                                if empty_position:
                                    current_row.pop(empty_position)
                                    current_row.insert(coordinates[1], 'X')

                                    # Validate the board
                                    return self.validate_board(current_board, player)

                                # In case there are no empty slots in the entire row,
                                # then check if the last element is Red marble or not.
                                else:
                                    popped_marble = current_row.pop(6)
                                    current_row.insert(coordinates[1], 'X')

                                    if popped_marble == 'R':
                                        if player_number == 2:
                                            self.add_capture(1)
                                        else:
                                            self.add_capture(2)

                                    elif popped_marble == player.get_player_color():
                                        return False

                                    # Validate the board
                                    return self.validate_board(current_board, player)
                        print("Move is invalid")
                        return False

                    elif direction == "F":
                        if south == 'X':
                            current_board = copy.deepcopy(self.get_board_state())
                            current_column = list()

                            # In this case we need to identify the column of the board.
                            for value in current_board.get_board().values():
                                current_column.append(value[coordinates[1]])

                            # If X identified in North, then shift.
                            if north == 'X':
                                current_column.pop(coordinates[0] - 1)
                                current_column.insert(coordinates[0], 'X')

                                count = 0
                                for value in current_board.get_board().values():
                                    value[coordinates[1]] = current_column[count]
                                    count += 1

                                # Validate the board
                                return self.validate_board(current_board, player)

                            else:
                                # Check the empty slot on the entire column to the top for shifting.
                                empty_position = None

                                for i in range(coordinates[0], -1, -1):
                                    if current_column[i] == 'X':
                                        empty_position = i
                                        break

                                if empty_position:
                                    current_column.pop(empty_position)
                                    current_column.insert(coordinates[0], 'X')

                                    count = 0
                                    for value in current_board.get_board().values():
                                        value[coordinates[1]] = current_column[count]
                                        count += 1

                                    # Validate the board
                                    return self.validate_board(current_board, player)

                                # If no empty slot, pop the first element in column and then perform shift,
                                # with the coordinate value turned X (empty)
                                else:
                                    popped_marble = current_column.pop(0)
                                    current_column.insert(coordinates[0], 'X')

                                    count = 0
                                    for value in current_board.get_board().values():
                                        value[coordinates[1]] = current_column[count]
                                        count += 1

                                    # If popped marble is R, then capture the count.
                                    if popped_marble == 'R':
                                        if player_number == 2:
                                            self.add_capture(1)
                                        else:
                                            self.add_capture(2)

                                    elif popped_marble == player.get_player_color():
                                        return False

                                    # Validate the board
                                    return self.validate_board(current_board, player)
                        print("Move is invalid")
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

                                count = 0
                                for value in current_board.get_board().values():
                                    value[coordinates[1]] = current_column[count]
                                    count += 1

                                # Validate the board
                                return self.validate_board(current_board, player)

                            else:
                                # Check the empty slot on the entire column till the bottom for shifting.
                                empty_position = None

                                for i in range(coordinates[0], len(current_board.get_board())):
                                    if current_column[i] == 'X':
                                        empty_position = i
                                        break

                                if empty_position:
                                    current_column.pop(empty_position)
                                    current_column.insert(coordinates[0], 'X')

                                    count = 0
                                    for value in current_board.get_board().values():
                                        value[coordinates[1]] = current_column[count]
                                        count += 1

                                    # Validate the board
                                    return self.validate_board(current_board, player)

                                # If no empty slot, pop the last element of column and then perform shift,
                                # with the coordinate value turned X (empty)
                                else:
                                    popped_marble = current_column.pop(6)
                                    current_column.insert(coordinates[0], 'X')

                                    count = 0
                                    for value in current_board.get_board().values():
                                        value[coordinates[1]] = current_column[count]
                                        count += 1

                                    # If popped marble is R, then capture the count.
                                    if popped_marble == 'R':
                                        if player_number == 2:
                                            self.add_capture(1)
                                        else:
                                            self.add_capture(2)

                                    elif popped_marble == player.get_player_color():
                                        return False

                                    # Validate the board
                                    return self.validate_board(current_board, player)
                        print("Move is invalid")
                        return False

                return False


def main():
    """
    Used for adding the valid moves to the program.
    :return:
    """
    game = Game(('PlayerA', 'W'), ('PlayerB', 'B'))
    game.print_board(game.get_board_state().get_board())
    print("\nMarble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))

    print((7, 7), 'L')
    print(game.make_move('PlayerA', (6, 6), 'L'))  # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((7, 1), 'R')
    print(game.make_move('PlayerB', (6, 0), 'R'))  # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((7, 6), 'L')
    print(game.make_move('PlayerA', (6, 5), 'L'))  # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((7, 2), 'R')
    print(game.make_move('PlayerB', (6, 1), 'R'))  # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((7, 6), 'L')
    print(game.make_move('PlayerA', (6, 5), 'L'))  # False - Ko Rule Failed this move
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((7, 5), 'F')
    print(game.make_move('PlayerA', (6, 4), 'F'))  # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((6, 1), 'R')
    print(game.make_move('PlayerB', (5, 0), 'R'))  # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((6, 5), 'F')
    print(game.make_move('PlayerA', (5, 4), 'F'))  # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((6, 2), 'R')
    print(game.make_move('PlayerB', (5, 1), 'R')) # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((1, 1), 'B')
    print(game.make_move('PlayerA', (0, 0), 'B')) # True
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((6, 3), 'R')
    print(game.make_move('PlayerB', (5, 2), 'R'))
    print("White marble is captured in 5th Row (Count from 0)")
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((2, 1), 'B')
    print(game.make_move('PlayerA', (1, 0), 'B'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((6, 4), 'R')
    print(game.make_move('PlayerB', (5, 3), 'R'))
    print("White marble is captured in 5th Row (Count from 0)")
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((4, 1), 'B')
    print(game.make_move('PlayerA', (3, 0), 'R'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((6, 6), 'B')
    print(game.make_move('PlayerB', (5, 5), 'B'))
    print("White marble in 6th Row (Count from 0)")
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((4, 2), 'R')
    print(game.make_move('PlayerA', (3, 1), 'R'))
    print("Red marble is captured in 4th row by Player A")
    print("Red marbles count for Player A is {}".format(game.player1.count))
    print("Red marbles count for Player B is {}".format(game.player2.count))
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    print("\n")
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((2, 7), 'L')
    print(game.make_move('PlayerB', (1, 6), 'L'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((4, 3), 'R')
    print(game.make_move('PlayerA', (3, 2), 'R'))
    print("Red marble is captured in 4th row by Player A")
    print("Red marbles count for Player A is {}".format(game.player1.count))
    print("Red marbles count for Player B is {}".format(game.player2.count))
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    print("\n")
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((2, 6), 'L')
    print(game.make_move('PlayerB', (1, 5), 'L'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((4, 4), 'R')
    print(game.make_move('PlayerA', (3, 3), 'R'))
    print("Red marble is captured in 4th row by Player A")
    print("Red marbles count for Player A is {}".format(game.player1.count))
    print("Red marbles count for Player B is {}".format(game.player2.count))
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    print("\n")
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((2, 5), 'L')
    print(game.make_move('PlayerB', (1, 4), 'L'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((3, 4), 'R')
    print(game.make_move('PlayerA', (3, 4), 'R'))
    print("Red marble is captured in 4th row by Player A")
    print("Red marbles count for Player A is {}".format(game.player1.count))
    print("Red marbles count for Player B is {}".format(game.player2.count))
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    print("\n")
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((2, 4), 'L')
    print(game.make_move('PlayerB', (1, 3), 'L'))
    game.print_board(game.get_board_state().get_board())


    print("\n")
    print(game.get_current_turn())
    print((4, 6), 'R')
    print(game.make_move('PlayerA', (3, 5), 'R'))
    print("Red marble is captured in 4th row by Player A")
    print("Red marbles count for Player A is {}".format(game.player1.count))
    print("Red marbles count for Player B is {}".format(game.player2.count))
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    print("\n")
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((1, 7), 'F')
    print(game.make_move('PlayerB', (0, 6), 'F'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((3, 1), 'F')
    print(game.make_move('PlayerA', (2, 0), 'F'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((2, 7), 'B')
    print(game.make_move('PlayerB', (1, 6), 'B'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((2, 1), 'F')
    print(game.make_move('PlayerA', (1, 0), 'F'))
    print("Red marble is captured in 4th row by Player A")
    print("Red marbles count for Player A is {}".format(game.player1.count))
    print("Red marbles count for Player B is {}".format(game.player2.count))
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    print("\n")
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((1, 6), 'B')
    print(game.make_move('PlayerB', (0, 5), 'B'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((5, 7), 'B')
    print(game.make_move('PlayerA', (4, 6), 'B'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((2, 6), 'B')
    print(game.make_move('PlayerB', (1, 5), 'B'))
    game.print_board(game.get_board_state().get_board())

    print("\n")
    print(game.get_current_turn())
    print((6, 7), 'B')
    print(game.make_move('PlayerA', (5, 6), 'B'))
    print("Red marble is captured in 4th row by Player A")
    print("Red marbles count for Player A is {}".format(game.player1.count))
    print("Red marbles count for Player B is {}".format(game.player2.count))
    print("Marble Count (White, Black , Red) is - {} ".format(game.get_marble_count()))
    print("Winner is {}".format(game.get_winner()))
    game.print_board(game.get_board_state().get_board())


if __name__ == '__main__':
    main()
