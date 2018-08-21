import sys

SIZE = 3

EMPTY = 1
X = 2
O = 4
DRAW = 8

def whos_won(board):
    cw = [0] * SIZE
    rw = [0] * SIZE
    dw = [0] * 2
    all = 0

    for i in range(SIZE):
        dw[0] |= board[i][i]
        dw[1] |= board[i][SIZE-1-i]
        for j in range(SIZE):
            cw[i] |= board[i][j]
            rw[j] |= board[i][j]
            all |= board[i][j]

    for i in range(SIZE):
        if cw[i] in (X, O): return cw[i]
        if rw[i] in (X, O): return rw[i]

    for i in range(2):
        if dw[i] in (X, O): return dw[i]

    return EMPTY if (all & EMPTY) else DRAW

SHOW = {
    EMPTY : '.',
    X : 'X',
    O : 'O',
}

def do_move(board, i, j, xo):
    if i < 0 or i >= SIZE or j < 0 or j >= SIZE:
        return False

    if board[i][j] != EMPTY:
        return False

    board[i][j] = xo
    return True

def all_moves(board):
    return [ (i, j) for j in range(SIZE) for i in range(SIZE) if board[i][j] == EMPTY ]

def h(board):
    H = 0
    for i in range(0, 3):
        for j in range(0, 3):
            H = (H << 4) | board[i][j]

    return H

CACHED = {}

def best_move(board, xo):
    H = h(board)
    if H in CACHED:
        return CACHED[H]

    w = whos_won(board)
    if w != EMPTY:
        if w == xo: return (10000, None, 1)
        elif w == DRAW: return (0, None, 1)
        else: return (-10000, None, 1)

    best_pos = None
    best_score = None
    total_moves = 0

    for i,j in all_moves(board):
        do_move(board, i, j, xo)
        ox = O if xo == X else X

        (score, next_move, moves) = best_move(board, ox)
        score = -score
        total_moves += moves

        if best_score is None or best_score < score:
            best_score = score
            best_pos = (i,j)

        board[i][j] = EMPTY

    CACHED[H] = (best_score, best_pos, total_moves)

    return (best_score, best_pos, total_moves)

def auto_move(board, xo):
    (score, move, total_moves) = best_move(board, xo)

    return move

def print_board(board):
    print "----"

    print "\n".join([" ".join(map(lambda c: SHOW[c], row)) for row in board])

    w = whos_won(board)

    if w in (X, O):
        print "{} won!".format(SHOW[w])
    elif w == DRAW:
        print "Draw"
    else:
        print "In progress"

    print all_moves(board)

def game():
    board = [[EMPTY] * SIZE for i in range(SIZE)]

    turn = X
    w = EMPTY

    while w == EMPTY:
        print_board(board)

        print "Best move: {}".format(best_move(board, turn))

        print "{}'s turn".format(SHOW[turn])

        l = ""

        while True:
            try:
                print "Enter your move:"
                l = sys.stdin.readline()
                i, j = map(int, l.strip().split())
                
                if (do_move(board, i, j, turn)):
                    break

                print "Can't make move ({}, {}). Try again".format(i,j)

            except:
                if l.strip() == "": sys.exit(1)
                print "`{}` is not a valid input".format(l[:-1])
                print "Please enter <column> <row> + Enter. <column>,<row> are 0-based.".format(l[:-1])
                print "To quit input an empty string."

        turn = O if turn == X else X
        w = whos_won(board)

    print_board(board)

#    for i,j,xo in [(1,1,X), (0,0,O), (0,1,X), (2,1,O), (1,2,X), (1,0,O), (2,0,X), (0,2,O), (2,2,X)]:
#        do_move(board,i,j,xo)
#        print_board(board)

def main():
    game()

if __name__ == "__main__":
    main()
