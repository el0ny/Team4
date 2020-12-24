""" This module contains the main classes """
import os
import sys
import random

import pygame

from graphModule import getOptimalPath

screen_width = 1600
screen_height = 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (225, 225, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 100)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
colors = [YELLOW, RED, GREEN, BLUE, WHITE]
type_colors = {"armor": [BLUE, DARK_BLUE], "population": [RED, DARK_RED], "product": [GREEN, DARK_GREEN]}
train_colors = {1: (255, 255, 120), 2: (120, 255, 255), 3: (255, 120, 255)}


class Point:
    def __init__(self, idx: int, post_idx: int = None, coordinates: list = None):
        self.idx = idx
        self.post_idx = post_idx
        self.original_coordinates = coordinates
        self.coordinates = coordinates  # zoomed
        self.adjacent_points = []
        self.faces = []
        self.post = None
        self.home = False
        self.scale = 1
        self.selected = False

    def set_coords(self, x: int, y: int):
        self.original_coordinates = [x, y]
        self.coordinates = [x, y]

    def set_adjacent_points(self, points):
        self.adjacent_points = points

    def draw_table(self, info, screen):
        font = pygame.font.SysFont('arial', 20)
        i = 0
        for key, string in info.items():
            text1 = font.render(key, True, WHITE)
            if len(string) == 2:
                pygame.draw.rect(screen, type_colors[key][1], (screen_width - 200, screen_height - 20 - i, 100, 20))
                text2 = font.render('{0}/{1}'.format(string[0], string[1]), True, WHITE)
                pygame.draw.rect(screen, type_colors[key][0], (
                    screen_width - 200, screen_height - 20 - i, int(100 * string[0] / string[1]), 20))
            else:
                text2 = font.render(str(string[0]), True, WHITE)
            screen.blit(text1, (screen_width - 400, screen_height - 20 - i))
            screen.blit(text2, (screen_width - 200, screen_height - 20 - i))
            i += 30

    def draw(self, surface: pygame.Surface, screen):
        size = 5
        if self.home:
            size *= 2
        if self.post is not None:
            # image_rect = self.post.image.get_rect()
            # image_rect.center = (int(self.coordinates[0]), int(self.coordinates[1]))
            # surface.blit(self.post.image, image_rect)
            info = self.post.get_info()
            color_type = self.post.type
        else:
            info = {"idx": [self.idx]}
            color_type = 0
        if self.selected:
            self.draw_table(info, screen)
            color_type = 4
        pygame.draw.circle(surface, colors[color_type], (int(self.coordinates[0]), int(self.coordinates[1])), size)


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

        pygame.draw.aaline(screen, WHITE, (int(self.points[0].coordinates[0]), int(self.points[0].coordinates[1])),
                           (int(self.points[1].coordinates[0]), int(self.points[1].coordinates[1])))


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


class Post:
    def __init__(self, post_dict: dict):
        self.name = post_dict['name']
        self.idx = post_dict['point_idx']
        self.post_idx = post_dict['idx']
        self.type = post_dict['type']
        if self.type == 1:
            # self.image_path = "pictures/city.png"
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.population = (post_dict['population'], post_dict['population_capacity'])
            self.product = (post_dict['product'], post_dict['product_capacity'])
            self.upgrade_cost = post_dict['next_level_price']
        elif self.type == 2:
            # self.image_path = "pictures/shop.png"
            self.resource = (post_dict['product'], post_dict['product_capacity'])
            self.replenishment = post_dict['replenishment']
        elif self.type == 3:
            # self.image_path = "pictures/armour.png"
            self.resource = (post_dict['armor'], post_dict['armor_capacity'])
            self.replenishment = post_dict['replenishment']

        # image = pygame.image.load(self.resource_path()).convert_alpha()
        # self.image = pygame.transform.scale(image, (20, 20))

    # def resource_path(self):
    #     """ Get absolute path to resource, works for dev and for PyInstaller """
    #     try:
    #         # PyInstaller creates a temp folder and stores path in _MEIPASS
    #         base_path = sys._MEIPASS
    #     except Exception:
    #         base_path = os.path.abspath(".")
    #
    #     return os.path.join(base_path, self.image_path)

    def get_info(self) -> dict:
        info = {'name': [self.name], 'idx': [self.idx]}
        if self.type == 1:
            info['armor'] = [self.armor[0], self.armor[1]]
            info['population'] = [self.population[0], self.population[1]]
            info['product'] = [self.product[0], self.product[1]]
        elif self.type == 2:
            info['replenishment'] = [self.replenishment]
            info['product'] = [self.resource[0], self.resource[1]]
        elif self.type == 3:
            info['replenishment'] = [self.replenishment]
            info['armor'] = [self.resource[0], self.resource[1]]
        return info

    def update(self, post_dict: dict):
        if self.type == 1:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.population = (post_dict['population'], post_dict['population_capacity'])
            self.product = (post_dict['product'], post_dict['product_capacity'])
            self.upgrade_cost = post_dict['next_level_price']
        elif self.type == 2:
            self.product = (post_dict['product'], post_dict['product_capacity'])
        elif self.type == 3:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])

    def get_income(self, last_visit, turns):
        income = min((turns - last_visit) * self.replenishment, self.resource[1])
        return income


