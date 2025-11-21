from specialAction import SecretAction
import pygame

class SnackAction(SecretAction):
    def __init__(self, snack_bag=100, point_snack=10):
        super().__init__(name="snack", point=point_snack)

        self.snack_bag_total = snack_bag
        self.remain_snack = snack_bag
        
        self.eat_speed = 10.0

    def start(self, ctx):
        if self.is_complete():
            print("Sanck misson finished!")
            return
        super().start(ctx)
        #과자 먹는 모션으로

    def stop(self, ctx):
        was_active = self.is_active
        super().stop(ctx)

        if was_active:
            #수업 듣는 모션으로
            pass

    def execute(self, dt, ctx):
        if not self.is_active:
            return
        if self.remain_snack <= 0:
            if not self.is_complete():
                self.progress = 1.0
            self.stop(ctx)
            return
        self.remain_snack -= self.eat_speed * dt
        self.score += self.point * dt

        self.progress = 1.0 - (self.remain_snack / self.snack_bag_total)

        if self.remain_snack <= 0:
            self.remain_snack = 0
            self.progress = 1.0

            #엔딩으로 이동 (미션 완료)
        
    def caught(self, ctx):
        print("교수님; '누가 수업 시간에 과자를 먹나!!")
        super().caught(ctx)