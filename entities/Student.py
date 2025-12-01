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

    pygame.draw.rect(surface, tube_color, (x, y, width, height), border_radius=radius)

    inner = pygame.Rect(x + 4, y + 4, width - 8, height - 8)
    pygame.draw.rect(surface, inner_color, inner, border_radius=radius - 4)
    # 위치 조정 필요
    p = max(0.0, min(progress, 1.0))
    fill_w = int((inner.width - 8) * p)
    if fill_w > 0:
        fill = pygame.Rect(inner.x + 4, inner.y + 4,
                           fill_w, inner.height - 8)
        pygame.draw.rect(surface, fill_color, fill, border_radius=radius - 6)


class Student:
    current: Literal["sleep", "snack", "game", "normal"]
    
    def __init__(self, screen_width, screen_height):
        self.current_action: SecretAction | None= None
        self.current= "normal"
        self.remaining_missions = [SleepAction, SnackAction, GameAction]
        self.target_action: SecretAction | None = None
           
        image_paths = {
            'normal': 'images/student.png',
            'snack':  'images/snack.png',
            'game':   'images/game.png',
            'sleep':  'images/sleep.png',
        }
        self.images = {}
        target_width = 500  
        
        for key, path in image_paths.items():
            temp_img = pygame.image.load(path)
            w, h = temp_img.get_size()
            ratio = target_width / w  
            new_height = int(h * ratio)
            self.images[key] = pygame.transform.scale(temp_img, (target_width, new_height))
            
        center_x = screen_width // 2 + 140
        center_y = screen_height // 2 + 200  
        
        self.current_image = self.images['normal']

        self.rect = self.current_image.get_rect(center=(center_x, center_y))
        self.image = self.images['normal']
        
        self.next_mission()

        # SnackAction일때만 추가되는 과자 이미지
        self.snackicon_img = pygame.image.load('images/snackicon.png')
        self.snackicon_img = pygame.transform.scale(self.snackicon_img, (140, 140))

    def next_mission(self):
        if self.remaining_missions:
            mission_cls = random.choice(self.remaining_missions)
            self.target_action = mission_cls()
            print(f"다음 미션: {mission_cls.__name__}")
        else:
            self.target_action = None
            print("모든 미션 클리어")
            
    def get_mission_name(self):
        if self.target_action:
            return self.target_action.__class__.__name__.replace('Action', '').upper()
        return None
            

    def set_state(self, state_name):
        if state_name in self.images:
            self.image = self.images[state_name]
            self.current = state_name
        else:
            self.image = self.images['normal']
            self.current = 'normal'
            
        Ocenter= self.rect.center
        self.rect= self.image.get_rect(center= Ocenter)

    def update(self, dt, keys):
        space_pressed = keys[pygame.K_SPACE]
        ctx = {
            "student": self,
            "sleep_pressed": False,
            "snack_pressed": False,
            "game_pressed": False
        }
        
        # 전체 스페이스바로 처리
        if self.target_action and space_pressed:
            # 현재 미션 종류 확인
            mission_type = type(self.target_action)
            
            if mission_type == SleepAction:
                ctx["sleep_pressed"] = True
            elif mission_type == SnackAction:
                ctx["snack_pressed"] = True
            elif mission_type == GameAction:
                ctx["game_pressed"] = True

            if self.current_action is None:
                if mission_type == SleepAction:
                    self.to_sleep(ctx)
                elif mission_type == SnackAction:
                    self.to_snack(ctx)
                elif mission_type == GameAction:
                    self.to_game(ctx)
                    
        # 스페이스바를 뗐다면 행동 중단
        if not space_pressed:
             self.stop_current_action(ctx)

        # 현재 진행 중인 액션 업데이트
        if self.current_action and self.current_action.is_active:
            self.current_action.execute(dt, ctx)
            
            # 미션 완료 체크
            if self.current_action.is_complete():
                action_cls = type(self.current_action)
                if action_cls in self.remaining_missions:
                    self.remaining_missions.remove(action_cls)
                    if not self.remaining_missions:
                        self.target_action = None
                        return "all_cleared" 
                    else:
                        self.next_mission()
                        return "mission_complete" 
        
        return None 

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # 현재 미션이 '과자먹기'라면 과자 이미지 넣기
        if isinstance(self.target_action, SnackAction):
            screen.blit(self.snackicon_img, (680, 440))

        if self.target_action:
            screen_w, screen_h = screen.get_size()
            bar_w = 500
            bar_h = 30
            bar_x = (screen_w - bar_w) // 2 + 30
            bar_y = screen_h - 60
            draw_mission_bar(screen, bar_x, bar_y, bar_w, bar_h, progress=self.target_action.progress)

    def to_sleep(self, ctx):
        self._start_action(SleepAction, "sleep", ctx)

    def to_snack(self, ctx):
        self._start_action(SnackAction, "snack", ctx)
 
    def to_game(self, ctx):
        self._start_action(GameAction, "game", ctx)
        
    def _start_action(self, action_cls, name: str, ctx):
        if not isinstance(self.target_action, action_cls):
            return
        self.current_action = self.target_action
        self.set_state(name)      
        self.current_action.start(ctx)
