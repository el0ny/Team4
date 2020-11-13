import pygame
import json
from graph import Graph, Point, Line
from myModule import getMaxCycle


screen_width = 1600
screen_height = 900
WHITE = (255, 255, 255)
YELLOW = (225, 225, 0)


def main():
    with open("files/small_graph.json", "r") as read_file:
        raw_graph = json.load(read_file)

    points = {}
    for point in raw_graph['points']:
        points[point['idx']] = Point(point['idx'], point['post_idx'])
    lines = {}
    for line in raw_graph['lines']:
        point_list = [points[point] for point in line['points']]
        lines[line['idx']] = Line(line['idx'], line['length'], point_list)

    cycle = getMaxCycle([line.get_points() for line in lines.values()])

    pygame.init()
    sc = pygame.display.set_mode((screen_width, screen_height))
    graph = Graph(raw_graph)
    graph.draw(sc)
    # pygame.draw.arc(sc, WHITE, [80,10,250,1200], 3*math.pi/2, math.pi, 2)

    pygame.display.update()

    while 1:
        pygame.time.delay(1000)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
        main()
