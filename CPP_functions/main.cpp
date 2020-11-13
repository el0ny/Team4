#include <iostream>
#include <vector>
#include <unordered_set>

struct Line {
    int x;
    int y;

    bool operator==(const Line &rhs) const {
        return (x == rhs.x && y == rhs.y) || (y == rhs.x && x == rhs.y);
    }
};

struct Fragment {
    std::vector<Line> lines;
};

struct Face {
    std::vector<int> points;
};


std::vector<Face> GetAllowedFace(Fragment fragment, std::vector<Face> faces) {
    std::vector<Face> allowed_faces;
    std::unordered_set<int> fragment_points; //если Fragment хранит points то можно работать сразу с ними
    for (auto line : fragment.lines) {
        fragment_points.insert(line.y);
        fragment_points.insert(line.x);
    }
    for (auto face : faces) {
        std::unordered_set<int> face_points(face.points.begin(), face.points.end());
        if (face_points == fragment_points) {
            allowed_faces.push_back(face);
        }
    }
    return allowed_faces;
}

std::ostream &operator<<(std::ostream &os, const std::vector<int> &a) {
    for (const auto &i : a) {
        os << i << " ";
    }
    return os;
}

int main() {
    Fragment fr = {{{1, 2}, {2, 3}, {3, 1}}};
    std::vector<Face> faces = {{{1, 2, 3}},
                               {{3, 4, 5}}};
    for (auto face : GetAllowedFace(fr, faces)) {
        std::cout << face.points << "\n";
    }
    return 0;
}
