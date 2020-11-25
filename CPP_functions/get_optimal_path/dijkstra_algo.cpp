#include "dijkstra_algo.h"
#include <algorithm>
#include <iostream>
#include <map>
#include <set>

pair<vector<int>, vector<int>> GetOptimalPath(int begin_idx, int end_idx, const vector<pair<int, pair<int, int>>> &gr) {
    map<int, vector<pair<int, int>>> graph;
    for (const auto& i : gr) {
        graph[i.second.first].push_back({i.second.second, i.first});
        graph[i.second.second].push_back({i.second.first, i.first});
    }
    map<int, int> parents, distance;
    map<int, bool> visited;
    for (const auto &item : graph) {
        distance.emplace(item.first, INT32_MAX);
        parents.emplace(item.first, 0);
        visited.emplace(item.first, false);
    }
    distance[begin_idx] = 0;

    set<pair<int, int>> q;
    q.insert({distance[begin_idx], begin_idx});
    while (!q.empty()) {
        int v = q.begin()->second;
        q.erase(q.begin());
        for (size_t j = 0; j < graph[v].size(); ++j) {
            int to = graph[v][j].first,
                len = graph[v][j].second;
            if (distance[v] + len < distance[to]) {
                q.erase(make_pair(distance[to], to));
                distance[to] = distance[v] + len;
                parents[to] = v;
                q.insert(make_pair(distance[to], to));
            }
        }
    }

    vector<int> path, orientation;
    for (int v = end_idx; v != begin_idx; v = parents[v]) {
        path.push_back(v);
    }
    path.push_back(begin_idx);
    reverse(path.begin(), path.end());
    for (size_t j = 0; j < path.size() - 1; j++) {
        for (size_t i = 0; i < gr.size(); i++) {
            if ((gr[i].second.first == path[j] && gr[i].second.second == path[j + 1])) {
                orientation.push_back(1);
                break;
            } else if (gr[i].second.second == path[j] && gr[i].second.first == path[j + 1]) {
                orientation.push_back(-1);
                break;
            }
        }
    }

    return {path, orientation};
}

int main() {
    vector<pair<int, pair<int, int>>> gr{{7, {1, 2}}, {9, {1, 3}}, {10, {2, 3}}, {14, {1, 6}}, {2, {6, 3}}, {9, {6, 5}}, {6, {5, 4}}, {11, {3, 4}}, {15, {2, 4}}};
    vector<int> path = GetOptimalPath(4, 6, gr).first;
    for (const auto &i : path) {
        cout << i << " ";
    }
    cout << "\n";
    vector<int> orientation = GetOptimalPath(4, 6, gr).second;
    for (const auto &i : orientation) {
        cout << i << " ";
    }
    return 0;
}
