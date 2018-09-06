def conv1d(x, P):
    out = []

    for i in range(len(x) - len(P) + 1):
        S = 0
        for j in range(len(P)):
            S += x[i+j] * P[j]
        out.append(S)

    return out


print(conv1d([1,2,3,4,5], [1,-1]))
