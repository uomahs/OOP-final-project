import pygame
import os

class Ending:
    STATE_NORMAL = 0
    STATE_HOVER  = 1
    STATE_ACTIVE = 2

    def __init__(self, ending_type):
        self.type = ending_type
        self.font = pygame.font.SysFont("malgungothic", 60, True)
        self.small_font = pygame.font.Font(None, 32)

        # 버튼 rect (충돌 체크용)
        self.rect = None
        self.state = Ending.STATE_NORMAL  # 버튼 상태

        base_dir = os.path.dirname(os.path.dirname(__file__))  # 프로젝트 루트
        img_dir = os.path.join(base_dir, "images")

        # 이미지 로드
        self.background_img = pygame.image.load(os.path.join(img_dir, "background.png"))
        self.restart_normal = pygame.image.load(os.path.join(img_dir, "restartbutton.png"))
        self.restart_hover  = pygame.image.load(os.path.join(img_dir, "restartHover.png"))
        self.restart_click  = pygame.image.load(os.path.join(img_dir, "restartClick.png"))

        # 공통 크기로 스케일
        button_size = (360, 350)

        self.restart_normal = pygame.transform.scale(self.restart_normal, button_size)
        self.restart_hover  = pygame.transform.scale(self.restart_hover,  button_size)
        self.restart_click  = pygame.transform.scale(self.restart_click,  button_size)

    def handle_button_event(self, event):
        if self.rect is None:
            return False

        if event.type not in (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        ):
            return False

        eventPointInButtonRect = self.rect.collidepoint(event.pos)

        if self.state == Ending.STATE_NORMAL:
            if eventPointInButtonRect:
                self.state = Ending.STATE_HOVER

        elif self.state == Ending.STATE_HOVER:
            if not eventPointInButtonRect:
                self.state = Ending.STATE_NORMAL
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.state = Ending.STATE_ACTIVE

        elif self.state == Ending.STATE_ACTIVE:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.state = Ending.STATE_NORMAL
                return True  # 클릭 완료

        return False

    def play(self, screen):        
        running = True
        clock = pygame.time.Clock()

        while running:
            screen.blit(self.background_img, (0,0))
            self.draw(screen)  # 여기서 self.rect 갱신

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                # mission_fail일 때만 버튼 동작
                if self.type == "mission_fail":
                    clicked = self.handle_button_event(event)
                    if clicked:
                        print("다시하기 클릭됨!")
                        return "retry"
                    
                elif self.type == "mission_success":
                    if (event.type == pygame.KEYDOWN or
                    (event.type == pygame.MOUSEBUTTONUP and event.button == 1)):
                        return "continue"
                    
                elif self.type == "class_end":
                    clicked = self.handle_button_event(event)
                    if clicked:
                        return "retry"

            pygame.display.flip()
            clock.tick(60)

        return "quit"

    def draw(self, screen):

        if self.type == "mission_success":  # 미션 하나 성공 -> 텍스트만
            text = self.font.render("Mission Completed!", True, (0, 255, 0))
            screen.blit(text, (350, 180))

        elif self.type == "mission_fail":   # 미션 실패 -> 텍스트 + 다시하기 버튼
            text= self.font.render("Mission Failed!", True, (255, 100, 100))
            screen.blit(text, (350, 180))
            self.draw_restart_button(screen)

        elif self.type == "class_end": # 모든 미션 성공시 수업 종료 출력
            text = self.font.render("Class has ended!", True, (0, 255, 0))
            screen.blit(text, (350, 180))
            self.draw_restart_button(screen)

        else:
            text = self.font.render("알 수 없는 엔딩", True, (255, 255, 255))
            screen.blit(text, (200, 200))
            
    def draw_restart_button(self, screen):
        base_img = self.restart_normal
        btn_w, btn_h = base_img.get_size()
        btn_x = (screen.get_width() - btn_w) // 2
        btn_y = 280

        if self.state == Ending.STATE_ACTIVE:
            img = self.restart_click
        elif self.state == Ending.STATE_HOVER:
            img = self.restart_hover
        else:
            img = self.restart_normal

        self.rect = img.get_rect(topleft=(btn_x, btn_y))
        screen.blit(img, self.rect.topleft)