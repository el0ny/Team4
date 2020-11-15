import pygame
import random


screen_width = 1600
screen_height = 900
WHITE = (255, 255, 255)
YELLOW = (225, 225, 0)


class Point:
    def __init__(self, idx, post_idx=None, coordinates=None):
        self.idx = idx
        self.post_idx = post_idx
        self.coordinates = coordinates
        self.adjacent_points = None
        self.faces = []

    def set_coords(self, x, y):
        self.coordinates = [x, y]

    def set_adjacent_points(self, points):
        self.adjacent_points = points

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.coordinates, 10)


class Line:
    def __init__(self, points, idx=None, length=None):
        self.idx = idx
        self.length = length
        self.points = points

    def get_points(self):
        return [point.idx for point in self.points]

    def draw(self, screen):
        pygame.draw.aaline(screen, WHITE, self.points[0].coordinates, self.points[1].coordinates)


class Face:
    def __init__(self, points_dict: dict, points_list: list):
        self.points_dict = points_dict
        self.points_list = points_list

    def get_points(self):
        return [point.idx for point in self.points_dict.values()]

    def get_edges(self, a, b):
        indexes = sorted([self.points_list.index(a), self.points_list.index(b)])
        first_edge = self.points_list[indexes[1]:] + self.points_list[:indexes[0]]
        second_edge = self.points_list[indexes[0]:indexes[1]]
        return [first_edge, second_edge]



class Graph:
    def __init__(self, points: dict = None, lines=None, name=None, idx=None):
        self.points = {}
        self.lines = {}
        self.name = name
        self.idx = idx
        self.faces = []
        if points is not None:
            self.points = points
        if lines is not None:
            self.lines = lines

    def get_lines_by_path(self, path: list):
        pairs = [[path[i], path[i+1]] for i in range(len(path)-1)]

        return self.get_line_by_points(pairs)

    def get_line_by_points(self, pair_points):
        pair_points = [sorted(pair) for pair in pair_points]
        lines = {}
        for key, line in self.lines.items():
            if sorted(line.get_points()) in pair_points:
                lines[key] = line
        return lines

    def get_faces(self):
        return [face.get_points() for face in self.faces]

    def get_lines(self):
        return [line.get_points() for line in self.lines.values()]

    def draw(self, screen):
        for point in self.points.values():
            if not point.coordinates:
                point.set_coords(random.randrange(screen_width), random.randrange(screen_height))
        for point in self.points.values():
            point.draw(screen)
        for line in self.lines.values():
            line.draw(screen)

    def change_face(self, alpha_path: list, face_index: int):
        edges = self.faces[face_index].get_edges(alpha_path[0], alpha_path[-1])
        if edges[1][0] == alpha_path[0]:
            edges[0], edges[1] = edges[1], edges[0]
        old_list = [point for point in alpha_path[::-1] + edges[0][1:]]
        new_list = [point for point in alpha_path + edges[1][1:]]
        old_dict = {point: self.points[point] for point in old_list}
        new_dict = {point: self.points[point] for point in new_list}
        self.faces[face_index].points_dict = old_dict
        self.faces[face_index].points_list = old_list

        self.faces.append(Face(new_dict, new_list))
