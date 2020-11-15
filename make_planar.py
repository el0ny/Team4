from graph import *


def cycle_to_graph(graph, cycle):
    subgraph = Graph()
    point_pairs = []
    for i in range(len(cycle)):
        point_pairs.append([cycle[i - 1], cycle[i]])
        subgraph.points[cycle[i - 1]] = graph.points[cycle[i - 1]]
        adjacent_points = [cycle[i-2], cycle[i]]
        subgraph.points[cycle[i - 1]].set_adjacent_points(adjacent_points)

    lines = graph.get_line_by_points(point_pairs)
    subgraph.lines = lines
    return subgraph


points = [Point(1), Point(2), Point(5)]


