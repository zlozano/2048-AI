import math
from BaseAI_3 import BaseAI
from Grid_3 import Grid
import time

time_limit = 0.03  # IDDFS for .7 seconds

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
        while time.clock() - start < time_limit:
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
        for row in node.map:
            for i in range(1, len(row) - 1):
                if row[i - 1] <= row[i] <= row[i + 1]:
                    score += 1
                elif row[i - 1] >= row[i] >= row[i + 1]:
                    score += 1

        for j in range(node.size):
            for i in range(1, len(node.map) - 1):
                if node.map[i - 1][j] < node.map[i][j] < node.map[i + 1][j]:
                    score += 1
                elif node.map[i - 1][j] > node.map[i][j] > node.map[i + 1][j]:
                    score += 1

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


