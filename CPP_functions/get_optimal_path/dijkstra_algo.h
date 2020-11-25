#pragma once
#include <vector>
using namespace std;

pair<vector<int>, vector<int>> GetOptimalPath(int begin_idx, int end_idx, const vector<pair<int, pair<int, int>>> &gr);

