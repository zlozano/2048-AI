# 2048-AI
AI agent to solve 2048 puzzle

The model and main application were taken from a course at Columbia University.  I implemented `PlayerAI_3.py`.

# Implementation

The implementation used is a [minimax](https://en.wikipedia.org/wiki/Minimax) algorithm with [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning).

The player agent must respond with a move within 0.1 seconds.  During that time, an Iterative Deepening DFS is run to find the move which minimizes the maximum loss of the player.  The heuristic evaluation function is based on three main goals:

### Promoting row/column monotonicity

Giving bonuses for monotonic rows and columns helps propagate lower value tiles up to form higher value tiles.

### Reducing the difference between adjacent tiles

Reducing the difference between adjacent tiles allows tiles to merge more easily.

### Maximizing board real estate 

Maxmizing the empty cells allows for more playable space, and reduces the liklihood of running out of tiles, thus ending the game early.

# Running the application

Python 3 is a requirement.

Download the project and execute `python3 GameManager_3.py`
