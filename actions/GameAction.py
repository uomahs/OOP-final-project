from SecretAction import SecretAction
import pygame

class GameAction(SecretAction):
    def __init__(self, session_time=10.0, point_game=20): 
        super().__init__(name="game", point=point_game)
    
        self.session_time = session_time     
        self.elapsed = 0.0                    
        self.success_hits = 0                 
        self.required_hits = 10               
        self.play_success = False             
        self.time_per_hit = self.session_time / self.required_hits

    def start(self, ctx):
        super().start(ctx) 
        
        if not self.play_success:
            print(f"게임 시작! (목표: {self.required_hits} 스테이지)")

    def execute(self, dt, ctx):
        if not self.is_active or self.is_complete():
            return

        professor = ctx.get('professor')
        if professor and professor.is_looking_back:
            self.caught(ctx)
            return

        self.elapsed += dt
        
        while self.elapsed >= self.time_per_hit:
            self.elapsed -= self.time_per_hit 
            self.success_hits += 1
        self.progress = self.success_hits / self.required_hits

        if self.is_complete():
            self.play_success = True
            print(f"게임 클리어! 점수 {self.point}점 획득!")
            self.stop(ctx)

    def caught(self, ctx):
        print("교수님: '누가 수업 시간에 게임 소리를 내나!!'")
        super().caught(ctx) 

    def stop(self, ctx):
        super().stop(ctx) 
