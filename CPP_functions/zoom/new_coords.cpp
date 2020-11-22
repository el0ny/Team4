#include "new_coords.h"

vector<pair<double, double>> GetNewCoordinates(vector<pair<double, double>> &coordinates, double cons) {
    for (auto &point : coordinates) {
        point.first = point.first * cons;
        point.second = point.second  * cons;
    }
    return coordinates;
}




//int main() {
//    vector<pair<double, double>> l{{-2, 4}};
//    pair<double, double> cen{-2, 3};
//    auto v = GetNewCoordinates(cen, l);
//    cout << v[0].first << " " << v[0].second << "\n";
//    v = GetOldCoordinates(cen, v);
//    cout << v[0].first << " " << v[0].second;
//    return 0;
//}
