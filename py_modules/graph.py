import pygame
import random


screen_width = 1600
screen_height = 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (225, 225, 0)
RED = (225, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
colors = [YELLOW, RED, GREEN, BLUE, WHITE]


class Point:
    def __init__(self, idx, post_idx=None, coordinates=None):
        self.idx = idx
        self.post_idx = post_idx
        self.original_coordinates = coordinates
        self.coordinates = coordinates
        self.adjacent_points = []
        self.faces = []
        self.post = None
        self.home = False
        self.scale = 1
        self.selected = False

    def set_coords(self, x, y):
        self.original_coordinates = [x, y]
        self.coordinates = [x, y]

    def set_adjacent_points(self, points):
        self.adjacent_points = points

    def draw(self, surface: pygame.Surface, screen):
        type = 0

        # pygame.draw.rect(screen, BLACK, (screen_width - 400, screen_height - 500, 400, 500), 0)
        if self.post is not None:
            if self.selected:
                info = self.post.get_info()
                font = pygame.font.SysFont('arial', 20)
                i = 0
                for key, string in info.items():
                    text1 = font.render(key, True, WHITE)
                    text2 = font.render(string, True, WHITE)
                    screen.blit(text1, (screen_width - 400, screen_height - 20 - i))
                    screen.blit(text2, (screen_width - 200, screen_height - 20 - i))
                    i += 30
            type = self.post.type
        size = 5
        if self.home:
            size = 10
        if self.selected:
            type = 4
        pygame.draw.circle(surface, colors[type], (int(self.coordinates[0]), int(self.coordinates[1])), size)


class Line:
    def __init__(self, points, idx=None, length=None):
        self.idx = idx
        self.length = length
        self.points = points

    def get_points(self):
        return [point.idx for point in self.points]

    def draw(self, screen):
        # font = pygame.font.SysFont('arial', 10)
        # text = font.render(str(self.idx), True, WHITE)
        #
        # coordinates = [0, 0]
        # coordinates[0] = (self.points[0].coordinates[0] + self.points[1].coordinates[0]) / 2
        # coordinates[1] = (self.points[0].coordinates[1] + self.points[1].coordinates[1]) / 2
        # screen.blit(text, (int(coordinates[0]), int(coordinates[1])))

        pygame.draw.aaline(screen, WHITE, (int(self.points[0].coordinates[0]),
                                           int(self.points[0].coordinates[1])),
                           (int(self.points[1].coordinates[0]),
                            int(self.points[1].coordinates[1])))


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

    def get_biggest_face(self):
        faces_count = {self.faces.index(face): len(face.points_list) for face in self.faces}
        return self.faces[max(faces_count, key=faces_count.get)]

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

    def draw(self, surface, screen):
        # for point in self.points.values():
        #     if not point.coordinates:
        #         point.set_coords(random.randrange(screen_width), random.randrange(screen_height))

        for point in self.points.values():
            point.draw(surface,screen)
        for line in self.lines.values():
            line.draw(surface)

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
            point.coordinates[0]+=x
            point.coordinates[1]+=y

    def zoom(self, scale):
        for point in self.points.values():

            point.coordinates[0] = point.coordinates[0]/point.scale*scale
            point.coordinates[1] = point.coordinates[1]/point.scale*scale
            point.scale = scale


class Post:
    def __init__(self, post_dict: dict):
        self.name = post_dict['name']
        self.idx = post_dict['point_idx']
        self.post_idx = post_dict['idx']
        self.type = post_dict['type']
        if self.type == 1:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.population = (post_dict['population'], post_dict['population_capacity'])
            self.product = (post_dict['product'], post_dict['product_capacity'])
        elif self.type == 2:
            self.product = (post_dict['product'], post_dict['product_capacity'])
            self.replenishment = post_dict['replenishment']
        elif self.type == 3:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.replenishment = post_dict['replenishment']

    def get_info(self) -> dict:
        info = {'name': self.name}
        if self.type == 1:
            info['armor'] = '{0}/{1}'.format(self.armor[0], self.armor[1])
            info['population'] = '{0}/{1}'.format(self.population[0], self.population[1])
            info['product'] = '{0}/{1}'.format(self.product[0], self.product[1])
        elif self.type == 2:
            info['replenishment'] = '{0}'.format(self.replenishment)
            info['product'] = '{0}/{1}'.format(self.product[0], self.product[1])
        elif self.type == 3:
            info['replenishment'] = '{0}'.format(self.replenishment)
            info['armor'] = '{0}/{1}'.format(self.armor[0], self.armor[1])
        return info

    def update(self, post_dict: dict):
        if self.type == 1:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.population = (post_dict['population'], post_dict['population_capacity'])
            self.product = (post_dict['product'], post_dict['product_capacity'])
        elif self.type == 2:
            self.product = (post_dict['product'], post_dict['product_capacity'])
            # self.replenishment = post_dict['replenishment']
        elif self.type == 3:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            # self.replenishment = post_dict['replenishment']


class Train:
    def __init__(self, train_dict: dict):
        self.idx = train_dict['idx']
        # self.fuel = (train_dict['fuel'], train_dict['fuel_capacity'])
        self.goods = (train_dict['goods'], train_dict['goods_capacity'])
        self.line_idx = train_dict['line_idx']
        self.position = train_dict['position']
        self.speed = train_dict['speed']
        self.line = None
        self.coordinates = [0, 0]

    def set_line(self, line: Line):
        self.line = line

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (0, 0, 100, 100), 0)
        font = pygame.font.SysFont('arial', 20)
        text = font.render(str(self.line_idx) + ' ' + str(self.position) + ' ' + str(self.speed), True, WHITE)
        screen.blit(text, (0, 0))
        self.coordinates[0] = (self.line.points[0].coordinates[0] + self.line.points[1].coordinates[0]) / 2
        self.coordinates[1] = (self.line.points[0].coordinates[1] + self.line.points[1].coordinates[1]) / 2
        pygame.draw.circle(screen, YELLOW, (int(self.coordinates[0]), int(self.coordinates[1])), 5, 0)

    def get_possible_lines(self):

        return self.line_idx

    def update(self, train_dict: dict):
        self.goods = (train_dict['goods'], train_dict['goods_capacity'])
        self.line_idx = train_dict['line_idx']
        self.position = train_dict['position']
        self.speed = train_dict['speed']