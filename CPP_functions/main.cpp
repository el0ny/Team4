#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <algorithm>


struct Line {
    int x;
    int y;

    bool operator==(const Line &rhs) const {
        return (x == rhs.x && y == rhs.y) || (y == rhs.x && x == rhs.y);
    }
};

std::ostream &operator<<(std::ostream &os, const std::vector<Line> &a) {
    for (const auto &i : a) {
        os << i.x << "-" << i.y << "\n";
    }
    return os;
}

struct Fragment {
    std::vector<Line> lines;
};

std::vector<Fragment> getFragments(const std::vector<Line> &graph, const std::vector<Line> &subgraph) {
    std::unordered_set<int> subgraph_points;
    for (auto line : subgraph) {
        subgraph_points.insert(line.x);
        subgraph_points.insert(line.y);
    }

    std::unordered_map<int, bool> other_points;
    for (auto line : graph) {
        if (subgraph_points.find(line.x) == subgraph_points.end()) {
            other_points[line.x] = false;
        }
        if (subgraph_points.find(line.y) == subgraph_points.end()) {
            other_points[line.y] = false;
        }
    }

    std::vector<Fragment> fragments;
    Fragment fragment = {};
    for (auto &point : other_points) {
        if (!point.second) {
            std::queue<int> order;
            order.push(point.first);
            point.second = true;
            while (!order.empty()) {
                int cur = order.front();
                order.pop();
                for (auto line : graph) {
                    if (line.x == cur || line.y == cur) {
                        int next_point = (cur == line.x) ? line.y : line.x;
                        if (subgraph_points.find(next_point) == subgraph_points.end() &&
                            !other_points[next_point]) {
                            order.push(next_point);

                            other_points[next_point] = true;
                        }

                        if ((other_points.find(next_point) != other_points.end() &&
                             other_points.find(cur) != other_points.end() &&
                             cur < next_point) ||
                            (subgraph_points.find(next_point) != subgraph_points.end()) ||
                            (subgraph_points.find(cur) != subgraph_points.end())) {
                            fragment.lines.push_back({next_point, cur});
                        }
                    }
                }
            }
            fragments.push_back(fragment);
            fragment = {};
        }
    }

    for (auto line : graph) {
        if (subgraph_points.find(line.x) != subgraph_points.end() &&
            subgraph_points.find(line.y) != subgraph_points.end() &&
            std::find(std::begin(subgraph), std::end(subgraph), line) == std::end(subgraph)) {
            fragments.push_back({{line}});
        }
    }
    return fragments;
}


int main() {
    for (auto fragment : getFragments({{1,  2},
                                       {1,  8},
                                       {1,  7},
                                       {1,  9},
                                       {9,  2},
                                       {9,  10},
                                       {2,  10},
                                       {2,  3},
                                       {10, 3},
                                       {10, 4},
                                       {3,  11},
                                       {3,  4},
                                       {4,  5},
                                       {5,  11},
                                       {6,  11},
                                       {2,  6},
                                       {7,  6},
                                       {8,  7},
                                       {2,  8},
                                       {8,  7},
                                       {5,  6}}, {{1, 2},
                                                  {2, 3},
                                                  {3, 4},
                                                  {4, 5},
                                                  {5, 6},
                                                  {6, 7},
                                                  {7, 8},
                                                  {8, 1}})) {
        std::cout << fragment.lines << std::endl;
    }
    return 0;
}
