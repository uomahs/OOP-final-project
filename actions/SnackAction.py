from SecretAction import SecretAction

class SnackAction(SecretAction):
    def __init__(self):
        super().__init__(name="snack", total_time=10.0, total_hits=10)

    def start(self, ctx):
        super().start(ctx)

    def caught(self, ctx):
        print("교수님: '누가 수업 시간에 과자를 먹나!!'")
        super().caught(ctx) 
    
    def execute(self, dt, ctx):
        if not self.is_active or not ctx.get('snack_pressed', False):
            return
        super().execute(dt, ctx)