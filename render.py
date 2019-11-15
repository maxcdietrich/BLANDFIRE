import pygame
import map
import time

class View:
    def __init__(self, width, height):
        self.size = (width, height)
        self.screen = pygame.display.set_mode((width,height))

    def init_render(self, seed_map):
        self.screen.fill((255,255,255))
        for coordinate in seed_map.tile_dict:
            coordinate = eval(coordinate)
            rectangle = pygame.Rect((coordinate[0],coordinate[1]),(1,1))
            pygame.draw.rect(self.screen,(34,139,34),rectangle)
        pygame.display.flip()
        time.sleep(0.01)


    def update_render(self):
        pass

def draw_model():
    sim_map = map.Map()
    sim_map.fromJSON('test_map')
    key_list = []
    for key in sim_map.tile_dict:
        key_list.append(key)
    key_list.sort()
    last_key = eval(key_list[-1]) #has format (max x, max y)
    view = View(last_key[0],last_key[1])
    view.init_render(sim_map)
    print('done')
    while True:
        view.update_render()





draw_model()
