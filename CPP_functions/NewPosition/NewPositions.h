#ifndef NEWPOSITION_NEWPOSITIONS_H
#define NEWPOSITION_NEWPOSITIONS_H

#include <iostream>
#include <vector>
#include <map>
#include <unordered_set>
#include <queue>
#include "math.h"

std::map<int, int> CalculateDistances(const std::vector<std::pair<int, int>> &graph,
                                      const std::vector<int> &external_face);

std::pair<int, int>
NewPosition(std::pair<int, std::pair<int, int>> cur_vertex, // index, position
            const std::vector<std::pair<int, std::pair<int, int>>> &neighbours,
            const std::vector<std::pair<int, int>> &graph,
            const std::vector<int> &external_face,
            int cool,
            int A);


#endif //NEWPOSITION_NEWPOSITIONS_H
