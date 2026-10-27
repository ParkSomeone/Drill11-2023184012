from pico2d import *
import random
import turtle
#모듈을 우클릭 후 go to definition을 하면 해당 모듈의 정의를 볼 수 있다.

# Game object class here

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass


class Boy:
    #class 변수 image선언
    image=None
    def __init__(self):
        self.x, self.y = random.randint(0, 800), 90
        self.frame = random.randint(0, 7)
        #self변수: 객체의 변수, (객체명)변수: 클래스 변수
        #생성된 class변수는 모든 객체가 공유한다.
        if Boy.image==None:
            Boy.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def handle_events():
    global running
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global world

    world = []

    grass = Grass()
    world.append(grass)

    team = [Boy() for i in range(10000)]
    world += team


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
#    delay(0.05)
# finalization code
close_canvas()
