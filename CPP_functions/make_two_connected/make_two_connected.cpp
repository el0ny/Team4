#include "make_two_connected.h"
#include <iostream>
#include <unordered_map>

vector<pair<int, int>> MakeTwoConnected(vector<pair<int, int>> &lines) {
    unordered_map<int, vector<int>> graph;
    for (const auto &line : lines) {
        graph[line.first].push_back(line.second);
        graph[line.second].push_back(line.first);
    }
    vector<pair<int, int>> fake_edges;
    for (auto &vertex : graph) {
        if (vertex.second.size() < 2) {
            int i = 0;
            if (graph[vertex.second[0]][i] == vertex.first) {
                i = 1;
            }
            graph[graph[vertex.second[0]][i]].push_back(vertex.first);
            graph[vertex.first].push_back(graph[vertex.second[0]][i]);
            fake_edges.emplace_back(vertex.first, graph[vertex.second[0]][i]);
        }
    }
    return fake_edges;
}

int main() {
    vector<pair<int, int>> v{{2, 3}, {1, 2}, {2, 4}};
    vector<pair<int, int>> b = MakeTwoConnected(v);

    return 0;
}
