import pygame


class DragBar:
    def __init__(self, x, y, width, currVal, minVal, maxVal):
        self.x = x
        self.y = y
        self.width = width
        self.height = 3
        self.currVal = currVal
        self.previewVal = currVal
        self.minVal = minVal
        self.maxVal = maxVal

        self.barSurface = pygame.Surface((width, 2))
        self.barSurface.fill('#7F7F7F')
        self.barRect = pygame.Rect(x, y, width, 2)
        self.pointSurface = pygame.Surface((5, 5))
        pygame.draw.circle(self.pointSurface, '#7F7F7F', [2, 2], 2)
        self.pointRect = pygame.Rect(x + ((currVal - minVal) / (maxVal - minVal) * width), y, 5, 5)

        self.rectangle_dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.barRect = pygame.Rect(x, y - self.barSurface.get_rect().height / 2, self.width, 2)
        # self.pointRect = pygame.Rect(x, y - self.pointSurface.get_rect().height / 2, 5, 5)

    def getCurrVal(self):
        return self.currVal

    def getPreviewVal(self):
        return self.previewVal

    def process(self, events):
        mousePos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mousePos
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # print("Hold")
                    if self.pointRect.collidepoint(mousePos):
                        # print("Point")
                        self.rectangle_dragging = True
                    elif self.barRect.collidepoint(mousePos):
                        # print("Bar")
                        self.rectangle_dragging = True
                        self.currVal = int((mouse_x - self.x) / self.width * self.maxVal)
                        # mouse_x, mouse_y = event.pos
                        # self.offset_x = rectangle.x - mouse_x
                        # self.offset_y = rectangle.y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.rectangle_dragging = False
                    self.currVal = self.previewVal

            elif event.type == pygame.MOUSEMOTION:
                if self.rectangle_dragging:
                    self.previewVal = ((mouse_x - self.x) / self.width * (self.maxVal - self.minVal)) + self.minVal
                    self.previewVal = int(self.previewVal) if self.previewVal <= self.maxVal else self.maxVal
                    self.previewVal = int(self.previewVal) if self.previewVal >= self.minVal else self.minVal

        self.pointRect = pygame.Rect(self.x + ((self.previewVal - self.minVal) / (self.maxVal - self.minVal) * self.width) - 2, self.y - self.pointSurface.get_rect().height / 2, 5, 5)
                    # print('Point')
        # elif self.barRect.collidepoint(mousePos):
            # print('Bar')

    def render(self, screen):
        # pygame.draw.rect(screen, '#E6E6E6', pygame.Rect(self.x, self.y, self.width, self.height))
        # center = [self.controlPointBox.x-self.controlPointBox.width, self.controlPointBox.y-self.controlPointBox.height]
        # pygame.draw.circle(screen, '#E6E6E6', center, 4)

        # screen.blit(self.barSurface, [x, screen.get_rect().height / 2 - self.barSurface.get_rect().height / 2])
        # screen.blit(self.pointSurface, self.pointRect)

        screen.blit(self.barSurface, self.barRect)
        screen.blit(self.pointSurface, self.pointRect)
