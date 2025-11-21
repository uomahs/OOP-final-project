import pygame
import os
import sys

# 경로 설정
BASE_DIR = os.path.dirname(__file__)          # OOP-final-project 폴더
IMAGE_PATH = os.path.join(BASE_DIR, "images", "background.png")


def main():
    # Pygame 초기화
    pygame.init()

    # 이미지 로드
    try:
        image = pygame.image.load(IMAGE_PATH)
    except pygame.error as e:
        print(f"[ERROR] 이미지 로드 실패: {IMAGE_PATH}")
        print(e)
        pygame.quit()
        sys.exit(1)

    # 이미지 크기에 맞춰 창 생성
    width, height = image.get_size()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("교수님 몰래 @@하기")

    clock = pygame.time.Clock()
    running = True

    # 메인 루프
    while running:
        clock.tick(60)  # FPS 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # ESC 눌러도 종료

        # 화면에 이미지 그리기
        screen.blit(image, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
