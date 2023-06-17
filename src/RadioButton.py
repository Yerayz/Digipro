import pygame


class RadioButton:
    def __init__(self, x, y, width, height, filterId, onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.filterId = filterId
        self.onclickFunction = onclickFunction
        self.isActive = False
        self.alreadyPressed = False

        self.fillColor = {
            'normal': '#FFFFFF',
            'hover': '#F5F5F5'
        }
        self.radioColor = {
            'normal': '#7F7F7F',
            'hover': '#191919'
        }
        # self.buttonText = buttonText
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonSurface.fill('#FFFFFF')
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        # self.buttonSurf = pygame.font.SysFont('Arial', 14).render(buttonText, True, '#7F7F7F')

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self, funcArgs, events):
        result = None
        mousePos = pygame.mouse.get_pos()
        # self.buttonSurf = pygame.font.SysFont('Arial', 14).render(self.buttonText, True, self.fillText['normal'])
        if self.buttonRect.collidepoint(mousePos):
            # self.buttonSurf = pygame.font.SysFont('Arial', 14).render(self.buttonText, True, self.fillText['hover'])
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.alreadyPressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.alreadyPressed:
                        self.isActive = not self.isActive
                        self.alreadyPressed = False
                        result = self.onclickFunction(funcArgs + [self.filterId, self.isActive])
        return result

    def render(self, screen):
        mousePos = pygame.mouse.get_pos()
        center = [self.buttonRect.width / 2, self.buttonRect.height / 2]
        color = self.radioColor['normal']
        self.buttonSurface.fill(self.fillColor['normal'])
        # pygame.draw.circle(self.buttonSurface, self.radioColor['normal'], center, 8, width=1)
        if self.buttonRect.collidepoint(mousePos):
            color = self.radioColor['hover']
            self.buttonSurface.fill(self.fillColor['hover'])
            # pygame.draw.circle(self.buttonSurface, self.radioColor['normal'], center, 8, width=1)
        pygame.draw.circle(self.buttonSurface, color, center, 6, width=1)
        if self.isActive:
            pygame.draw.circle(self.buttonSurface, color, center, 4)
        screen.blit(self.buttonSurface, self.buttonRect)
