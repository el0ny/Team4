#include "NewPositions.h"

std::pair<int, int>
NewPosition(std::pair<int, int> cur_pos, const std::vector<std::pair<int, int>> &neighbours, int cool, int C) {
    std::pair<double, double> cur_force(0, 0);
    for (auto neighbour : neighbours) {
        double distance_x = neighbour.first - cur_pos.first;
        double distance_y = neighbour.second - cur_pos.second;
        cur_force.first += C * distance_x * distance_x * distance_x;
        cur_force.second += C * distance_y * distance_y * distance_y;
    }
    cur_pos.first += std::min(static_cast<double>(cool), std::abs(cur_force.first)) *
                     cur_force.first / std::abs(cur_force.first);
    cur_pos.second += std::min(static_cast<double>(cool), std::abs(cur_force.second)) *
                      cur_force.second / std::abs(cur_force.second);
    return cur_pos;
}