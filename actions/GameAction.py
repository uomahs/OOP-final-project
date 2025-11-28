from actions.SecretAction import SecretAction

class GameAction(SecretAction):
    def __init__(self): 
        super().__init__(name="game", total_time=10.0, total_hits=10)

    def start(self, ctx):
        super().start(ctx) 

    def caught(self, ctx):
        print("교수님: '누가 수업 시간에 게임 소리를 내나!!'")
        super().caught(ctx) 
        
    def execute(self, dt, ctx):
        if not self.is_active or not ctx.get('game_pressed', False):
            return
        super().execute(dt, ctx)
