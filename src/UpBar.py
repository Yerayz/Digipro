import pygame

from DragBar import DragBar


class UpBar:
    def __init__(self):
        self.x = 150 + 150/2
        self.y = 0
        self.width = 900 - 150 - 150
        self.height = 30
        self.isActive = False
        self.option = {
            'brighten': [['Amount', DragBar(0, 0, 100, 10, -20, 20)]],  # Text, (x, y, width, currVal, minVal, maxVal)
            'contrast': [['Amount', DragBar(0, 0, 100, 10, -20, 20)]],
            'sharp': [['Amount', DragBar(0, 0, 100, 10, -20, 20)]],
            'blur': [['Size', DragBar(0, 0, 50, 10, 1, 20)]],
            'invert': [],
            'dual': [['1:Red  2:Green  3:Blue', DragBar(0, 0, 30, 1, 1, 3)]],
            'edge': [],
            'emboss': [],
            'contour': []
        }
        self.selected = 'blur'
        self.barSurface = pygame.Surface((self.width+2, self.height+2))
        self.barRect = pygame.Rect(self.x-1, self.y-1, self.width+2, self.height+2)
        self.barSurface.fill('#FFFFFF')
        pygame.draw.rect(self.barSurface, '#E6E6E6', pygame.Rect(0, 0, self.width+2, self.height+2), width=1)

    def setIsActive(self, isActive):
        self.isActive = isActive

    def process(self, filters, events):
        if not self.isActive:
            return
        for i, component in enumerate(self.option[self.selected]):
            component[1].process(events)
            filters[self.selected][i+1] = component[1].getCurrVal()

    def render(self, screen):
        if not self.isActive:
            return
        surface = self.barSurface
        surface.fill('#FFFFFF')
        # w_screen, h_screen = screen.get_size()
        # self.width = w_screen - 150 - 150
        # pygame.draw.rect(screen, '#FFFFFF', )
        # pygame.draw.rect(screen, '#E6E6E6', pygame.Rect(self.x-1, self.y-1, self.width+2, self.height+2), width=1)  # Border


        i = 0
        for ind, component in enumerate(self.option[self.selected]):
            if ind > 0:
                i = i + 20
                pygame.draw.line(surface, '#E6E6E6', (i, surface.get_rect().height * 0.2), (i, surface.get_rect().height * 0.8), width=1)
            i = i + 20
            textSurf = pygame.font.SysFont('Arial', 14).render(component[0], True, '#7F7F7F')
            surface.blit(textSurf, [i, surface.get_rect().height / 2 - textSurf.get_rect().height / 2])
            i = i + textSurf.get_rect().width + 10
            # component[1].render(surface, i)
            component[1].setPos(self.barRect.x + i, surface.get_rect().height / 2)
            i = i + component[1].width + 10
            textSurf = pygame.font.SysFont('Arial', 14).render(str(component[1].getPreviewVal()), True, '#7F7F7F')
            surface.blit(textSurf, [i, surface.get_rect().height / 2 - textSurf.get_rect().height / 2])
            i = i + textSurf.get_rect().width

        screen.blit(self.barSurface, self.barRect)
        for component in self.option[self.selected]:
            component[1].render(screen)
