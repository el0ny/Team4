#ifndef ALPHA_PATH_FIND_ALPHA_PATH_H
#define ALPHA_PATH_FIND_ALPHA_PATH_H

#include <vector>
using namespace std;

struct Line;
struct Fragment;

vector<int> FindAlphaPath(const Fragment &fragment, const vector<Line> &subgraph);

#endif//ALPHA_PATH_FIND_ALPHA_PATH_H
