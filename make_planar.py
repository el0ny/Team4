from graph import *


def cycle_to_graph(points, cycle):
    for i in range(len(cycle)):
        adjacent_points = [cycle[i-2], cycle[i]]
        points[i-1].set_adjacent_points(adjacent_points)
    return points


points = [Point(1), Point(2), Point(5)]
face = Face(points)
out_face = face

