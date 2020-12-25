from py_modules.train import Train


class Path:
    def __init__(self, path, start, end, length, connector, post_type=None, posts=None, stop_dict=None):
        self.path = path
        self.start = start
        self.end = end
        self.length = length
        self.connector = connector
        self.current_track = [path[0][0], path[0][1], 0]  # line_id, direction, length
        self.current_track_idx = 0
        self.posts = posts  # maybe list
        self.arrival_points = {}  # point_idx: arrival_time

        self.stop_dict = {} if stop_dict is None else stop_dict  # {point_idx: time}
        self.income = 0
        self.lines = {}  # line_idx: Line
        self.post_type = post_type
        self.tick = 0
        self.resume = False

    def copy(self):
        return Path(self.path, self.start, self.end, self.length, self.connector, self.post_type, self.posts, stop_dict=self.stop_dict)

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

    def should_stop(self, train_idx):
        # points = self.lines[self.current_track[0]].points
        # point = points[0] if self.current_track[1] == 1 else points[1]
        # if point.idx in self.stop_dict:
        #     self.stop_dict[point.idx] -= 1
        #     if self.stop_dict[point.idx] == 0:
        #         del self.stop_dict[point.idx]
        #     return True
        if self.tick in self.stop_dict:
            self.connector.move_train(self.current_track[0], 0, train_idx)
            self.stop_dict[self.tick] -= 1
            if self.stop_dict[self.tick] == 0:
                del self.stop_dict[self.tick]
                self.resume = True
            return True
        return False

    def move(self, train_idx):

        if not self.should_stop(train_idx):

            if self.current_track[2] <= 0:
                # if self.current_track_idx == len(self.path):
                #     return False
                self.current_track = list(self.path[self.current_track_idx])
                self.connector.move_train(self.current_track[0], self.current_track[1], train_idx)
                self.current_track_idx += 1
            elif self.resume:
                self.connector.move_train(self.current_track[0], self.current_track[1], train_idx)
                self.resume = False
            self.current_track[2] -= 1
            self.tick += 1
            if self.current_track[2] <= 0 and self.current_track_idx == len(self.path):

                return False
        return True
