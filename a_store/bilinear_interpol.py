import math

def resize(A, B):
    Ha = len(A)
    Wa = len(A[0]) if Ha > 0 else 0
    Hb = len(B)
    Wb = len(B[0]) if Hb > 0 else 0

    for y in range(Hb):
        i = y * Ha / Hb
        i0 = math.floor(i)
        i1 = min(i0 + 1, Ha-1)
        mi = (i - i0)

        for x in range(Wb):
            j = x * Wa / Wb
            j0 = math.floor(j)
            j1 = min(j0 + 1, Wa-1)
            mj = (j - j0)

            B[y][x] = (A[i0][j0] * (1.-mi) + A[i1][j0] * mi) * (1.-mj) + \
                      (A[i0][j1] * (1.-mi) + A[i1][j1] * mi) * mj


def print_it(X):
    for x in X:
        print(", ".join(map(str, x)))

A = [ [ i*4+j for j in range(4) ] for i in range(4) ]

B = [ [0] * 3 for i in range(3) ]

resize(A, B)

print_it(A)
print_it(B)
