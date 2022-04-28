**Development of a new game named Kuba**

Kuba is played on a 7x7 square board, with the following setup:

![image](https://user-images.githubusercontent.com/77983115/165850013-2f0a5449-8156-46d2-a5c9-8b68f95f2af0.png)

Check out the video of the game to understand basic rules: https://www.youtube.com/watch?v=XglqkfzsXYc

Below is the **data structure view** of the game state mentained by the code: - 

**X - Denotes the empty spaces on the board, R - Neutral Red Marblesm W - White Marbles - Player 1, B - Black Marbles - Player 2**

	     1: ['W', 'W', 'X', 'X', 'X', 'B', 'B'],
            2: ['W', 'W', 'X', 'R', 'X', 'B', 'B'],
            3: ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
            4: ['X', 'R', 'R', 'R', 'R', 'R', 'X'],
            5: ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
            6: ['B', 'B', 'X', 'R', 'X', 'W', 'W'],
            7: ['B', 'B', 'X', 'X', 'X', 'W', 'W']
            
**Description**

A stone may slide one cell in any orthogonal direction, and eventually push other stones.

To slide a stone, there must be access to it. For example, to slide a stone to the left, the space just to the right of the stone being moved, cannot have any stone.
If it results to the end of the board then it can be termed as captured 

KO rule - If a player pushes stones in one direction, the other player may not push these stones back in the opposite direction in his next 
move if the full board position is repeated, but must wait one turn. The player cannot push his own stones off the board. 
When a player push off board, one stone, he may slide again.

**Basic Game Rules**

Any player can start the game. Players then alternate turns. There are no bonus turns.
Game ends when a player win.

**Winning Conditions**

A player wins by pushing off and capturing seven neutral red stones or by pushing off all of the opposing stones.  
A player who has no legal moves available has lost the game.

**Rules to move a marble**

You need an empty space (freedom) or to be on the edge of the board to make a move in direction (L, R, F, B).
A player cannot undo a move the opponent just made if it leads to the exact same board position in the subsequent move - (Ko - Rule).
(Track one game state of each player to validate Ko- rule).





