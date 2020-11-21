#include "NewPositions.h"

std::pair<int, int> NewPosition(
        std::pair<int, std::pair<int, int>> cur_vertex,
        const std::vector<std::pair<int, std::pair<int, int>>> &neighbours,
        const std::vector<std::pair<int, int>> &graph,
        const std::vector<int> &external_face,
        int cool,
        int A) {
    std::map<int, int> distances = CalculateDistances(graph, external_face);
    int max_per = 0;
    for (auto vertex : distances) {
        max_per = std::max(max_per, vertex.second);
    }
    std::pair<double, double> cur_force(0, 0);
    for (auto neighbour : neighbours) {
        double distance_x = neighbour.second.first - cur_vertex.second.first;
        double distance_y = neighbour.second.second - cur_vertex.second.second;
        double C = std::sqrt(distances.size() / 3.141592) * std::pow(2.718281, (2 * max_per
                                                                                - distances[cur_vertex.first]
                                                                                - distances[neighbour.first]) /
                                                                               max_per * A);
        cur_force.first += C * distance_x * distance_x * distance_x;
        cur_force.second += C * distance_y * distance_y * distance_y;
    }
    cur_vertex.second.first += std::min(static_cast<double>(cool), std::abs(cur_force.first)) *
                               cur_force.first / std::abs(cur_force.first);
    cur_vertex.second.second += std::min(static_cast<double>(cool), std::abs(cur_force.second)) *
                                cur_force.second / std::abs(cur_force.second);
    return cur_vertex.second;
}

std::map<int, int> CalculateDistances(const std::vector<std::pair<int, int>> &graph,
                                      const std::vector<int> &external_face) {
    std::map<int, int> distances;
    std::unordered_set<int> vertexes(external_face.begin(), external_face.end());
    for (const auto &line : graph) {
        distances[line.first] = (vertexes.find(line.first) == vertexes.end()) ? -1 : 0;
        distances[line.second] = (vertexes.find(line.second) == vertexes.end()) ? -1 : 0;
    }
    std::queue<int> order;
    for (const auto& vertex : external_face) {
        order.push(vertex);
    }
    while (!order.empty()) {
        int cur = order.front();
        order.pop();
        for (auto line : graph) {
            if (line.first == cur || line.second == cur) {
                int next_point = (cur == line.first) ? line.second : line.first;
                if (distances[next_point] == -1) {
                    order.push(next_point);
                    distances[next_point] = distances[cur] + 1;
                }
            }
        }
    }
    return distances;
}