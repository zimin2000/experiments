import heapq

def f(A):
    Q = []
    M = 0

    for i in range(len(A)):
        heapq.heappush(Q, (A[i][0], 0, i))
        M = max(M, A[i][0])

    result = M - Q[0][0]

    print(M, result)

    while len(Q) > 0:
        m, n, i = heapq.heappop(Q)

        n += 1

        if n < len(A[i]):
            heapq.heappush(Q, (A[i][n], n, i))

            M = max(M, A[i][n])
            result = min(result, M - Q[0][0])

        else:
            break

    return result


print f([[1,2,3], [20,40,60]])
