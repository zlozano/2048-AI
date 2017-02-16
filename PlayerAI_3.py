import math
from BaseAI_3 import BaseAI
from Grid_3 import Grid
import time

time_limit = 0.05


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
        num_empty_cells = len(node.getAvailableCells())

        for i in range(node.size):
            for j in range(node.size):
                val = node.getCellValue((i, j))
                score += val * 10 if val else (1000 / num_empty_cells)  # reward empty spaces more if they are scarce

                val_up = node.getCellValue((i - 1, j))
                val_dn = node.getCellValue((i + 1, j))
                val_lt = node.getCellValue((i, j - 1))
                val_rt = node.getCellValue((i, j + 1))
                if val_up is not None and \
                   val_dn is not None and \
                   val != 0:
                    if not (val_up <= val <= val_dn or val_up >= val >= val_dn):
                        score -= 75 * (abs(val_up - val) + abs(val_dn - val))
                if val_lt is not None and \
                   val_rt is not None and \
                   val != 0:
                    if not(val_lt <= val <= val_rt or val_lt >= val >= val_rt):
                        score -= 75 * (abs(val_lt - val) + abs(val_rt - val))

                if j == 0:
                    row = node.map[i]
                    monotonic_row = all(x <= y for x, y in zip(row, row[1:]))
                    monotonic_row = monotonic_row or all(x >= y for x, y in zip(row, row[1:]))
                    if monotonic_row:
                        score += 200 * sum(row)  # big bonus

                if i == 0:
                    col = [node.map[pos][j] for pos in range(node.size)]
                    monotonic_col = all(x <= y for x, y in zip(col, col[1:]))
                    monotonic_col = monotonic_col or all(x >= y for x, y in zip(col, col[1:]))
                    if monotonic_col:
                        score += 200 * sum(col)  # big bonus

                val_order = PlayerAI.get_value_order(val)
                if val_order > 0:
                    val_up_order = PlayerAI.get_value_order(val_up)
                    val_dn_order = PlayerAI.get_value_order(val_dn)
                    val_lt_order = PlayerAI.get_value_order(val_lt)
                    val_rt_order = PlayerAI.get_value_order(val_rt)
                    if val_up_order > 0:
                        score -= abs(val_up_order - val_order) * 25
                    if val_dn_order > 0:
                        score -= abs(val_dn_order - val_order) * 25
                    if val_lt_order > 0:
                        score -= abs(val_lt_order - val_order) * 25
                    if val_rt_order > 0:
                        score -= abs(val_rt_order - val_order) * 25

        return score

    @staticmethod
    def get_value_order(value):
        order = 0
        if value is not None and value > 0:
            while value > 1:
                value >>= 1
                order += 1
        return order

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
