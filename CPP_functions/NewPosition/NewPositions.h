#ifndef NEWPOSITION_NEWPOSITIONS_H
#define NEWPOSITION_NEWPOSITIONS_H
#include <vector>
#include "math.h"
#include <utility>

std::pair<int, int>
NewPosition(std::pair<int, int> cur_pos, const std::vector<std::pair<int, int>> &neighbours, double cool, double C);


#endif //NEWPOSITION_NEWPOSITIONS_H
