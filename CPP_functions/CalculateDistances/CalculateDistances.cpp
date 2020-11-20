#include "CalculateDistances.h"

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