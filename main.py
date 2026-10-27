from pico2d import *
import random

from grass import Grass #grass.py에서 Grass클래스를 가져온다.
from boy import Boy     #boy.py에서 Boy클래스를 가져온다.
#각 모듈당 class는 하나만 정의하는 것이 좋다. 
#모듈명과 클래스명을 같게 하는 것이 좋다.

# Game object class here





def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        boy.handle_event(event)


def reset_world():
    global world
    global boy

    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
