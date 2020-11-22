import pygame
from py_modules.graph import Graph, Point, Line, Face, Post, Train
from graphModule import getCycle
from py_modules.make_planar import cycle_to_graph, draw_planar, prettify
from py_modules.connector import get_map, get_info, close_conn

screen_width = 1600
screen_height = 900


def mouse_click(mouse_pos, points: dict, selected):
    if selected is not None:
        selected.selected = False
    if 100 < mouse_pos[0] < 1000:
        for point in points.values():
            if point.coordinates[0]-7 < mouse_pos[0]-100 < point.coordinates[0]+7:
                if point.coordinates[1] - 7 < mouse_pos[1] < point.coordinates[1] + 7:
                    point.selected = True
                    return point
    return None


# for future
def event_alarm(events, screen):
    for event in events:
        print(event['type'])


def update_map(posts, info):
    for post in info['posts']:
        posts[post['idx']].post.update(post)


def update_screen(image, screen, subgraph):
    image.fill((12, 12, 12))
    screen.fill((0,0,0))
    subgraph.draw(image, screen)
    screen.blit(image, (100, 0))
    pygame.display.update()


def main():
    player_info, first_layer_info, second_layer_info, sock = get_map()
    raw_graph = first_layer_info
    # with open("files/big_graph.json", "r") as read_file:
    #     raw_graph = json.load(read_file)
    points = {}
    for point in raw_graph['points']:
        points[point['idx']] = Point(point['idx'], point['post_idx'])
    points[player_info['home']['idx']].home = True
    lines = {}
    for line in raw_graph['lines']:
        point_list = [points[point] for point in line['points']]
        point_list[0].adjacent_points.append(point_list[1])
        point_list[1].adjacent_points.append(point_list[0])
        lines[line['idx']] = Line(point_list, line['idx'], line['length'])
    posts = {}
    for post in second_layer_info['posts']:
        points[post['point_idx']].post = Post(post)
        posts[post['idx']] = points[post['point_idx']]
    graph = Graph(points, lines, raw_graph['name'], raw_graph['idx'])
    cycle = getCycle(graph.get_lines())
    subgraph = cycle_to_graph(graph, cycle)
    subgraph.faces.append(Face(subgraph.points, cycle))
    subgraph.faces.append(Face(subgraph.points, cycle))
    prettify(graph, subgraph, points)
    draw_planar(subgraph, points)
    pygame.font.init()
    pygame.display.init()
    sc = pygame.display.set_mode((screen_width, screen_height))
    image = pygame.Surface([900, 900])
    image.fill((12,12, 12))

    graph.draw(image, sc)

    trains = {train['idx']: Train(train) for train in player_info['trains']}
    for train in trains.values():
        train.set_line(lines[train.line_idx])
    clock = pygame.time.Clock()
    selected = None
    sc.blit(image, (100, 0))
    pygame.display.update()
    dragging = False
    scale = 1
    running = True
    while running:
        clock.tick(120)
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                # if i.key == pygame.K_e:
                #     for train in trains.values():
                #         move_train(sock, 609, -1, train.idx)
                if i.key == pygame.K_SPACE:
                    info = get_info(sock)
                    # if info['posts'][0][]
                    update_map(posts, info)
                    if selected is not None:
                        selected.draw(image, sc)
                    # for train in trains.values():
                    #     # move_train(sock, train.get_possible_lines(), 1, train.idx)
                    #     train.update(info['trains'][0])
                    #     train.draw(image)
            if i.type == pygame.QUIT:
                close_conn(sock)
                running = False
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if selected is not None:
                        selected.draw(image, sc)
                    selected = mouse_click(i.pos, points, selected)
                    sc.blit(image, (100, 0))
                    pygame.display.update()
                elif i.button == 2:
                    old_mouse_x, old_mouse_y = i.pos
                    dragging = True
                elif i.button == 4:
                    scale += 0.1
                    subgraph.zoom(scale)
                elif i.button == 5:
                    scale -= 0.1
                    subgraph.zoom(scale)
            elif i.type == pygame.MOUSEBUTTONUP:
                if i.button == 2:
                    dragging = False
            elif i.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = i.pos
                    subgraph.move(mouse_x - old_mouse_x, mouse_y - old_mouse_y)
                    old_mouse_x, old_mouse_y = i.pos
            update_screen(image, sc, subgraph)


if __name__ == '__main__':
    main()
    raise SystemExit()
