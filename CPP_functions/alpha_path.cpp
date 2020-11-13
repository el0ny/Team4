#include "find_alpha_path.h"
#include <iostream>
#include <queue>
#include <unordered_map>
#include <unordered_set>

// Скопировала пока структурки из getFragments
struct Line {
    int x;
    int y;

    bool operator==(const Line &rhs) const {
        return (x == rhs.x && y == rhs.y) || (y == rhs.x && x == rhs.y);
    }
};
struct Fragment {
    vector<Line> lines;
};

template<typename T, typename Container>
bool Contain(T v, Container &c) {
    return c.find(v) != c.end();
}

int dfs(int vertex, unordered_map<int, vector<int>> &adjacency, vector<int> &parents, unordered_set<int> &s) {
    vector<bool> visited(adjacency.size());
    queue<int> que;
    que.push(vertex);
    visited[vertex] = true;
    parents[vertex] = -1;

    while (!que.empty()) {
        int v = que.front();
        que.pop();
        for (size_t i = 0; i < adjacency[v].size(); ++i) {
            int to = adjacency[v][i];
            if (!visited[to] && !Contain(to, s)) {
                visited[to] = true;
                que.push(to);
                parents[to] = v;
            } else if (Contain(to, s) && !visited[to]) {
                parents[to] = v;
                return to;
            }
        }
    }
    return -1;
}

vector<int> FindAlphaPath(const Fragment &fragment, const vector<Line> &subgraph) {
    unordered_set<int> subgraph_vertex;
    for (const auto &line : subgraph) {
        subgraph_vertex.insert(line.x);
        subgraph_vertex.insert(line.y);
    }
    unordered_map<int, vector<int>> adjacency;
    for (const auto &line : fragment.lines) {
        adjacency[line.x].push_back(line.y);
        adjacency[line.y].push_back(line.x);
    }
    vector<int> parents(adjacency.size());
    int last = 0;
    for (const auto &vertex : subgraph_vertex) {
        if (Contain(vertex, adjacency)) {
            last = dfs(vertex, adjacency, parents, subgraph_vertex);
            break;
        }
    }
    vector<int> cycle;
    for (; last != -1; last = parents[last]) {
        cycle.push_back(last);
    }
    return cycle;
}
int main() {
    //Пример применения
    Fragment fr;
    fr.lines = {{0, 1}, {1, 2}, {2, 3}};
    vector<Line> subgraph;
    subgraph.push_back({0, 3});
    vector<int> ans = FindAlphaPath(fr, subgraph);
    for (const auto &x : ans) {
        cout << x << " ";//0 1 2 3
    }
    return 0;
}
