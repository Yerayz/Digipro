import pygame
import sys
import os
from tkinter import *
from tkinter import filedialog
from PIL import ImageOps, Image as Img

from UpBar import UpBar
from Button import Button
from Image import Image
from RadioButton import RadioButton


def myFunction(args):
    print('Button Pressed')


def browseFile(args):
    Tk().withdraw()
    filename = filedialog.askopenfilename(filetypes=[('Image', ('.png', '.jpg', 'jpeg'))])
    return filename


def exportImage(args):
    if args[0]:
        image_array = pygame.surfarray.array3d(args[0].previewImage)
        image = Img.fromarray(image_array)
        image = ImageOps.exif_transpose(image)
        image = ImageOps.mirror(image.rotate(270, expand=True))
        files = [('Image', ('*.png', '*.jpg', '*.jpeg'))]
        Tk().withdraw()
        f = filedialog.asksaveasfile(mode='wb', initialfile=args[0].filename, filetypes=files, defaultextension=files)
        if f:
            image.save(f)


def changeFilterFlag(args):
    global filterIsExpanded
    filterIsExpanded = not filterIsExpanded


def changeAdjustmentFlag(args):
    global adjustmentIsExpanded
    adjustmentIsExpanded = not adjustmentIsExpanded


def setFilter(args):  # [filters, filterId, isActive]
    # print(args)
    args[0][args[1]][0] = args[2]  # filters[filterId][0] = isActive


def executeBlur(args):
    if args[0]:
        args[0].blur()


def setUpBar(args):  # UpBar, 'blur'
    if not args[0].isActive:
        args[0].isActive = True
        args[0].selected = args[1]
    elif args[0].selected == args[1]:
        args[0].isActive = False
    else:
        args[0].selected = args[1]


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((900, 480), pygame.RESIZABLE)
pygame.mouse.set_visible(True)
font = pygame.font.SysFont('Arial', 40)
pygame.display.set_caption('Digipro')

objects = []  # List of tuple (Object, isVisible, isRadio)
file = None
filterIsExpanded = False
adjustmentIsExpanded = False
filters = {
    'brighten': [False, 10],
    'contrast': [False, 10],
    'sharp': [False, 10],
    'blur': [False, 10],
    'invert': [False],
    'dual': [False, 1],
    'edge': [False],
    'emboss': [False],
    'contour': [False]
}
upBar = UpBar()

objects.append([Button(1, 1, 149, 30, 'Open Image', browseFile), True, False])
objects.append([Button(1, 31, 149, 30, 'Adjustment', changeAdjustmentFlag), True, False])
objects.append([Button(1, 61, 149, 30, 'Brightness', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 63, 24, 24, 'brighten', setFilter), False, True])
objects.append([Button(1, 61, 149, 30, 'Contrast', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 63, 24, 24, 'contrast', setFilter), False, True])
objects.append([Button(1, 61, 149, 30, 'Sharpness', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 63, 24, 24, 'sharp', setFilter), False, True])
objects.append([Button(1, 31, 149, 30, 'Filters', changeFilterFlag), True, False])
objects.append([Button(1, 61, 149, 30, 'Gaussian Blur', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 63, 24, 24, 'blur', setFilter), False, True])
objects.append([Button(1, 91, 149, 30, 'Invert', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 93, 24, 24, 'invert', setFilter), False, True])
objects.append([Button(1, 91, 149, 30, 'Dual Channel', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 93, 24, 24, 'dual', setFilter), False, True])
objects.append([Button(1, 91, 149, 30, 'Edge Enhance', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 93, 24, 24, 'edge', setFilter), False, True])
objects.append([Button(1, 91, 149, 30, 'Emboss', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 93, 24, 24, 'emboss', setFilter), False, True])
objects.append([Button(1, 91, 149, 30, 'Contour', setUpBar, textAlignment='right'), False, False])
objects.append([RadioButton(117, 93, 24, 24, 'contour', setFilter), False, True])
objects.append([Button(1, 121, 149, 30, 'Export', exportImage), True, False])

