import sys

SIZE = 3

EMPTY = 1
X = 2
O = 4
DRAW = 8

class Player:
    def __init__(self, board, xo):
        self._board = board
        self._xo = xo

    @property
    def board(self):
        return self._board

    @property
    def xo(self):
        return self._xo

    def make_move(self):
        pass

class AI(Player):
    def __init__(self, board, xo):
        super().__init__(board, xo)
        self.CACHED = {}

    def best_move(self, xo):
        board = self._board
        h = hash(board)

        if h in self.CACHED:
            return self.CACHED[h]

        w = board.whos_won()
        if w != EMPTY:
            if w == xo: return (10000, None, 1)
            elif w == DRAW: return (0, None, 1)
            else: return (-10000, None, 1)

        best_pos = None
        best_score = None
        total_moves = 0

        for m in board.all_moves():
            board.do_move(m, xo)

            ox = O if xo == X else X

            (score, next_move, moves) = self.best_move(ox)
            score = -score
            total_moves += moves

            if best_score is None or best_score < score:
                best_score = score
                best_pos = m

            board.undo_move(m)

        self.CACHED[h] = (best_score, best_pos, total_moves)

        return (best_score, best_pos, total_moves)

    def make_move(self):
        (score, move, total_moves) = self.best_move(self.xo)

        return move

class Human(Player):
    def __init__(self, board, xo):
        super().__init__(board, xo)

    def make_move(self):
        while True:
            try:
                print ("Enter your move:")
                l = sys.stdin.readline()
                i, j = map(int, l.strip().split())

                if self._board.board[i][j] == EMPTY:
                    return (i,j)
                
                print ("Can't make move ({}, {}). Try again".format(i,j))

            except:
                if l.strip() == "": sys.exit(1)
                print ("`{}` is not a valid input".format(l[:-1]))
                print ("Please enter <column> <row> + Enter. <column>,<row> are 0-based.".format(l[:-1]))
                print ("To quit input an empty string.")

class Board:
    def __init__(self):
        self._board = None
        self.reset()

    @property
    def board(self):
        return self._board

    def __hash__(self):
        H = 0
        for i in range(0, 3):
            for j in range(0, 3):
                H = (H << 4) | self._board[i][j]
        return H

    def whos_won(self):
        cw = [0] * SIZE
        rw = [0] * SIZE
        dw = [0] * 2
        all = 0

        for i in range(SIZE):
            dw[0] |= self.board[i][i]
            dw[1] |= self.board[i][SIZE-1-i]
            for j in range(SIZE):
                cw[i] |= self.board[i][j]
                rw[j] |= self.board[i][j]
                all |= self.board[i][j]

        for i in range(SIZE):
            if cw[i] in (X, O): return cw[i]
            if rw[i] in (X, O): return rw[i]

        for i in range(2):
            if dw[i] in (X, O): return dw[i]

        return EMPTY if (all & EMPTY) else DRAW

    def do_move(self, m, xo):
        if m[0] < 0 or m[0] >= SIZE or m[1] < 0 or m[1] >= SIZE:
            return False

        if self._board[m[0]][m[1]] != EMPTY:
            return False

        self._board[m[0]][m[1]] = xo

        return True

    def undo_move(self, m):
        self._board[m[0]][m[1]] = EMPTY

    def reset(self):
        self._board = [[EMPTY] * SIZE for i in range(SIZE)]
        
    def all_moves(self):
        return [ (i, j) for j in range(SIZE) for i in range(SIZE) if self._board[i][j] == EMPTY ]

    
SHOW = {
    EMPTY : '.',
    X : 'X',
    O : 'O',
}

class Game:
    def __init__(self):
        self._board = Board()
        self._player = {
#            X : Human(self._board, X),
#            O : AI(self._board, O)
            X : AI(self._board, X),
            O : Human(self._board, O)
        }

    def print_board(self):
        print ("----")

        print ("\n".join([" ".join(map(lambda c: SHOW[c], row)) for row in self._board.board]))

        w = self._board.whos_won()

        if w in (X, O):  print ("{} won!".format(SHOW[w]))
        elif w == DRAW:  print ("Draw")
        else:            print ("In progress")

#        print (board.all_moves())

    def run(self):
        turn = X
        w = EMPTY

        while w == EMPTY:
            self.print_board()

            m = self._player[turn].make_move()

            self._board.do_move(m, turn)

            turn = O if turn == X else X
            w = self._board.whos_won()

        self.print_board()

#    for i,j,xo in [(1,1,X), (0,0,O), (0,1,X), (2,1,O), (1,2,X), (1,0,O), (2,0,X), (0,2,O), (2,2,X)]:
#        do_move(board,i,j,xo)
#        print_board(board)

def main():
    g = Game()
    g.run()

if __name__ == "__main__":
    main()
