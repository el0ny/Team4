from py_modules.graph import *
from math import pi
from graphModule import getFragments, getAllowedFaces, getAlphaPath, newPosition, calculateDistances
from py_modules.draw import get_face_coordinates


def cycle_to_graph(graph, cycle):
    subgraph = Graph()
    point_pairs = []
    for i in range(len(cycle)):
        point_pairs.append([cycle[i - 1], cycle[i]])
        subgraph.points[cycle[i - 1]] = graph.points[cycle[i - 1]]
    lines = graph.get_line_by_points(point_pairs)
    subgraph.lines = lines
    return subgraph


def prettify(graph, subgraph, points):
    while True:
        fragments = getFragments(graph.get_lines(), subgraph.get_lines())
        if not fragments:
            break
        allowed_faces_indexes = []
        for fragment in fragments:
            faces = subgraph.get_faces()
            allowed_faces_indexes.append(getAllowedFaces(sorted(fragment[0]), faces))
            if len(allowed_faces_indexes[-1]) < 2:
                break
        alpha_path = getAlphaPath(fragment[0], fragment[1])
        alpha_points = {point_idx: points[point_idx] for point_idx in alpha_path}
        subgraph.points = {**alpha_points, **subgraph.points}
        subgraph.change_face(alpha_path, allowed_faces_indexes[-1][0])
        subgraph.lines = {**graph.get_lines_by_path(alpha_path), **subgraph.lines}


def draw_planar(subgraph, points):
    face = subgraph.get_biggest_face()
    N = len(face.points_list)
    coords = get_face_coordinates(N)
    i = 0
    inner_points = dict(points)
    for point in face.points_dict.values():
        point.set_coords(coords[0][i], coords[1][i])
        del inner_points[point.idx]
        i += 1
    for point in inner_points.values():
        point.set_coords(random.randrange(screen_width // 2 - 150, screen_width // 2 + 150),
                         random.randrange(screen_height // 2 - 150, screen_height // 2 + 150))

    n = len(points)
    const = get_const(n)
    delta = 1
    old_coords = {}
    cool = get_cool(n, i)
    periphericity = calculateDistances(subgraph.get_lines(), face.get_points())
    while 1:
        for point in inner_points.values():
            old_coords[point.idx] = point.coordinates
        for _ in range(10):
            new_coords = {}
            for point in inner_points.values():
                neighbours = [neighbour.coordinates for neighbour in point.adjacent_points]
                new_coords[point.idx] = newPosition(point.coordinates, neighbours, 4 * cool, const)
            for point in inner_points.values():
                point.set_coords(new_coords[point.idx][0], new_coords[point.idx][1])
        stop = True
        for point in inner_points.values():
            if abs(old_coords[point.idx][0] - point.coordinates[0]) > delta or abs(
                    old_coords[point.idx][1] - point.coordinates[1]) > delta:
                stop = False
        if stop:
            break


def get_const(n):
    return (n/pi)**0.5


def get_cool(n, i):
    return (pi/n)**0.5/(1 + pi / n * i ** 1.5)



