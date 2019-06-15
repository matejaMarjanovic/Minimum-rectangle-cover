def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return int(ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D))

def XOR(s1, s2):
    res = []
    for s in s1:
        if not s in s2:
            res += [s]

    for s in s2:
        if not s in s1:
            res += [s]

    return res

class Graph:
    def __init__(self, diagonal_edges, is_horizontal):
        self.side = is_horizontal
        self.adj_matrix = self.make_bipartite(diagonal_edges)

    def make_bipartite(self, diagonal_edges):
        n = len(diagonal_edges)
        adj_matrix = [[0 for i in range(n)] for j in range(n)]
        
        for i in range(n):
            for j in range(n):
                adj_matrix[i][j] = intersect(diagonal_edges[i][0], diagonal_edges[i][1], diagonal_edges[j][0], diagonal_edges[j][1])
                # print adj_matrix[i][j],
            # print
        return adj_matrix

    def maximum_independent_set(self):
        matching, x, y = self.maximum_matching()
        for m in matching.iteritems():
            print m
        # self.minimum_vertex_cover()

    def maximum_matching(self):
        matching = {}
        for u in range(len(self.adj_matrix)):
            for v in range(len(self.adj_matrix)):
                if self.adj_matrix[u][v] == 1 and v not in matching:
                    matching[v] = u
                    break
        
        while 1:
            preds = {}
            unmatched = []
            pred = dict([(u,unmatched) for u in range(len(self.adj_matrix))])
            for v in matching:
                del pred[matching[v]]
            layer = list(pred)
            
            # repeatedly extend layering structure by another pair of layers
            while layer and not unmatched:
                newLayer = {}
                for u in layer:
                    for v in range(len(self.adj_matrix)):
                        if self.adj_matrix[u][v] == 1 and v not in preds:
                            newLayer.setdefault(v,[]).append(u)
                layer = []
                for v in newLayer:
                    preds[v] = newLayer[v]
                    if v in matching:
                        layer.append(matching[v])
                        pred[matching[v]] = v
                    else:
                        unmatched.append(v)
            
            # did we finish layering without finding any alternating paths?
            if not unmatched:
                unlayered = {}
                for u in range(len(self.adj_matrix)):
                    for v in range(len(self.adj_matrix)):
                        if self.adj_matrix[u][v] == 1 and v not in preds:
                            unlayered[v] = None
                return (matching,list(pred),list(unlayered))

            # recursively search backward through layers to find alternating paths
            # recursion returns true if found path, false otherwise
            def recurse(v):
                if v in preds:
                    L = preds[v]
                    del preds[v]
                    for u in L:
                        if u in pred:
                            pu = pred[u]
                            del pred[u]
                            if pu is unmatched or recurse(pu):
                                matching[v] = u
                                return 1
                return 0

            for v in unmatched: recurse(v)




        # matched = []
        # free = []
        # for i in range(len(self.adj_matrix)):
        #     if self.side[i] == 0:
        #         free += [i]
        # P = []
        # F = []
        
        # for u in free:
        #     for v in range(len(self.adj_matrix[u])):
        #         if self.adj_matrix[u][v] == 1 and v not in F:
        #             F += [v]
        
        # for v in F:
        #     for u in range(len(self.adj_matrix[v])):
        #         if self.adj_matrix[v][u] == 1:
        #             P += [(v, u)]

        # matched = XOR(matched, P)

        # while True:
        #     for u in free:
        #         for v in range(len(self.adj_matrix[u])):
        #             if self.adj_matrix[u][v] == 1 and not v in F:
        #                 already_matched = False
        #                 for m in matched:
        #                     if v in m:
        #                         free += [m[1]]
        #                 if not already_matched:
        #                     F += [v]
        #     for v in F:
        #         ind = -1
        #         for u in range(len(self.adj_matrix[v])):
        #             if self.adj_matrix[v][u] == 1:
        #                 P += [(v, u)]
        #                 if (v, u) not in matched:
        #                     ind = F.index(v)
        #                     F = F[:ind] + F[ind+1:]
        #                     ind = free.index(u)
        #                     free = free[:ind] + free[ind+1:]

        #     matched = XOR(matched, P)

        #     if len(P) == 0:
        #         break