import random
import pygame

class Professor:
    state: str          # 현재 교수님 상태
    watch_timer: float  # Watching 상태 지속 시간
    
    min_write = 2.0 # 최소 판서 시간
    max_write = 5.0 # 최대 판서 시간

    def __init__(self, x:int, y:int):
        # 위치 (교수님 기준 위치)
        self.x = x
        self.y = y

        # 상태 초기화
        self.state = "Writing"
        self.watch_timer = 0.0
        self.write_timer = random.uniform(self.min_write, self.max_write) # 필기 지속 시간

        # 이미지 로드
        self.image_writing = pygame.image.load("OOP-final-project/images/professorBack.png")
        self.image_watching = pygame.image.load("OOP-final-project/images/professorFront.png")
        self.current_image = self.image_writing

    def update(self, dt):
        # 감시 중일 때 (Watching)
        if self.state == "Watching":
            self.watch_timer -= dt
            if self.watch_timer <= 0:
                self.professor_stop()

        # 필기 중일 때 (Writing) - 일정 확률 혹은 시간이 지나면 감시
        elif self.state == "Writing":
            self.write_timer -= dt
            if self.write_timer <= 0:
               duration = random.uniform(2.0, 4.0)
               self.start_watching(duration)

    def is_watching(self) -> bool:
        return self.state == "Watching"

    def start_watching(self, duration: float):
        self.state = "Watching"
        self.watch_timer = duration
        self.current_image = self.image_watching
        print(f"(!) 교수님이 뒤를 돌아봅니다! ({duration:.1f}초간 감시)")

    def professor_stop(self):
        self.state = "Writing"
        self.write_timer = random.uniform(self.min_write, self.max_write)
        self.current_image = self.image_writing
        print("교수님이 다시 수업을 시작합니다!")

    def draw(self, surface: pygame.Surface):
        rect = self.init_image.get_rect()
        rect.center = (self.x, self.y)
        surface.blit(self.init_image, rect)