#pragma once
#include <iostream>
#include <vector>

using namespace std;

vector<pair<double, double>> GetNewCoordinates(const pair<double, double>& center,
                                               vector<pair<double, double>> &coordinates, double cons = 2);

vector<pair<double, double>> GetOldCoordinates(const pair<double, double> &center,
                                               vector<pair<double, double>> &coordinates, double cons = 2);

