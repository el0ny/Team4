#include "find_max_cycle.h"
#include <algorithm>
#include <iostream>
#include <queue>
#include <set>

//Вызываем в виде vector<int> cycle = FindMinCycle(lines);
//Необходимо передать в функцию множество ребер в виде пары точек.

//Чтобы работало с любой нумерацией вершин:
vector<int> MapFromBadIndexes(vector<pair<int, int>> &lines) {
    set<int> s;
    for (const auto &x : lines) {
        s.insert(x.first);
        s.insert(x.second);
    }
    vector<int> v;
    for (auto it = s.begin(); it != s.end(); ++it) {
        v.push_back(*it);
    }
    for (auto &x : lines) {
        for (size_t i = 0; i < v.size(); i++) {
            if (v[i] == x.first) {
                x.first = i;
            }
            if (v[i] == x.second) {
                x.second = i;
            }
        }
    }
    return v;
}

vector<int> MapToBadIndexes(vector<int> &cycle, const vector<int> &dict) {
    for (auto &x : cycle) {
        for (size_t i = 0; i < dict.size(); i++) {
            if (i == x) {
                x = dict[i];
                break;
            }
        }
    }
    return cycle;
}

//Находим цикл наибольшей длины.
vector<int> FindMaxCycle(vector<pair<int, int>> &lines) {
    // Переводим список ребер в матрицу смежности.
    set<int> unique;
    for (auto x : lines) {
        unique.insert(x.first - 1);
        unique.insert(x.second - 1);
    }
    int n = unique.size();
    vector<int> dict = MapFromBadIndexes(lines);
    vector<vector<int>> graph(n, vector<int>());
    for (const auto &x : lines) {
        int a = x.first;
        int b = x.second;
        graph[a].push_back(b);
        graph[b].push_back(a);
    }

    vector<int> max_parents;
    int vertex_max_cycle_to = 0, vertex_max_cycle_v = 0, max_cycle_length = -1;

    //Бфс из каждой из вершин.
    for (int k = 0; k < n; k++) {
        vector<bool> visited(n);
        vector<int> parents(n), levels(n);
        queue<int> que;
        que.push(k);
        visited[k] = true;
        parents[k] = -1;

        while (!que.empty()) {
            int v = que.front();
            que.pop();
            for (size_t i = 0; i < graph[v].size(); ++i) {
                if (graph[v][i] != parents[v]) {
                    int to = graph[v][i];
                    if (!visited[to]) {
                        visited[to] = true;
                        levels[to] = levels[v] + 1;
                        que.push(to);
                        parents[to] = v;
                    } else {
                        int cycle_length = levels[v] + levels[to];
                        max_cycle_length = max(max_cycle_length, cycle_length);
                        if (max_cycle_length == cycle_length) {
                            vertex_max_cycle_to = to;
                            vertex_max_cycle_v = v;
                            max_parents = parents;
                        }
                    }
                }
            }
        }
    }
    vector<int> cycle;
    if (max_cycle_length != -1) {
        while (max_parents[vertex_max_cycle_to] != -1) {
            cycle.push_back(vertex_max_cycle_to);
            vertex_max_cycle_to = max_parents[vertex_max_cycle_to];
        }
        reverse(cycle.begin(), cycle.end());
        while (vertex_max_cycle_v != -1) {
            cycle.push_back(vertex_max_cycle_v);
            vertex_max_cycle_v = max_parents[vertex_max_cycle_v];
        }
    }
    return MapToBadIndexes(cycle, dict);
}
int main() {
    //Примеры:
    vector<pair<int, int>> lines{{1, 2}, {2, 3}, {3, 4}, {4, 1}, {1, 3}};
    vector<int> c = FindMaxCycle(lines);
    for (const auto &x : c) {
        cout << x << " ";
    }

    vector<pair<int, int>> lines1{{11, 22}, {22, 10}, {10, 11}};
    vector<int> c1 = FindMaxCycle(lines1);
    for (const auto &x : c1) {
        cout << x << " ";
    }

    return 0;
}