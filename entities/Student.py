import pygame
import random
from typing import Literal, Optional

from actions.SleepAction import SleepAction
from actions.SnackAction import SnackAction
from actions.GameAction import GameAction
from actions.SecretAction import SecretAction

class Student:
    current: Literal["sleep", "snack", "game"]
    
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
            'front': pygame.image.load('images/professorFront.png'),
            'back': pygame.image.load('images/professorBack.png')
        }

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

            if self.current_action.is_complete():
                self.stop_current_action(ctx)
                self.update_score(self.current_action.point)
                print(f"미션 완료! 총점: {self.total_score}")

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def stop_current_action(self, ctx):
        if self.current_action:
            self.current_action.stop(ctx)
        self.set_state('normal')

    def to_sleep(self, ctx):
        self._start_action(SleepAction, "sleep", ctx)

    def to_snack(self, ctx):
        self._start_action(SnackAction, "snack", ctx)
 
    def to_game(self, ctx):
        self._start_action(GameAction, "game", ctx)

    def start_action(self, action_cls, name: str, ctx):
        if (action_cls not in self.remaining_missions):
            return
        
        action= action_cls()
        self.current_action= action
        self.current= name

        self.set_state(name)
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
            
    def update_score(self, point):
        self.total_score+= point