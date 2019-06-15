import math

class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices
        self.n = len(vertices)
        self.checked_vertices = []

    def solve(self):
        diagonal_edges = self.cut_poly()
        for diag in diagonal_edges:
            print diag
        # for diag in diagonal_edges:
        #     graph.add(diag)
        # graph = graph.maximum_independent_set()
        # graph = graph.minimum_vertex_cover()
        # polygon_arr = graph.get_polygons()
        num_of_rects = 0
        # for poly in polygon_arr:
        #     num_of_rects = poly.cut()
        return num_of_rects

    def cut_poly(self):
        # 0th vertex
        fst = self.vertices[self.n-1]
        snd = self.vertices[0]
        trd = self.vertices[1]
        diagonal_edges = []
        if self.concave(fst[0], fst[1],
                   snd[0], snd[1],
                   trd[0], trd[1]):
            self.add_to_diagonal(fst, snd, trd, diagonal_edges)

        # from 1st to (n-1)st vertices
        for i in range(1, self.n - 1):
            fst = self.vertices[i - 1]
            snd = self.vertices[i]
            trd = self.vertices[i + 1]
            if self.concave(fst[0], fst[1],
                   snd[0], snd[1],
                   trd[0], trd[1]):
                self.add_to_diagonal(fst, snd, trd, diagonal_edges)
        
        # nth vertex
        fst = self.vertices[self.n - 2]
        snd = self.vertices[self.n - 1]
        trd = self.vertices[0]
        if self.concave(fst[0], fst[1],
                   snd[0], snd[1],
                   trd[0], trd[1]):
            self.add_to_diagonal(fst, snd, trd, diagonal_edges)

        return diagonal_edges

    def add_to_diagonal(self, fst, snd, trd, diagonal_edges):
        best_vert = (float('inf'), float('inf'))
        best_dist = float('inf')
        for vertex in self.vertices:
            if vertex != snd and vertex != fst and vertex != trd and (vertex[0] == snd[0] or vertex[1] == snd[1]) and snd not in self.checked_vertices and vertex not in self.checked_vertices:
                dist = self.dist(snd, vertex)
                if dist < best_dist:
                    best_vert = vertex
                    best_dist = dist

        if snd == (float('inf'), float('inf')) or best_vert == (float('inf'), float('inf')):
            return
        self.checked_vertices += [snd]
        self.checked_vertices += [best_vert]
        diagonal_edges += [(snd, best_vert)]

    def dist(self, v1, v2):
        return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)


    def concave(self, x1, y1, x2, y2, x3, y3):
        area_sum = 0
        area_sum += x1 * (y3 - y2)
        area_sum += x2 * (y1 - y3)
        area_sum += x3 * (y2 - y1)
        if area_sum >= 0:
            return True
        return False

def main():
    vertices = [(0, 0),
                (1, 0),
                (1, 1.5),
                (2, 1.5),
                (2, 2.5),
                (1, 2.5),
                (1, 3),
                (0, 3),
                (0, 2),
                (-1, 2),
                (-1, 1),
                (0, 1),
                ]
    Polygon(vertices).solve()
    return

if __name__ == "__main__":
    main()