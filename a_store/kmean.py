import math

# C = [[x,y],[x,y],[x,y]], prints = []
def kMean(C, points):
    clusters_x = [ [] for c in C ]
    clusters_y = [ [] for c in C ]

    for p in points:
        best_distance = None
        for i in range(len(C)):
            c = C[i]
            distance = math.hypot(c[0]-p[0], c[1]-p[1])
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_cluster = i

            clusters_x[best_cluster].append(p[0])
            clusters_y[best_cluster].append(p[1])

    return [ (sum(clusters_x[i])/len(clusters_x[i]), sum(clusters_y[i])/len(clusters_y[i])) for i in range(len(clusters_x)) ]

print(kMean([(0,0), (10,10)], [(-1,-1), (-2,-2), (20,20)]))