while True:
    clock.tick(30)

    # Process
    events = pygame.event.get()
    res = objects[0][0].process([], events)  # 'Open Image' Button
    if res:
        file = Image(os.path.basename(res), pygame.image.load(res))

    # for object in objects[:2]:  # 'Filters', 'Export', etc Buttons
    #     object[0].process([], events)
    # for object in objects[2:6]:  # Filters Buttons
    #     if object[1]:
    #         if object[2]:
    #             object[0].process([filters], events)
                # filters = res if res else filters
                # if res:
                #     filters = res
                #     print(file.filters, filters)
            # else:
            #     object[0].process([file], events)
    if objects[0][1]: objects[0][0].process([], events)  # Open Image
    if objects[1][1]: objects[1][0].process([], events)  # Adjustment
    if objects[2][1]: objects[2][0].process([upBar, 'brighten'], events)  # Brightness
    if objects[3][1] and objects[3][2]: objects[3][0].process([filters], events)  # Brightness Radio
    if objects[4][1]: objects[4][0].process([upBar, 'contrast'], events)  # Contrast
    if objects[5][1] and objects[5][2]: objects[5][0].process([filters], events)  # Sharpness Radio
    if objects[6][1]: objects[6][0].process([upBar, 'sharp'], events)  # Sharpness
    if objects[7][1] and objects[7][2]: objects[7][0].process([filters], events)  # Contrast Radio
    if objects[8][1]: objects[8][0].process([], events)  # Filters
    if objects[9][1]: objects[9][0].process([upBar, 'blur'], events)  # Blur
    if objects[10][1] and objects[10][2]: objects[10][0].process([filters], events)  # Blur Radio
    if objects[11][1]: objects[11][0].process([upBar, 'invert'], events)  # Invert
    if objects[12][1] and objects[12][2]: objects[12][0].process([filters], events)  # Invert Radio
    if objects[13][1]: objects[13][0].process([upBar, 'dual'], events)  # Dual Channel
    if objects[14][1] and objects[14][2]: objects[14][0].process([filters], events)  # Dual Channel Radio
    if objects[15][1]: objects[15][0].process([upBar, 'edge'], events)  # Edge Enhance
    if objects[16][1] and objects[16][2]: objects[16][0].process([filters], events)  # Edge Enhance Radio
    if objects[17][1]: objects[17][0].process([upBar, 'emboss'], events)  # Emboss Channel
    if objects[18][1] and objects[18][2]: objects[18][0].process([filters], events)  # Emboss Radio
    if objects[19][1]: objects[19][0].process([upBar, 'contour'], events)  # Contour
    if objects[20][1] and objects[20][2]: objects[20][0].process([filters], events)  # Contour Radio
    if objects[21][1]: objects[21][0].process([file], events)  # Export

    # for object in objects[6:]:  # 'Filters', 'Export', etc Buttons
    #     object[0].process([], events)

    if file:
        file.process(filters)

    upBar.process(filters, events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Render
    w_screen, h_screen = screen.get_size()
    screen.fill('#F5F5F5') #191919 #E6E6E6
    pygame.draw.rect(screen, '#FFFFFF', pygame.Rect(0, 0, 150, h_screen))
    pygame.draw.line(screen, '#E6E6E6', (150, 0), (150, h_screen), width=1)
    if file:
        w_file, h_file = file.image.get_size()
        w_file = int((w_screen-w_file+150)/2)
        h_file = int((h_screen-h_file)/2)
        screen.blit(file.previewImage, (w_file, h_file))

    for object in objects[2:8]:  # adjustment
        object[1] = adjustmentIsExpanded
    for object in objects[9:21]:  # filters
        object[1] = filterIsExpanded

    i = -1
    for object in objects:
        if object[1]:
            if object[2]:
                object[0].setPos(117, i * 30 + 3)
            else:
                i = i + 1
                object[0].setPos(1, i * 30 + 1)
    i = 1
    for object in objects:
        if object[1]:
            object[0].render(screen)
            if not object[2]:
                pygame.draw.line(screen, '#E6E6E6', (0, i*30), (150, i*30), width=1)
                i = i+1

    upBar.render(screen)

    pygame.display.flip()
