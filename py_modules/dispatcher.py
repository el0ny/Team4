from py_modules.graph import Graph
from py_modules.path import Path

from graphModule import getOptimalPath


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
            if not paths:
                continue
            if paths[0] == 'upgrade':
                self.upgrade_dict['trains'].append(train)
                self.upgrade(train)
                paths.pop(0)
            elif paths[0] == 'upgrade2':
                self.upgrade_dict['trains'].append(train)
                self.upgrade_dict['trains'].append(train)
                self.upgrade(train)
                paths.pop(0)
            elif paths[0] == 'upgrade_town':
                self.upgrade(post=True)
                paths.pop(0)
            if paths[0].move(train) is False:
                # self.assign_tasks(train)
                paths.pop(0)
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
        return start, end

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
        if len(paths) == 1:
            paths = paths[0]
        for path in paths:
            path_list += path.path
            if path.posts is not None:
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

    def get_products(self, train_idx):
        """
        Creates the most optimal task for one train to deliver products
        :return: None
        """
        best_path_idx = self.train_paths[self.graph.trains[train_idx].goods[1]][2][train_idx-2]

        self.train_tasks[train_idx] = [self.finite_paths[2][best_path_idx].copy()]
        # self.train_tasks[2][0].stop_dict[20] = 3

    def prepare(self):
        """
        Makes preparations of the dispatcher for example optimal paths
        :return: None
        """
        # self.get_paths(2, self.graph.home.idx)
        # self.get_paths(3, self.graph.home.idx)
        # self.count_income(2, 1)

        # self.count_income(3, 1)

        # self.assign_tasks(1)
        # self.upgrade()

        # self.assign_tasks(2)
        # self.assign_tasks(3)
        self.tactics_setup()
        self.tactics_assign()

    def create_path_through_points(self, *points, post_type=3):
        index = tuple(points)
        paths = []
        for i in range(len(points)-1):
            paths.append(self.add_path(points[i], points[i+1], post_type))
        self.best_paths[index] = self.combine_paths([self.best_paths[i] for i in paths])
        print(points)
        print(self.best_paths[index])
        print(index)

    def tactics_setup(self):
        self.create_path_through_points(57, 61, 101, 97, 57, post_type=3)
        self.create_path_through_points(57, 67, 90, 87, 57, post_type=2)
        self.create_path_through_points(57, 60, 90, 87, 57, post_type=2)
        self.create_path_through_points(57, 60, 90, 88, 58, 57, post_type=2)

        self.best_paths['armor'] = self.best_paths[(57, 61, 101, 97, 57)]
        self.best_paths['product1'] = self.best_paths[(57, 67, 90, 87, 57)]
        self.best_paths['product2'] = self.best_paths[(57, 60, 90, 87, 57)]
        self.best_paths['product3'] = self.best_paths[(57, 60, 90, 88, 58, 57)]

        # print(self.get_best_path(57, 61))

    def tactics_assign(self):
        # self.upgrade_dict['trains'].append(1)
        # self.upgrade()
        paths = {1: self.best_paths['armor'].copy(),
                 2: self.best_paths['armor'].copy(),
                 3: self.best_paths['product1'].copy(),
                 4: self.best_paths['product1'].copy()}
        paths[1].stop_dict = {0: 1, 35: 4, 36: 31}
        paths[2].stop_dict[36] = 4
        paths[4].stop_dict = {0: 1, 53: 10}
        paths[5] = paths[1].copy()
        paths[5].stop_dict = {36: 28}
        paths[6] = paths[5].copy()
        self.train_tasks[1] = ['upgrade2', paths[1], self.best_paths['product1'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy()]
        self.train_tasks[2] = [paths[2], 'upgrade', self.best_paths['product2'].copy(), 'upgrade', self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy()]
        self.train_tasks[3] = [paths[3], self.best_paths['product3'].copy(), 'upgrade2', paths[5], 'upgrade_town', self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy()]
        self.train_tasks[4] = [paths[4], self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), 'upgrade2', self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy(), self.best_paths['product2'].copy()]

    def upgrade(self, *train_idxes, post=False):
        # if self.can_upgrade(train_idx):
        if post:
            self.upgrade_dict['posts'].append(32)
            self.graph.home.post.upgrade_cost *= 2
        for train_idx in train_idxes:
            self.graph.trains[train_idx].goods = (0, self.graph.trains[train_idx].goods[1] * 2)
            self.graph.home.post.armor = (self.graph.home.post.armor[0]-self.graph.trains[train_idx].upgrade_cost, self.graph.home.post.armor[1])
            self.graph.trains[train_idx].upgrade_cost *= 2
        self.upgrade_server()

    def upgrade_server(self):
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

        # if self.can_upgrade(train_idx):
        #     self.upgrade_dict['trains'].append(train_idx)
        #     self.graph.trains[train_idx].goods = (0, self.graph.trains[train_idx].goods[1]*2)
        #     self.graph.home.post.armor = (self.graph.home.post.armor[0]-self.graph.trains[train_idx].upgrade_cost, self.graph.home.post.armor[1])
        #     self.graph.trains[train_idx].upgrade_cost *= 2
        # if self.can_upgrade(1, True):
        #     self.upgrade_dict['posts'].append(74)
        #     self.graph.home.post.upgrade_cost *= 2
        # self.upgrade()
        if train_idx == 1:
        #     self.get_armor()
        # else:
            self.get_products(train_idx)
