#include "func.h"

bool Line::operator==(const Line &rhs) const {
    return (x == rhs.x && y == rhs.y) || (y == rhs.x && x == rhs.y);
}

std::vector<Fragment> GetFragments(const std::vector<Line> &graph, const std::vector<Line> &subgraph) {
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

std::vector<Face> GetAllowedFace(Fragment fragment, std::vector<Face> faces) {
    std::vector<Face> allowed_faces;
    std::unordered_set<int> fragment_points; //если Fragment хранит points то можно работать сразу с ними
    for (auto line : fragment.lines) {
        fragment_points.insert(line.y);
        fragment_points.insert(line.x);
    }
    for (auto face : faces) {
        std::unordered_set<int> face_points(face.points.begin(), face.points.end());
        if (face_points == fragment_points) {
            allowed_faces.push_back(face);
        }
    }
    return allowed_faces;
}