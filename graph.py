import pygame
import random


screen_width = 1600
screen_height = 900
WHITE = (255, 255, 255)
YELLOW = (225, 225, 0)

class Point:
    def __init__(self, idx, post_idx, coordinates=None):
        self.idx = idx
        self.post_idx = post_idx
        self.coordinates = coordinates

    def set_coords(self, x, y):
        self.coordinates = [x, y]

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.coordinates, 10)


class Line:
    def __init__(self, idx, length, points):
        self.idx = idx
        self.length = length
        self.points = points

    def draw(self, screen):
        pygame.draw.aaline(screen, WHITE, self.points[0].coordinates, self.points[1].coordinates)


class Graph:
    def __init__(self, graph_dict):
        self.points = {}
        self.lines = {}
        self.name = graph_dict['name']
        self.idx = graph_dict['idx']
        for point in graph_dict['points']:
            self.points[point['idx']] = Point(point['idx'], point['post_idx'])
        for line in graph_dict['lines']:
            point_list = [self.points[point] for point in line['points']]
            self.lines[line['idx']] = Line(line['idx'], line['length'], point_list)

    def draw(self, screen):
        for point in self.points.values():
            point.set_coords(random.randrange(screen_width), random.randrange(screen_height))
        for point in self.points.values():
            point.draw(screen)
        for line in self.lines.values():
            line.draw(screen)