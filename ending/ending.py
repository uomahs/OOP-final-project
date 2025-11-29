import pygame
import os

class Ending:
    STATE_NORMAL = 0
    STATE_HOVER  = 1
    STATE_ACTIVE = 2

    def __init__(self, ending_type):
        self.type = ending_type
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        # 버튼 rect (충돌 체크용)
        self.rect = None
        self.state = Ending.STATE_NORMAL  # 버튼 상태

        base_dir = os.path.dirname(os.path.dirname(__file__))  # 프로젝트 루트
        img_dir = os.path.join(base_dir, "images")

        # 원본 이미지 로드
        self.restart_normal = pygame.image.load(os.path.join(img_dir, "restartbutton.png"))
        self.restart_hover  = pygame.image.load(os.path.join(img_dir, "restartHover.png"))
        self.restart_click  = pygame.image.load(os.path.join(img_dir, "restartClick.png"))

        # 공통 크기로 스케일
        btn_w, btn_h = self.restart_normal.get_size()
        target_width = 350
        ratio = target_width / btn_w
        new_size = (target_width, int(btn_h * ratio))

        self.restart_normal = pygame.transform.scale(self.restart_normal, new_size)
        self.restart_hover  = pygame.transform.scale(self.restart_hover,  new_size)
        self.restart_click  = pygame.transform.scale(self.restart_click,  new_size)

    def handle_button_event(self, event):
        """SimpleButton.handleEvent와 거의 동일한 버튼 상태 머신"""
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
        """엔딩 화면 루프"""
        running = True
        clock = pygame.time.Clock()

        while running:
            screen.fill((0, 0, 0))
            self.draw(screen)  # 여기서 self.rect 갱신됨

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
                    if (event.type == pygame.KEYDOWN or
                        (event.type == pygame.MOUSEBUTTONUP and event.button == 1)):
                        return "quit"

            pygame.display.flip()
            clock.tick(60)

        return "quit"

    def draw(self, screen):
        if self.type == "mission_success":  # 미션 하나 성공 -> 텍스트만
            text = self.font.render("mission success!", True, (255, 255, 255))
            screen.blit(text, (200, 200))

        elif self.type == "mission_fail":   # 미션 실패 -> 텍스트 + 다시하기 버튼
            text = self.font.render("mission failed!", True, (255, 100, 100))
            screen.blit(text, (200, 150))

            # 버튼 위치 계산 (가운데 정렬)
            base_img = self.restart_normal  # 크기 기준용
            btn_w, btn_h = base_img.get_size()
            btn_x = (screen.get_width() - btn_w) // 2
            btn_y = 280

            # 상태에 따라 그릴 이미지 결정 (SimpleButton.draw()와 동일)
            if self.state == Ending.STATE_ACTIVE:
                img = self.restart_click
            elif self.state == Ending.STATE_HOVER:
                img = self.restart_hover
            else:
                img = self.restart_normal

            # rect 업데이트 (충돌 체크용)
            self.rect = img.get_rect(topleft=(btn_x, btn_y))
            screen.blit(img, self.rect.topleft)

        elif self.type == "class_end": # 모든 미션 성공시 수업 종료 출력
            text = self.font.render("Class has ended!", True, (200, 255, 200))
            screen.blit(text, (150, 200))

        else:
            text = self.font.render("알 수 없는 엔딩", True, (255, 255, 255))
            screen.blit(text, (200, 200))