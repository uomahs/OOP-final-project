import pygame

class Ending:
    def __init__(self, ending_type):
        self.type = ending_type
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.button_rect = None  # 다시하기 버튼 위치 저장

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
                            print("다시하기 클릭됨!")
                            return "retry"

            pygame.display.flip()
            clock.tick(60)

        return "quit"

    def draw(self, screen):
        if self.type == "mission_success": # 미션 하나 성공-> 텍스트만
            text = self.font.render("이번 미션 성공!", True, (255, 255, 255))
            screen.blit(text, (200, 200))

        elif self.type == "mission_fail": #미션 실패-> 텍스트, 다시하기 버튼
            text = self.font.render("미션 실패!", True, (255, 100, 100))
            screen.blit(text, (200, 150))

            button_text = self.small_font.render("다시하기", True, (0, 0, 0))
            btn_w, btn_h = 160, 50
            btn_x, btn_y = 200, 280

            self.button_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            pygame.draw.rect(screen, (255, 255, 255), self.button_rect)
            screen.blit(button_text, (btn_x + 30, btn_y + 10))

        elif self.type == "class_end": # 모든 미션 성공시 수업 종료 출력
            text = self.font.render("Class has ended!", True, (200, 255, 200))
            screen.blit(text, (150, 200))

        else:
            text = self.font.render("알 수 없는 엔딩", True, (255, 255, 255))
            screen.blit(text, (200, 200))

