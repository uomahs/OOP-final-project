import pygame

class SecretAction:
    def __init__(self, name, point=10):
        self.name = name          
        self.point = point        
        self.is_active = False    
        self.progress = 0.0       
        self.score = 0            
    
    def start(self, ctx): 
        if not self.is_complete():
            self.is_active = True
            # 각 미션에 해당하는 액션을 나타내는 모션 넣기

    def stop(self, ctx): 
        if self.is_active:
            self.is_active = False
            # 각 미션에 해당하는 액션을 하다가 아무것도 안하는 모션으로 바꾸기

    def execute(self, dt, ctx): 
        if not self.is_active:
            return

        pass 

    def caught(self, ctx): 
        self.stop(ctx)
        # 걸렸을 때 나타낼 문구 출력
        if 'game' in ctx:
            ctx['game'].set_state('GAME_OVER')

    def is_complete(self):
        return self.progress >= 1.0