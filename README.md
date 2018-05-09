![alt text](https://raw.githubusercontent.com/Bmcgarry194/master/ChessStyle/black-background-black-and-white-board-game-814133.jpg)


# ChessStyle: Beyond Chess ELO

Predicting chess performance based on style clustering 

Clustering players based on similar play style metrics

## Business Understanding
An additional metric to rate professional chess players besides just straight ELO would be incredibly valuable for chess websites like chess.com, lichess.org, and others. Especially if the evaluation has the appeal of a stylistic component which amature chess players could identify with.

## Data Understanding
There are several different chess databases available online (chessbase,  chesstempo, FIDE, chessdb) which have almost every game played by the top 100 players in pgn format including win, loss or draw, what color played, round number, elo of both competitors and name of event. Also I can scrape wikipedia for additional information on each of the players.

## Data Preparation
Take the data from the chess databases and marry them to additional player info. Use the pgn to extract additional features about the games. Theses features include: opening played, number of pieces on the board at every point in the game, etc.. 

Additionally I will make use of engines to develop more features like: avg centipawn loss per move, sharp vs calm positions, 
Modeling
Start off with a clustering algorithm (K-means) to section off players into specific categories based on features pulled from their games.

For predictions I would use a linear regression or random forest to predict probability of win loss or draw using group membership and elo as features

## Evaluation
The model can be evaluated fairly easily by just taking more recent game data, or held out game data to predict on and see how much my predictions are off from what really happened. 

## Deployment
Most likely just a presentation outlining the different groups of chess players I found and what various characteristics they have along with predictions based on group affiliation. 
