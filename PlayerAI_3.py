from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):

    def getMove(self, grid):
        moves = grid.getAvailableMoves()

        print('zac ' + str(moves))

        return moves[0]
