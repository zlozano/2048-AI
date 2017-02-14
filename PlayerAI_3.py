import math
from BaseAI_3 import BaseAI
from Grid_3 import Grid
import time

time_limit = 0.02

class PlayerAI(BaseAI):

    def getMove(self, grid: Grid):
        return self.alpha_beta(grid)

    """
    An iterative deepening, alpha-beta pruned, minimax search.
    Return the next move which minimizes the maximum loss incurred.
    """
    def alpha_beta(self, node: Grid):
        maximizing_value = -math.inf
        maximizing_move = None
        depth = 1
        start = time.clock()
        while time.clock() - start < time_limit and depth < 4:
            (value, move) = self.maximizing(-math.inf, math.inf, node, depth)
            maximizing_value = max(maximizing_value, value)
            maximizing_move = move if value == maximizing_value else move
            depth += 1
        return maximizing_move

    """
    Maximizing function - returns the best possible move, given the result of the minimizing player's move
    """
    def maximizing(self, alpha, beta, node: Grid, depth):
        maximizing_move = None
        if depth == 0:
            return self.heuristic(node), maximizing_move

        moves = node.getAvailableMoves()
        if not moves:
            return self.get_terminal_node_value(node), maximizing_move

        value = -math.inf
        for move in moves:
            child = node.clone()
            child.move(move)
            opponent_value = self.minimizing(alpha, beta, child, depth - 1)
            maximizing_move = move if opponent_value >= value else maximizing_move
            value = max(value, opponent_value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, maximizing_move

    """
    Minimizing function - returns the lowest scored move based on opponent's previous move
    """
    def minimizing(self, alpha, beta, node: Grid, depth):
        if depth == 0:
            return self.heuristic(node)

        cells = node.getAvailableCells()
        if not cells:
            return self.get_terminal_node_value(node)

        value = math.inf
        for cell in cells:
            for i in range(2, 5, 2):
                child = node.clone()
                child.insertTile(cell, i)
                value = min(value, self.maximizing(alpha, beta, child, depth - 1)[0])
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return value

    """
    Maximizing heuristic function for non-terminal nodes
    """
    @staticmethod
    def heuristic(node: Grid):
        score = 0

        # award monotonic sequences among rows
        for row in node.map:
            for i in range(1, len(row)):
                if i < len(row) - 1:
                    if row[i - 1] <= row[i] <= row[i + 1]:
                        score += 900
                    elif row[i - 1] >= row[i] >= row[i + 1]:
                        score += 900
                    else:
                        score -= 100000
                if row[i] != 0 and row[i - 1] != 0:
                    score -= abs(row[i] - row[i - 1]) * 1000

        # award monotonic sequences among columns
        for j in range(node.size):
            for i in range(1, len(node.map)):
                if i < len(node.map) - 1:
                    if node.map[i - 1][j] <= node.map[i][j] <= node.map[i + 1][j]:
                        score += 900
                    elif node.map[i - 1][j] >= node.map[i][j] >= node.map[i + 1][j]:
                        score += 900
                    else:
                        score -= 100000
                if node.map[i][j] != 0 and node.map[i - 1][j] != 0:
                    score -= abs(node.map[i][j] - node.map[i - 1][j]) * 1000

        # maximize board real estate (as many high value cells with maximum empty cells
        for row in node.map:
            for val in row:
                if val == 0:
                    score += 30000
                elif val == 2 or val == 4:
                    score -= 8000
                elif val >= 128:
                    score += val * 10000
                elif val >= 32:
                    score += val * 100

        return score

    """
    Determine if a losing state has been found or a winning state.
    For winning state return highest possible value.
    For losing state return lowest possible value.
    """
    @staticmethod
    def get_terminal_node_value(node: Grid):
        for row in node.map:
            for val in row:
                if val == 2048:
                    return math.inf
        return -math.inf


