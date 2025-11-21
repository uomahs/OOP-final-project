from SecretAction import SecretAction
import pygame

class SnackAction(SecretAction):
    def __init__(self, snack_bag=100, point_snack=10, eat_speed=10.0):
        super().__init__(name="snack", point=point_snack)

        self.snack_bag_total = snack_bag
        self.remain_snack = snack_bag
        self.point_snack = point_snack
        self.eat_speed = eat_speed
        self.is_eating = False

    def start(self, ctx):
        super().start(ctx)
        if not self.is_active:
            return
        self.is_eating = True

    def stop(self, ctx):
        super().stop(ctx)
        self.is_eating = False

    def execute(self, dt, ctx):
        #액션 x, 먹는 중 x -> 아무 것도 안 함
        if not self.is_active or not self.is_eating:
            return
        
        #과자 감소
        self.remain_snack -= self.eat_speed * dt
        if self.remain_snack < 0:
            self.remain_snack = 0
        
        #progress 갱신
        self.progress = 1.0 - (self.remain_snack / self.snack_bag_total)

        #score 갱신
        self.score += self.point_snack * dt

        #엔딩으로 이동 (미션 완료)
        
    def caught(self, ctx):
        print("교수님; '누가 수업 시간에 과자를 먹나!!")
        super().caught(ctx)