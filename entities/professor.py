import random

class Professor:
    state: str          # 현재 교수님 상태
    watch_timer: float  # Watching 상태 지속 시간
    patrol_timer: float # Patrol 상태 지속 시간
    
    min_write = 2.0 # 최소 판서 시간
    max_write = 5.0 # 최대 판서 시간

    def __init__(self):
        self.state = "Writing"   # 초기 상태
        self.watch_timer = 0.0
        self.patrol_timer = 0.0
        self.write_timer = random.uniform(self.min_write, self.max_write) # 필기 지속 시간

    def update(self, dt):
        # 1. 감시 중일 때 (Watching)
        if self.state == "Watching":
            self.watch_timer -= dt
            if self.watch_timer <= 0:
                self.stop()

        # 2. 순찰 중일 때 (Patrol)
        elif self.state == "Patrol":
            self.patrol_timer -= dt
            if self.patrol_timer <= 0:
                self.stop()

        # 3. 필기 중일 때 (Writing) - 일정 확률 혹은 시간이 지나면 감시/순찰 시작
        elif self.state == "Writing":
            self.write_timer -= dt
            if self.write_timer <= 0:
                # 필기 시간이 끝나면 랜덤하게 감시 혹은 순찰 시작
                action = random.choice(["Watch", "Patrol"])
                
                if action == "Watch":
                    # 2~4초 동안 감시
                    self.start_watching(random.uniform(2.0, 4.0))
                else:
                    # 3~6초 동안 순찰
                    self.start_patrol(random.uniform(3.0, 6.0))

    def is_watching(self) -> bool:
        return self.state == "Watching" or self.state == "Patrol"

    def start_watching(self, duration: float):
        self.state = "Watching"
        self.watch_timer = duration
        print(f"(!) 교수님이 뒤를 돌아봅니다! ({duration:.1f}초간 감시)")

    def start_patrol(self, duration: float):
        self.state = "Patrol"
        self.patrol_timer = duration
        print(f"(발소리) 실습 시간! 교수님이 가까이 옵니다. ({duration:.1f}초간 순찰)")

    def stop(self):
        self.state = "Writing"
        self.write_timer = random.uniform(self.min_write, self.max_write)
        print("교수님이 다시 수업을 시작합니다!")