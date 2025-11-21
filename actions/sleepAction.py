from actions.SecretAction import SecretAction

class SleepAction(SecretAction):
    def __init__(self, sleep_time=2.0, point=15):
        super().__init__(name="졸기", point=point)
        self.sleep_time = sleep_time
        self.sleep_timer = 0.0
        self.sleep_success = False

    def start(self, ctx):
        super().start(ctx)
        self.sleep_success = False
        self.sleep_timer = 0.0
        print("졸기 시작")

    def execute(self, dt, ctx):
        if not self.is_active:
            return

        if ctx.professor.is_watching():
            self.caught(ctx)
            return

        self.sleep_timer += dt
        self.progress = min(self.sleep_timer / self.sleep_time, 1.0)

        if self.progress >= 1.0 and not self.sleep_success:
            self.sleep_success = True
            self.is_active = False
            ctx.student.update_score(self.point)
            print("졸기 성공!", self.point)

    def stop(self, ctx):
        if not self.sleep_success:  
            print("졸기 실패! 너무 일찍 일어남")
        super().stop(ctx)

    def caught(self, ctx):
        self.sleep_success = False
        self.is_active = False
        print("교수님께 걸림! 졸기 실패")
