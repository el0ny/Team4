import pygame
import json
from graph import Graph


screen_width = 1600
screen_height = 900
WHITE = (255, 255, 255)
YELLOW = (225, 225, 0)


def main():
    with open("files/big_graph.json", "r") as read_file:
        raw_graph = json.load(read_file)

    pygame.init()
    sc = pygame.display.set_mode((screen_width, screen_height))
    graph = Graph(raw_graph)
    graph.draw(sc)

    pygame.display.update()

    while 1:
        pygame.time.delay(1000)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
        main()
