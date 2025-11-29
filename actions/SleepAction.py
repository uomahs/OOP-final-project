from actions.SecretAction import SecretAction

class SleepAction(SecretAction):
    def __init__(self):
        super().__init__(name="sleep", total_time= 10.0, total_hits=10)

    def start(self, ctx):
        super().start(ctx) 

    def caught(self, ctx):
        super().caught(ctx) 

    def execute(self, dt, ctx):
        if not self.is_active or not ctx.get('sleep_pressed', False):
            return
        super().execute(dt, ctx)

        #ctx['student'].progress= self.progress