import pygame

class SimpleButton:
    STATE_NORMAL = 0
    STATE_HOVER = 1
    STATE_ACTIVE = 2

    def __init__(self, window, loc, img_normal, img_hover, img_active):
        """
        window: 그림을 그릴 대상(screen)
        loc: 버튼의 중심 좌표 (x, y) 튜플
        img_*: 로드된 pygame image 객체들
        """
        self.window = window
        self.loc = loc
        self.surfaceUp = img_normal
        self.surfaceOn = img_hover
        self.surfaceDown = img_active
        
        self.rect = self.surfaceOn.get_rect(topleft=loc)

        self.state = SimpleButton.STATE_NORMAL

    def handleEvent(self, eventObj):
        if eventObj.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            return False
        
        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos)

        if self.state == SimpleButton.STATE_NORMAL:
            if eventPointInButtonRect:
                self.state = SimpleButton.STATE_HOVER

        elif self.state == SimpleButton.STATE_HOVER:
            if not eventPointInButtonRect:
                self.state = SimpleButton.STATE_NORMAL
            if eventObj.type == pygame.MOUSEBUTTONDOWN:
                self.state = SimpleButton.STATE_ACTIVE

        elif self.state == SimpleButton.STATE_ACTIVE:
            if eventObj.type == pygame.MOUSEBUTTONUP:
                self.state = SimpleButton.STATE_NORMAL
                return True 

        return False

    def draw(self):
        # 상태에 따라 그릴 이미지 결정
        if self.state == SimpleButton.STATE_ACTIVE:
            image_to_draw = self.surfaceDown
        elif self.state == SimpleButton.STATE_HOVER:
            image_to_draw = self.surfaceOn
        else: 
            image_to_draw = self.surfaceUp
            
        self.window.blit(image_to_draw, self.rect)