class Train:
    def __init__(self, train_dict: dict):
        self.idx = train_dict['idx']
        self.goods = (train_dict['goods'], train_dict['goods_capacity'])
        self.line_idx = train_dict['line_idx']
        self.position = train_dict['position']
        self.speed = train_dict['speed']
        self.line = None
        self.coordinates = [0, 0]
        self.font = pygame.font.SysFont('arial', 20)
        self.goods_type = train_dict['goods_type']
        self.upgrade_cost = train_dict['next_level_price']

    def set_line(self, line: Line):
        self.line = line

    def draw(self, screen, surface):
        threshold = (self.idx-1) * 150
        info = {'current line': [str(self.line_idx)], 'position': [self.position, self.line.length],
                'type of goods': [str(self.goods_type)], 'goods': self.goods}
        i = 5
        for key, value in info.items():
            if len(value) == 1:
                text2 = self.font.render(value[0], True, WHITE)
            else:
                text2 = self.font.render('{0}/{1}'.format(value[0], value[1]), True, WHITE)
            text1 = self.font.render(key, True, WHITE)
            screen.blit(text1, (1300, threshold+i))
            screen.blit(text2, (1500, threshold+i))
            i += 30
        step_x = (self.line.points[1].coordinates[0] - self.line.points[0].coordinates[0]) / self.line.length
        step_y = (self.line.points[1].coordinates[1] - self.line.points[0].coordinates[1]) / self.line.length
        self.coordinates[0] = self.line.points[0].coordinates[0] + step_x * self.position
        self.coordinates[1] = self.line.points[0].coordinates[1] + step_y * self.position
        pygame.draw.rect(screen,
                         train_colors[self.idx],
                         (1250, threshold+5, 300, 120), 1)
        pygame.draw.rect(surface,
                         train_colors[self.idx],
                         (int(self.coordinates[0]) - 8, int(self.coordinates[1]) - 8,
                          16,
                          16), 1)

    def get_possible_lines(self):
        return self.line_idx

    def update(self, train_dict: dict):
        self.goods = (train_dict['goods'], train_dict['goods_capacity'])
        self.line_idx = train_dict['line_idx']
        self.position = train_dict['position']
        self.speed = train_dict['speed']
        self.goods_type = train_dict['goods_type']
        self.upgrade_cost = train_dict['next_level_price']


