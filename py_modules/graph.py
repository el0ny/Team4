""" This module contains the main classes """
from py_modules.face import Face

screen_width = 1600
screen_height = 900


class Graph:
    def __init__(self, points: dict = None, lines=None, name=None, idx=None):
        self.points = {}
        self.lines = {}
        self.name = name
        self.idx = idx
        self.faces = []
        self.trains = {}
        self.posts = {}
        self.home = None
        if points is not None:
            self.points = points
        if lines is not None:
            self.lines = lines
        self.rating = 0
        self.scale = 1

    def get_biggest_face(self):
        faces_count = {self.faces.index(face): len(face.points_list) for face in self.faces}
        return self.faces[max(faces_count, key=faces_count.get)]

    def get_lines_by_path(self, path: list):
        pairs = [[path[i], path[i + 1]] for i in range(len(path) - 1)]
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

    def draw(self, surface, screen):
        for line in self.lines.values():
            line.draw(surface)
        for point in self.points.values():
            point.draw(surface, screen)
        # self.display_rating(screen)
        for train in self.trains.values():
            train.set_line(self.lines[train.line_idx])
            train.draw(screen, surface)

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

    def move(self, x, y):
        for point in self.points.values():
            point.coordinates[0] += x
            point.coordinates[1] += y

    def zoom(self, scale_increase):
        if 1 <= self.scale + scale_increase <= 3:
            self.scale += scale_increase
        for point in self.points.values():
            point.coordinates[0] = point.coordinates[0] / point.scale * self.scale
            point.coordinates[1] = point.coordinates[1] / point.scale * self.scale
            point.scale = self.scale

    # def display_rating(self, screen):
    #     font = pygame.font.SysFont('arial', 20)
    #     text1 = font.render(str(self.rating), True, WHITE)
    #     screen.blit(text1, (screen_width - 200, 320))
    #
    # def find_optimal_path(self, point1_idx: int, point2_idx: int):
    #     return getOptimalPath(point1_idx, point2_idx,
    #                           [[line.idx, line.length, line.get_points()] for line in self.lines.values()])
