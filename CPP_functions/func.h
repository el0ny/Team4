//
// Created by Sofa on 13.11.2020.
//

#ifndef GETFRAGMENTS_FUNC_H
#define GETFRAGMENTS_FUNC_H

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

    bool operator==(const Line &rhs) const;
};

struct Face {
    std::vector<int> points;
};


struct Fragment {
    std::vector <Line> lines;
};

std::vector<Fragment> GetFragments(const std::vector <Line> &graph, const std::vector <Line> &subgraph);

std::vector<Face> GetAllowedFace(Fragment fragment, std::vector<Face> faces);

#endif //GETFRAGMENTS_FUNC_H