class Dispatcher:
    def __init__(self, graph: Graph, connector):
        self.graph = graph
        self.posts = {1: {}, 2: {}, 3: {}}
        self.rem_length = 0
        self.train_path = None
        self.best_paths = {}
        self.finite_paths = {2: {}, 3: {}}
        self.train_tasks = {}
        self.income_losses = {2: [], 3: []}
        self.post_rating = {2: [], 3: []}
        self.arrival_dict = {}
        self.home = graph.home
        self.connector = connector
        self.train_paths = {40: {2: [], 3: []}, 80: {2: [], 3: []}, 160: {2: [], 3: []}}

        self.upgrade_dict = {'posts': [], 'trains': []}
        for idx, post in self.graph.posts.items():
            self.posts[post.post.type][post.idx] = post

    def count_start_income(self):
        for post_type, paths in self.finite_paths.items():
            for path_idx, path in paths.items():
                path.get_income()
                for key in self.train_paths.keys():
                    # if path.income >= key:
                    self.train_paths[key][post_type].append(path_idx)

    def get_best_path(self, point_a, point_b, train_lines=None, excluded_points=None):
        """
        Finds best way between two points
        :param point_a: start point
        :param point_b: finish point
        :param train_lines: if not None than start point is a train
        :param excluded_points: points to be removed from the path
        :return: list representation of the path
        """
        lines_list = []
        for line in self.graph.lines.values():
            points = line.get_points()
            if excluded_points is None or (
                    points[0] not in excluded_points.keys() and points[1] not in excluded_points.keys()):
                lines_list.append([line.idx, line.length, line.get_points()])
        if train_lines is not None:
            lines_list += train_lines
        return getOptimalPath(point_a, point_b, lines_list)

    def get_path_to_point(self, point_idx, train_idx):
        """
        Finds optimal path from current train position to a point
        :param point_idx: destination point
        :param train_idx: train
        :return: a path
        """
        lines = [[-1, self.graph.trains[train_idx].position,
                  [self.graph.trains[train_idx].line.points[0].idx, 0]],
                 [-2, self.graph.trains[train_idx].line.length - self.graph.trains[train_idx].position,
                  [0, self.graph.trains[train_idx].line.points[1].idx]]]
        best_path = self.get_best_path(0, point_idx, lines)
        best_path[0][0] = self.graph.trains[train_idx].line.idx
        return best_path

    def do_tasks(self):
        """
        Does tasks for all trains and assigns new if all tasks are done
        :return: None
        """
        for train, paths in self.train_tasks.items():
            if paths[0].move(train) is False:
                self.assign_tasks(train)
                # paths.pop(0)
                # if paths:
                #     paths[0].move(train)
                # else:
                #     self.assign_tasks(train)
                #     print('recur')
                #     self.do_tasks()
                #     print('recur2')

    def add_path(self, start, end, post_type, excluded_points=None, post=None):
        path = self.get_best_path(start, end, excluded_points=excluded_points)
        distance = 0
        posts = {}
        for line in path:
            line.append(self.graph.lines[line[0]].length)
            distance += line[2]
            point = self.graph.lines[line[0]].points[0] if line[1] == -1 else self.graph.lines[line[0]].points[1]
            if point.post is not None and post_type == point.post.type:
                posts[distance] = point.post
        self.best_paths[(start, end)] = Path(path, start, end, distance, self.connector, post_type, posts)

    def get_paths(self, post_type, start):
        """
        Creates the paths to posts and the returning ones
        :param post_type: post type
        :param start: start point (home town)
        :return: None
        """
        comeback_distances = []
        for idx, post in self.posts[post_type].items():
            excluded_points = self.posts[2] if post_type == 3 else self.posts[3]
            self.add_path(start, idx, post_type, excluded_points=excluded_points, post=self.graph.points[idx])
            self.add_path(idx, start, post_type)
            for idx2, post2 in self.posts[post_type].items():
                if idx2 != idx:
                    self.add_path(idx, idx2, post_type, post=self.graph.points[idx2])
        for idx, post in self.posts[post_type].items():
            for idx2, post2 in self.posts[post_type].items():
                if idx2 != idx:
                    self.finite_paths[post_type][(start, idx, idx2, start)] = \
                        self.combine_paths(self.best_paths[(start, idx)],
                                           self.best_paths[(idx, idx2)],
                                           self.best_paths[(idx2, start)])
                else:
                    self.finite_paths[post_type][(start, idx, start)] = \
                        self.combine_paths(self.best_paths[(start, idx)],
                                           self.best_paths[(idx, start)])
                    # print(str(start)+' '+str(idx)+' '+str(idx2))
                    # print(self.best_paths[(start, idx)].length+self.best_paths[(idx, idx2)].length+self.best_paths[(idx2, start)].length)
                    # print(self.posts[post_type][idx].post.resource[1]+self.posts[post_type][idx2].post.resource[1])
            # comeback_distances.append((idx, distance + distance_back))
        # comeback_distances.sort(key=lambda full_distance: full_distance[1])
        # self.post_rating[post_type] = comeback_distances

    def combine_paths(self, *paths):
        path_list = []
        length = 0
        posts = {}
        for path in paths:
            path_list += path.path
            for turn, post in path.posts.items():
                posts[turn + length] = post
            length += path.length
        return Path(path_list, paths[0].start, paths[0].start, length, paths[0].connector, path.post_type, posts)

    def count_income(self, post_type, train_idx):
        """
        Creates a list of income losses if specific train will drive to specific post type
        :param post_type: type of the post
        :param train_idx: train idx
        :return: None
        """
        self.count_start_income()
        for train_capacity, types in self.train_paths.items():
            for post_type, paths_list in types.items():
                paths_list.sort(key=lambda key: min(self.finite_paths[post_type][key].income, train_capacity) /
                                                    self.finite_paths[post_type][key].length, reverse=True)
                print([min(self.finite_paths[post_type][key].income, train_capacity) /
                      self.finite_paths[post_type][key].length for key in paths_list])

        # for post_pair in self.post_rating[post_type]:
        #     turns = post_pair[1]
        #     if self.posts[post_type][post_pair[0]].post.resource[1] >= self.graph.trains[train_idx].goods[1]:
        #         estimated_income = self.graph.trains[train_idx].goods[1]
        #     else:
        #         pass
        #     income = self.estimated_consumption(turns, 1) - estimated_income
        #     self.income_losses[post_type].append((post_pair[0], income))
        # self.income_losses[post_type].sort(key=lambda loss: loss[1])

    def estimated_consumption(self, turns, population):
        """
        Function to estimate the consumption of products
        :param population: start population
        :param turns: number of turns to estimate
        :return: consumed products
        """

        consumption = turns * population

        num_of_cycles = turns // 90
        return consumption

    def get_armor(self):
        best_path_idx = self.train_paths[self.graph.trains[1].goods[1]][3][0]
        self.train_tasks[1] = [self.finite_paths[3][best_path_idx].copy()]

    def get_products(self):
        """
        Creates the most optimal task for one train to deliver products
        :return: None
        """
        best_path_idx = self.train_paths[self.graph.trains[2].goods[1]][2][0]
        self.train_tasks[2] = [self.finite_paths[2][best_path_idx].copy()]

    def prepare(self):
        """
        Makes preparations of the dispatcher for example optimal paths
        :return: None
        """
        self.get_paths(2, self.graph.home.idx)
        self.get_paths(3, self.graph.home.idx)
        self.count_income(2, 1)
        # self.count_income(3, 1)

        self.assign_tasks(1)
        self.assign_tasks(2)

    def upgrade(self):
        self.connector.upgrade(self.upgrade_dict)
        for value in self.upgrade_dict.values():
            value.clear()

    def can_upgrade(self, train_idx, home=False):
        if home:
            if self.graph.home.post.upgrade_cost is not None and\
                    self.graph.home.post.upgrade_cost <= self.graph.home.post.armor[0]:
                return True
            else:
                return False
        if (1 not in self.train_tasks or self.train_tasks[1]) \
                and self.graph.trains[train_idx].upgrade_cost is not None \
                and self.graph.trains[train_idx].upgrade_cost <= self.graph.home.post.armor[0]:
            return True
        return False

    def assign_tasks(self, train_idx):
        """
        THis function will choose what is optimal to do in the future
        :return: None
        """

        if self.can_upgrade(train_idx):
            self.upgrade_dict['trains'].append(train_idx)
            self.graph.trains[train_idx].goods = (0, self.graph.trains[train_idx].goods[1]*2)
            self.graph.home.post.armor = (self.graph.home.post.armor[0]-self.graph.trains[train_idx].upgrade_cost, self.graph.home.post.armor[1])
            self.graph.trains[train_idx].upgrade_cost *= 2
        if self.can_upgrade(1, True):
            self.upgrade_dict['posts'].append(74)
            self.graph.home.post.upgrade_cost *= 2
        self.upgrade()
        if train_idx == 1:
            self.get_armor()
        else:
            self.get_products()


