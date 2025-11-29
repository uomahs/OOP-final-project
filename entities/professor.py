import random
import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

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
        back_path = os.path.join(IMAGE_DIR, "professorBack.png")
        front_path = os.path.join(IMAGE_DIR, "professorFront.png")

        self.image_writing = pygame.image.load(back_path)
        self.image_watching = pygame.image.load(front_path)
        self.current_image = self.image_writing #현재 이미지

        self.rect = self.current_image.get_rect()
        self.rect.center = (self.x, self.y)

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

        #이미지 변경시 rect도 해당 이미지 기준으로 다시 만들어 같은 위치 유지
        old_center = self.rect.center
        self.rect = self.current_image.get_rect()
        self.rect.center = old_center

        print(f"(!) 교수님이 뒤를 돌아봅니다! ({duration:.1f}초간 감시)")

    def professor_stop(self):
        self.state = "Writing"
        self.write_timer = random.uniform(self.min_write, self.max_write)
        self.current_image = self.image_writing

        old_center = self.rect.center
        self.rect = self.current_image.get_rect()
        self.rect.center = old_center
        
        print("교수님이 다시 수업을 시작합니다!")

    def draw(self, surface: pygame.Surface):
        surface.blit(self.current_image, self.rect)