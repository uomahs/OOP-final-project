import pygame
import random
from typing import Literal

from actions.SleepAction import SleepAction
from actions.SnackAction import SnackAction
from actions.GameAction import GameAction
from actions.SecretAction import SecretAction


def draw_mission_bar(surface, x, y, width, height, progress,
                     tube_color=(90, 50, 30),
                     inner_color=(40, 20, 10),
                     fill_color=(120, 220, 255)):

    radius = height // 2

    pygame.draw.rect(surface, tube_color,
                     (x, y, width, height),
                     border_radius=radius)

    inner = pygame.Rect(x + 4, y + 4, width - 8, height - 8)
    pygame.draw.rect(surface, inner_color, inner, border_radius=radius - 4)

    p = max(0.0, min(progress, 1.0))
    fill_w = int((inner.width - 8) * p)
    if fill_w > 0:
        fill = pygame.Rect(inner.x + 4, inner.y + 4,
                           fill_w, inner.height - 8)
        pygame.draw.rect(surface, fill_color, fill, border_radius=radius - 6)


class Student:
    current: Literal["sleep", "snack", "game", "normal"]
    
    def __init__(self, x=400, y=300):
        self.total_score = 0
        self.current_action = None
        self.current= None
        self.remaining_missions = [SleepAction, SnackAction, GameAction]

        self.images = {
            'normal': pygame.image.load('images/student.png'),
            'snack': pygame.image.load('images/snack.png'),
            'game': pygame.image.load('images/game.png'),
            'sleep': pygame.image.load('images/sleep.png'),
        }
        self.image = self.images['normal']
        self.rect = self.image.get_rect(center=(x, y)) # 위치는 수정


    def set_state(self, state_name):
        if state_name in self.images:
            self.image = self.images[state_name]
            self.current = state_name
        else:
            self.image = self.images['normal']
            self.current = "normal"

    def update(self, dt, ctx):
        if self.current_action and self.current_action.is_active:
            self.current_action.execute(dt, ctx)
            self.set_state(self.current_action.name)

            if self.current_action.is_complete():
                self.stop_current_action(ctx)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.current_action:
            progress = self.current_action.progress
            draw_mission_bar(screen, 150, 550, 500, 30, progress= self.current_action.progress)

    def stop_current_action(self, ctx):
        if self.current_action:
            self.current_action.stop(ctx)
        self.current_action = None
        self.set_state('normal')

    def to_sleep(self, ctx):
        self._start_action(SleepAction, "sleep", ctx)

    def to_snack(self, ctx):
        self._start_action(SnackAction, "snack", ctx)
 
    def to_game(self, ctx):
        self._start_action(GameAction, "game", ctx)
        
    def _start_action(self, action_cls, name: str, ctx):
        if action_cls not in self.remaining_missions:
            return

        action = action_cls()       
        self.current_action = action
        self.set_state("normal")      
        action.start(ctx)         

        self.remaining_missions.remove(action_cls)

    def start_random_mission(self, ctx):
        if (not self.remaining_missions):
            return
        chosen_cls= random.choice(self.remaining_missions)
        if (chosen_cls == SleepAction):
            self.to_sleep(ctx)
        elif(chosen_cls == SnackAction):
            self.to_snack(ctx)
        elif(chosen_cls == GameAction):
            self.to_game(ctx)
            