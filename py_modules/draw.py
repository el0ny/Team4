from math import cos, sin, pi


def get_face_coordinates(N):
    r = 400

    screen_width = 900
    screen_height = 900

    x = {}
    y = {}

    for n in range(N):
        x[n] = int(r * cos(2*pi*n/N) + screen_width//2)
        y[n] = int(r * sin(2*pi*n/N) + screen_height//2)

    return [x, y]
