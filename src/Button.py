import pygame


class Button:
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, multiPress=False, textAlignment='center'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.multiPress = multiPress
        self.alreadyPressed = False
        self.textAlignment = textAlignment

        self.fillText = {
            'normal': '#7F7F7F',
            'hover': '#191919'
        }
        self.buttonText = buttonText
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonSurface.fill('#FFFFFF')
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = pygame.font.SysFont('Arial', 14).render(buttonText, True, '#7F7F7F')

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
                    if not self.multiPress and self.alreadyPressed:
                        if self.onclickFunction:
                            result = self.onclickFunction(funcArgs)
                        self.alreadyPressed = False
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                # self.buttonSurface.fill(self.fillColors['pressed'])
                if self.multiPress:
                    if self.onclickFunction:
                        result = self.onclickFunction(funcArgs)
        return result

    def render(self, screen):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurf = pygame.font.SysFont('Arial', 14).render(self.buttonText, True, self.fillText['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurf = pygame.font.SysFont('Arial', 14).render(self.buttonText, True, self.fillText['hover'])
        if self.textAlignment == 'center':
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
                self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
            ])
        elif self.textAlignment == 'right':
            self.buttonSurface.blit(self.buttonSurf, [
                15,
                self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
            ])
        screen.blit(self.buttonSurface, self.buttonRect)
