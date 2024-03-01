# Connect4AI
The math for this algorithm is as follows:

        line_score = 0
        if there are 4 of the same color then,
            line_score += 500
        else if there are 3 of the same color but 1 empty slot then,
            line_score += 5
        else if there are 2 of the same color and 2 empty slots then,
            line_score += 1
	
Note: if there is only one of the same color, then it is too far from the winning condition, thus, this line can be disregarded. If there are lines that do not have consecutive tiles of the same color, it is also disregarded since it is too far from the winning condition.

Total Score = vertical line score + horizontal line score + left diagonal line score + right diagonal line score 

My motivation:
My algorithm examines all possible windows made up of 4 blocks. These possible windows include horizontal, vertical, and diagonal windows created to check winning conditions. This was to mimic the Connect 4 games, which require 4 consecutive coins of the same color. This involves assigning numerical values to these windows based on their potential to contribute to a winning arrangement. Priority is given to windows that represent winning configurations, while intermediate ones receive values reflecting their potential to evolve into winning setups. Conversely, windows incapable of forming a solution are disregarded. To emulate competition dynamics, positive scores denote advantageous outcomes for the player, while negative scores represent gains for the opponent.
Red: Minimax AI
Yello: monteCarloAI
In this midgame example, the red lines represent the lines that are disregarded. This is because these lines are too far from the winning condition. However, the green line represents a line that is regarded as a winning condition. In this case, the green line has 3 spaces that are filled with the same color and has one space. This will trigger the following conditions:
else if there are 3 of the same color but 1 empty slot then,
            line_score += 5
Then, there is also another case for the red player that has 3 spaces filled and with one space, thus, the condition:
else if there are 3 of the same color but 1 empty slot then,
            line_score += 5

will trigger again.


Thus, the total score will come out to be 10. This is significantly lower than the score of 500 since it is close to the winning condition, but is not a win yet. Ultimately, the score of the red player will have a score of 10.

In terms of the yellow player, the yellow player does not have a line that represents a winning condition, thus, the yellow player will have a score of 0.

Now, comparing these two scores, the probability of the red player winning will be counted as higher since the red player has a greater score.

In the next moves, the red player will try to place the coins on the left side of the board, since it has found the best move with the 3 red colors in a row.

Alpha-Beta pruning agent’s successor function

My successor function places the coins around the middle of the board. By focusing on the center, the alpha-beta algorithm can establish bounds for alpha and beta according to the activity in this center area. 
