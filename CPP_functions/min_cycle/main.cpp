#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <queue>
#include <set>
using namespace std;

//Вызываем в виде vector<int> cycle = FindMinCycle(FormGraph(lines).first, FormGraph(lines).second);
//Необходимо передать в функцию множество ребер в виде пары точек.
pair<int, vector<vector<int>>> FormGraph(vector<pair<int, int>> &lines) {
  set<int> unique;
  for (auto x : lines) {
    unique.insert(x.first - 1);
    unique.insert(x.second - 1);
  }
  int number = unique.size();
  vector<vector<int>> graph(number, vector<int>());
  for (auto x : lines) {
    int a = x.first - 1;
    int b = x.second - 1;
    graph[a].push_back(b);
    graph[b].push_back(a);

  }
  return {number, graph};
}

//Находим цикл наименьшей длины.
vector<int> FindMinCycle(int n, vector<vector<int>> graph) {
  vector<int> min_parents;
  int vertex_min_cycle_to = 0, vertex_min_cycle_v = 0, min_cycle_length = INT32_MAX;

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
            min_cycle_length = min(min_cycle_length, cycle_length);
            if (min_cycle_length == cycle_length) {
              vertex_min_cycle_to = to;
              vertex_min_cycle_v = v;
              min_parents = parents;
            }
          }
        }
      }
    }
  }
  vector<int> cycle;
  if (min_cycle_length != INT32_MAX) {
    while (min_parents[vertex_min_cycle_to] != -1) {
      cycle.push_back(vertex_min_cycle_to + 1);
      vertex_min_cycle_to = min_parents[vertex_min_cycle_to];
    }
    reverse(cycle.begin(), cycle.end());
    while (vertex_min_cycle_v != -1) {
      cycle.push_back(vertex_min_cycle_v + 1);
      vertex_min_cycle_v = min_parents[vertex_min_cycle_v];
    }
  }
  return cycle;
}

int main() {
  return 0;
}