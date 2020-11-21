#include "new_coords.h"

vector<pair<double, double>> GetNewCoordinates(const pair<double, double> &center,
                                               vector<pair<double, double>> &coordinates, double cons) {
    for (auto &point : coordinates) {
        point.first = center.first + (point.first - center.first) * cons;
        point.second = center.second + (point.second - center.second) * cons;
    }
    return coordinates;
}

vector<pair<double, double>> GetOldCoordinates(const pair<double, double> &center,
                                               vector<pair<double, double>> &coordinates, double cons) {
    for (auto &point : coordinates) {
        point.first = (point.first - center.first) / cons + center.first;
        point.second = (point.second - center.second) / cons + center.second;
    }
    return coordinates;
}


int main() {
    vector<pair<double, double>> l{{-2, 4}};
    pair<double, double> cen{-2, 3};
    auto v = GetNewCoordinates(cen, l);
    cout << v[0].first << " " << v[0].second << "\n";
    v = GetOldCoordinates(cen, v);
    cout << v[0].first << " " << v[0].second;
    return 0;
}
