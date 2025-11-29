import pygame
import os

class Ending:
    def __init__(self, ending_type):
        self.type = ending_type
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.button_rect = None  # 다시하기 버튼 위치 저장

        base_dir = os.path.dirname(os.path.dirname(__file__)) #파일 루트까지 올리기 위해
        img_dir = os.path.join(base_dir, "images")

        self.restart_normal = pygame.image.load(os.path.join(img_dir, "restartbutton.png"))
        self.restart_hover = pygame.image.load(os.path.join(img_dir, "restartHover.png"))
        self.restart_click = pygame.image.load(os.path.join(img_dir, "restartClick.png"))

        btn_w, btn_h = self.restart_normal.get_size()
        target_width = 350
        ratio = target_width / btn_w
        new_size = (target_width, int(btn_h * ratio))

        self.restart_normal = pygame.transform.scale(self.restart_normal, new_size)
        self.restart_hover  = pygame.transform.scale(self.restart_hover,  new_size)
        self.restart_click  = pygame.transform.scale(self.restart_click,  new_size)

        self.restart_img = self.restart_normal
        self.is_mouse_down = False

    def play(self, screen):
        """엔딩 화면 루프"""
        running = True
        clock = pygame.time.Clock()

        while running:
            screen.fill((0, 0, 0)) 
            self.draw(screen) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.type == "mission_fail" and self.button_rect:
                        if self.button_rect.collidepoint(event.pos):
                            if self.is_mouse_down:
                                self.restart_img = self.restart_click
                            else:
                                self.restart_img = self.restart_hover
                        else:
                            self.restart_img = self.restart_normal

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.type == "mission_fail" and self.button_rect:
                        if self.button_rect.collidepoint(event.pos):
                            self.is_mouse_down = True
                            self.restart_img = self.restart_click

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.type == "mission_fail" and self.button_rect:
                        if self.button_rect.collidepoint(event.pos) and self.is_mouse_down:
                            print("다시하기 클릭됨!")
                            self.is_mouse_down = False
                            self.restart_img = self.restart_hover
                            #여기서 메인/타이틀로 돌아가게 signal 보냄
                            return "retry"
                    self.is_mouse_down = False

            pygame.display.flip()
            clock.tick(60)

        return "quit"

    def draw(self, screen):
        if self.type == "mission_success": # 미션 하나 성공-> 텍스트만
            text = self.font.render("mission success!", True, (255, 255, 255))
            screen.blit(text, (200, 200))

        elif self.type == "mission_fail": #미션 실패-> 텍스트, 다시하기 버튼
            text = self.font.render("mission failed!", True, (255, 100, 100))
            screen.blit(text, (200, 150))

            btn_w, btn_h = self.restart_img.get_size()
            btn_x = (screen.get_width() - btn_w) // 2
            btn_y = 280

            self.button_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            screen.blit(self.restart_img, self.button_rect.topleft)

        elif self.type == "class_end": # 모든 미션 성공시 수업 종료 출력
            text = self.font.render("수업이 종료되었습니다!", True, (200, 255, 200))
            screen.blit(text, (150, 200))

        else:
            text = self.font.render("알 수 없는 엔딩", True, (255, 255, 255))
            screen.blit(text, (200, 200))