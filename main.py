import pygame
import os
import sys

from SimpleButton import SimpleButton

# 경로 설정
BASE_DIR = os.path.dirname(__file__)          # OOP-final-project 폴더
IMAGE_DIR = os.path.join(BASE_DIR, "images")

BACKGROUND_PATH = os.path.join(BASE_DIR, "images", "background.png")
TITLE_PATH = os.path.join(BASE_DIR, 'images', 'title.png') 
STARTBUTTON_PATH = os.path.join(BASE_DIR, 'images', 'gamestartbutton.png')
STARTBUTTON_HOV_PATH = os.path.join(BASE_DIR, 'images', 'gamestartHover.png')
STARTBUTTON_CLK_PATH = os.path.join(BASE_DIR, 'images', 'gamestartClick.png')

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # 이미지 로드
    background_img = pygame.image.load(BACKGROUND_PATH)
    title_img = pygame.image.load(TITLE_PATH)
    title_img = pygame.transform.scale(title_img, (600, 550))
    startbutton_img = pygame.image.load(STARTBUTTON_PATH)
    startbutton_img = pygame.transform.scale(startbutton_img, (300, 250))
    startbutton_hov_img = pygame.image.load(STARTBUTTON_HOV_PATH)
    startbutton_hov_img = pygame.transform.scale(startbutton_hov_img, (300, 250))
    startbutton_clk_img = pygame.image.load(STARTBUTTON_CLK_PATH)
    startbutton_clk_img = pygame.transform.scale(startbutton_clk_img, (300, 250))

    # 이미지 크기에 맞춰 창 생성
    width, height = background_img.get_size()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("교수님 몰래 @@하기")
    
    # SimpleButton 객체 생성
    startbutton = SimpleButton(
        window=screen,
        loc=(360, 350),
        img_normal=startbutton_img,
        img_hover=startbutton_hov_img,
        img_active=startbutton_clk_img)
    
    running = True
    game_state = "TITLE"

    while running:
        clock.tick(60)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # ESC 눌러도 종료

            if game_state == "TITLE":
                if startbutton.handleEvent(event):
                    print("게임 시작!")
                    game_state = "PLAY"

        # 화면에 이미지 그리기
        if game_state == "TITLE":
            screen.blit(background_img, (0, 0))
            screen.blit(title_img, (220, -10))
            startbutton.draw()
        elif game_state == "PLAY":
            screen.blit(background_img, (0,0))
            # 게임 로직...

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()