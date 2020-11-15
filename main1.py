import pygame
import json
from graph import Graph, Point, Line, Face
from graphModule import getCycle, getFragments, getAllowedFaces, getAlphaPath
from make_planar import cycle_to_graph
from draw import get_face_coordinates


screen_width = 1600
screen_height = 900
WHITE = (255, 255, 255)
YELLOW = (225, 225, 0)


def main():
    with open("files/small_graph.json", "r") as read_file:
        raw_graph = json.load(read_file)


    points = {}
    for point in raw_graph['points']:
        points[point['idx']] = Point(point['idx'], point['post_idx'])
    lines = {}
    for line in raw_graph['lines']:
        point_list = [points[point] for point in line['points']]
        lines[line['idx']] = Line(point_list, line['idx'], line['length'] )

    graph = Graph(points, lines, raw_graph['name'], raw_graph['idx'])

    cycle = getCycle(graph.get_lines())
    subgraph = cycle_to_graph(graph, cycle)
    subgraph.faces.append(Face(subgraph.points, cycle))
    subgraph.faces.append(Face(subgraph.points, cycle))
    while True:
        fragments = getFragments(graph.get_lines(), subgraph.get_lines())
        if not fragments:
            break
        allowed_faces_indexes = []
        for fragment in fragments:
            break_fragment = fragment
            faces = subgraph.get_faces()
            # allowed_faces_indexes.append(getAllowedFaces(sorted(fragment[0]), faces))
            allowed_faces_indexes.append(getAllowedFaces(sorted(fragment[0]), [sorted(face) for face in faces]))
            if len(allowed_faces_indexes[-1]) < 2:
                break
        alpha_path = getAlphaPath(break_fragment[0], break_fragment[1])
        alpha_points = {point_idx: points[point_idx] for point_idx in alpha_path}
        subgraph.points = {**alpha_points, **subgraph.points}
        subgraph.change_face(alpha_path, allowed_faces_indexes[-1][0])
        subgraph.lines = {**graph.get_lines_by_path(alpha_path), **subgraph.lines}
        print("test")
    N = len(cycle)
    coords = get_face_coordinates(N)
    i = 0
    for point in graph.faces[0].points_dict:

        point.set_coords(coords[0][i], coords[1][i])
        i += 1
    pygame.init()
    sc = pygame.display.set_mode((screen_width, screen_height))

    graph.draw(sc)

    # pygame.draw.arc(sc, WHITE, [80,10,250,1200], 3*math.pi/2, math.pi, 2)

    pygame.display.update()

    while 1:
        pygame.time.delay(1000)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
        main()
