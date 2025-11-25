from SecretAction import SecretAction

class GameAction(SecretAction):
    def __init__(self): 
        super().__init__(name="game", total_time=10.0, total_hits=10)

    def start(self, ctx):
        super().start(ctx) 
        
        if not self.play_success:
            print(f"🎮 게임 시작!")

    def caught(self, ctx):
        print("교수님: '누가 수업 시간에 게임 소리를 내나!!'")
        super().caught(ctx) 
