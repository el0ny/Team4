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
