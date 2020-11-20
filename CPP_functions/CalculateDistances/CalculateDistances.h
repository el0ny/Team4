#ifndef CALCULATEDISTANCES_CALCULATEDISTANCES_H
#define CALCULATEDISTANCES_CALCULATEDISTANCES_H

#include <vector>
#include <map>
#include <unordered_set>
#include <queue>

std::map<int, int> CalculateDistances(const std::vector<std::pair<int, int>> &graph,
                                      const std::vector<int> &external_face);

#endif
