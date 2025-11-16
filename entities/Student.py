from typing import Literal
import random

class Student:
    current: Literal["sleep", "snack", "game"]
    total_score: int
    current_action: 'SecretAction' | None 
    remaining_missions: list

    def __init__(self):
        self.total_score = 0
        self.current_action = None
        self.current= None
        self.remaining_missions = [SleepAction, SnackAction, GameAction]

    def to_sleep(self, ctx):
        self._start_action(SleepAction, "sleep", ctx)

    def to_snack(self, ctx):
        self._start_action(SnackAction, "snack", ctx)
 
    def to_game(self, ctx):
        self._start_action(GameAction, "game", ctx)

    def _start_action(self, action_cls, name: str, ctx):
        if (action_cls not in self.remaining_missions):
            return
        action= action_cls()
        
        self.current_action= action
        self.current= name
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
    
   