class Path:
    def __init__(self, path, start, end, length, connector, post_type=None, posts=None):
        self.path = path
        self.start = start
        self.end = end
        self.length = length
        self.connector = connector
        self.current_track = [0, 0, 0]  # line_id, direction, length
        self.current_track_idx = 0
        self.posts = posts  # maybe list
        self.arrival_points = {}  # point_idx: arrival_time
        self.stop_dict = {}  # {point_idx: time}
        self.income = 0
        self.lines = {}  # line_idx: Line
        self.post_type = post_type

    def copy(self):
        return Path(self.path, self.start, self.end, self.length, self.connector, self.post_type, self.posts)

    def get_income(self, full=True):
        arrival_time = {}
        for turn, post in self.posts.items():
            if full:
                if post.idx not in arrival_time:
                    self.income += post.resource[1]
                else:
                    self.income += min((turn - arrival_time[post.idx]) * post.replenishment, post.resource[1])
                arrival_time[post.idx] = turn

    def turns_wait(self, train: Train):
        # best_replenishment = sorted(self.posts, key=lambda post: post.replenishment, reverse=True)
        best_replenishment = max(self.posts, key=lambda key: self.posts[key].replenishment)
        best_rep = best_replenishment[0].replenishment
        if best_rep * self.length >= self.income:
            turns_to_wait = max((train.goods[1] - self.income) // best_rep, 0)
            if turns_to_wait > 0:
                # need to update income from other posts
                self.income += turns_to_wait * best_rep
                self.length += turns_to_wait
                if (train.goods[1] - self.income) * self.length >= self.income:
                    self.income += train.goods[1]
                    self.length += 1
                    turns_to_wait += 1
                self.stop_dict[best_replenishment[0].idx] = turns_to_wait

    def should_stop(self):
        # points = self.lines[self.current_track[0]].points
        # point = points[0] if self.current_track[1] == 1 else points[1]
        # if point.idx in self.stop_dict:
        #     self.stop_dict[point.idx] -= 1
        #     if self.stop_dict[point.idx] == 0:
        #         del self.stop_dict[point.idx]
        #     return True
        return False

    def move(self, train_idx):
        if self.current_track[2] <= 0:
            # if self.current_track_idx == len(self.path):
            #     return False
            self.current_track = list(self.path[self.current_track_idx])
            if not self.should_stop():
                self.connector.move_train(self.current_track[0], self.current_track[1], train_idx)
                self.current_track_idx += 1
        self.current_track[2] -= 1
        if self.current_track[2] <= 0 and self.current_track_idx == len(self.path):
            print('end_path')
            return False
        return True
