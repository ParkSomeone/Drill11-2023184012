import math
import time

from pico2d import (
    load_image, SDL_KEYDOWN, SDL_KEYUP,
    SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE,
)
from transitions import Machine

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.pressed_directions = set()
        self.state_started_at = time.monotonic()
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP'],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE'},
                {'trigger': 'start_running', 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN'},
                {'trigger': 'stop_running', 'source': 'RUN', 'dest': 'IDLE'},
            ],
        )

    def update(self):
        if self.state == 'IDLE':
            if time.monotonic() - self.state_started_at >= 5:
                self.fall_asleep()
                self.state_started_at = time.monotonic()
                return
            self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x += 5 * self.face_dir

    def handle_event(self, event):
        if (self.state == 'SLEEP' and event.type == SDL_KEYDOWN
                and event.key == SDLK_SPACE):
            self.wake_up()
            self.state_started_at = time.monotonic()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            self.pressed_directions.add(event.key)
            self.face_dir = -1 if event.key == SDLK_LEFT else 1
            if self.state in ('IDLE', 'SLEEP'):
                self.start_running()
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            self.pressed_directions.discard(event.key)
            if self.state == 'RUN':
                if self.face_dir == -1 and SDLK_LEFT not in self.pressed_directions:
                    if SDLK_RIGHT in self.pressed_directions:
                        self.face_dir = 1
                    else:
                        self.stop_running()
                        self.state_started_at = time.monotonic()
                elif self.face_dir == 1 and SDLK_RIGHT not in self.pressed_directions:
                    if SDLK_LEFT in self.pressed_directions:
                        self.face_dir = -1
                    else:
                        self.stop_running()
                        self.state_started_at = time.monotonic()

    def draw(self):
        if self.state == 'SLEEP':
            self.image.clip_composite_draw(
                self.frame * 100, 300 if self.face_dir == 1 else 200,
                100, 100, math.pi / 2, '',
                self.x, self.y - 20, 100, 100,
            )
            return

        if self.state == 'RUN':
            self.image.clip_draw(
                self.frame * 100, 100 if self.face_dir == 1 else 0,
                100, 100, self.x, self.y,
            )
            return

        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
