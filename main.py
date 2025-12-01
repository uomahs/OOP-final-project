import pygame
import os
import sys

from SimpleButton import SimpleButton
from entities.Student import Student
from entities.professor import Professor
from ending.ending import Ending

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
    screen = pygame.display.set_mode((800, 600))
    student_w, student_h = screen.get_size()
    student = Student(student_w, student_h)

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
    bg_w, bg_h = background_img.get_size()
    screen = pygame.display.set_mode((bg_w, bg_h))
    pygame.display.set_caption("교수님 몰래 @@하기")

    professor = Professor(350, 216)

    # SimpleButton 객체 생성
    startbutton = SimpleButton(
        window=screen,
        loc=(360, 350),
        img_normal=startbutton_img,
        img_hover=startbutton_hov_img,
        img_active=startbutton_clk_img)
    
    running = True
    game_state = "TITLE"

    font = pygame.font.SysFont(None, 50)
    
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
            dt= clock.get_time()/ 1000.0
            keys= pygame.key.get_pressed()

            student_status = student.update(dt, keys)
            result = professor.update(dt, student)
            
            if student_status == "mission_complete":
                ending = Ending("mission_success")
                outcome = ending.play(screen)
                if outcome == "quit":
                    running = False

            elif student_status == "all_cleared":
                ending = Ending("class_end")
                outcome = ending.play(screen)
                if outcome == "retry":
                    student = Student(student_w, student_h)
                    professor = Professor(350, 216)
                    game_state = "TITLE"
                    continue

                elif outcome == "quit":
                    running = False     

            if result == "caught":
                ending = Ending("mission_fail")
                outcome = ending.play(screen)

                if outcome == "retry":
                    student = Student(student_w, student_h)
                    prof_x = int(bg_w * 0.35)
                    prof_y = int(bg_h * 0.33)
                    professor = Professor(prof_x, prof_y)
                    game_state = "TITLE"
                    continue

                elif outcome == "quit":
                    running = False
                    continue

            screen.blit(background_img, (0,0))
            professor.draw(screen)
            student.draw(screen)
            mission_name = student.get_mission_name()

            if mission_name:
                mission_text = f"STAGE MISSION: {mission_name.replace('Action', '').upper()}"
                text_surface = font.render(mission_text, True, (255, 0, 0)) 
                screen.blit(text_surface, (50, 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()