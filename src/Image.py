import pygame
import math
import numpy as np
import copy
from PIL import Image as Img
from PIL import ImageEnhance, ImageFilter


class Image:
    def __init__(self, filename, image):
        self.filename = filename
        self.image = image
        self.originalImage = image
        self.previewImage = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.filters = {
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

        F_domain = []
        image_array = pygame.surfarray.array3d(self.image)
        for i in range(3):
            F_shift = np.fft.fftshift(np.fft.fft2(image_array[:, :, i]))
            F_domain.append(F_shift)
        image_spectrum = np.dstack([F_domain[0].astype('complex_'), F_domain[1].astype('complex_'), F_domain[2].astype('complex_')])
        self.originalSpectrum = image_spectrum
        self.previewSpectrum = image_spectrum
        # self.spectrumSurf = pygame.surfarray.make_surface(image_spectrum)

    # def setFilters(self, filter, isActive):
    #     self.filters[filter] = isActive

    def updateImage(self):
        image_list = []
        image_spectrum = self.previewSpectrum
        for i in range(3):
            image_layer = abs(np.fft.ifft2(np.fft.ifftshift(image_spectrum[:, :, i])))
            image_list.append(image_layer)
        image_array = np.dstack([image_list[0].astype(int), image_list[1].astype(int), image_list[2].astype(int)])
        self.previewImage = pygame.surfarray.make_surface(image_array)

    def updateSpectrum(self):
        F_domain = []
        image_array = pygame.surfarray.array3d(self.image).swapaxes(0, 1)
        for i in range(3):
            F_shift = np.fft.fftshift(np.fft.fft2(image_array[:, :, i]))
            F_domain.append(F_shift)
        image_spectrum = np.dstack([F_domain[0].astype(int), F_domain[1].astype(int), F_domain[2].astype(int)])
        self.previewSpectrum = image_spectrum

    # def updateSpectrumSurf(self):
    #     self.spectrumSurf = pygame.surfarray.make_surface(self.spectrum)

    def filterImage(self):
        self.previewSpectrum = self.originalSpectrum

        # Frequency Domain
        if self.filters['blur'][0]:
            self.blur(self.filters['blur'][1])

        self.updateImage()
        if self.filters['brighten'][0]:
            self.brighten(self.filters['brighten'][1])
        if self.filters['contrast'][0]:
            self.contrast(self.filters['contrast'][1])
        if self.filters['sharp'][0]:
            self.sharp(self.filters['sharp'][1])
        if self.filters['invert'][0]:
            self.invert()
        if self.filters['dual'][0]:
            self.dual(self.filters['dual'][1])
        if self.filters['edge'][0]:
            self.edge()
        if self.filters['emboss'][0]:
            self.emboss()
        if self.filters['contour'][0]:
            self.contour()

    def process(self, filters):
        # print(self.filters, filters)
        for filter in self.filters:
            if self.filters[filter] != filters[filter]:
                # self.filters[filter][0] = filters[filter][0]
                self.filters = copy.deepcopy(filters)
                # print(self.filters is filters)
                self.filterImage()
                # break

    def brighten(self, amount=10):
        print("Executed Brighten")
        image_array = pygame.surfarray.array3d(self.previewImage)
        image_array = image_array * (1.0 + (amount / 20 * 0.8))
        if amount > 0:
            image_array[image_array > 255] = 255
        elif amount < 0:
            image_array[image_array < 0] = 0
        self.previewImage = pygame.surfarray.make_surface(image_array)

    def contrast(self, amount=10):
        print("Executed Contrast")
        image_array = pygame.surfarray.array3d(self.previewImage)
        image = Img.fromarray(image_array)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1 + (amount / 20))

        # for i in range(3):
        #     currLayer = image_array[i]
        #     minVal = np.min(currLayer)
        #     maxVal = np.max(currLayer)
        #     print(minVal, maxVal)
        #     image_array[i] = 255 * (currLayer - minVal) / (maxVal - minVal)
        # image_array = image_array - 25
        # image_array = ImageOps.equalize(image_array)
        self.previewImage = pygame.surfarray.make_surface(np.array(image))

    def sharp(self, amount=10):
        image_array = pygame.surfarray.array3d(self.previewImage)
        image = Img.fromarray(image_array)
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1 + (amount / 20))
        self.previewImage = pygame.surfarray.make_surface(np.array(image))

    def blur(self, D0=10):
        print("Executed Blur")
        F_domain = []
        M_shape, N_shape, L_shape = self.previewSpectrum.shape
        # print(M_shape, N_shape)
        # D0 = 10
        for i in range(3):
            H = np.zeros((M_shape, N_shape), dtype=np.float32)
            F_shift = self.previewSpectrum[:, :, i]
            for u in range(M_shape):
                for v in range(N_shape):
                    D = np.sqrt((u - M_shape / 2) ** 2 + (v - N_shape / 2) ** 2)
                    H[u, v] = math.e ** (-1 * D ** 2 / (2 * D0 ** 2))  # Gaussian Low Pass
            G_shift = F_shift * H
            # G = abs(np.fft.ifft2(G_shift))
            # F_domain.append(G)
            F_domain.append(G_shift)
        self.previewSpectrum = np.dstack([F_domain[0].astype('complex_'), F_domain[1].astype('complex_'), F_domain[2].astype('complex_')])
        # final_image = np.dstack([F_domain[0].astype('complex_'), F_domain[1].astype('complex_'), F_domain[2].astype('complex_')])
        # self.image = pygame.surfarray.make_surface(final_image)
        # self.updateImage()
        # self.updateSpectrumSurf()

    def invert(self):
        print("Executed Invert")
        image_array = pygame.surfarray.array3d(self.previewImage)
        H = np.full(image_array.shape, 255)
        image_array = H - image_array
        self.previewImage = pygame.surfarray.make_surface(image_array)

    def dual(self, layer):
        image_array = pygame.surfarray.array3d(self.previewImage)
        if layer == 1:  # Red Channel
            image_array[:, :, 1] = 0
            image_array[:, :, 2] = 0
        elif layer == 2:  # Green Channel
            image_array[:, :, 0] = 0
            image_array[:, :, 2] = 0
        elif layer == 3:  # Blue Channel
            image_array[:, :, 0] = 0
            image_array[:, :, 1] = 0
        self.previewImage = pygame.surfarray.make_surface(image_array)

    def edge(self):
        image_array = pygame.surfarray.array3d(self.previewImage)
        image = Img.fromarray(image_array)
        image = image.filter(ImageFilter.EDGE_ENHANCE)
        self.previewImage = pygame.surfarray.make_surface(np.array(image))

    def emboss(self):
        image_array = pygame.surfarray.array3d(self.previewImage)
        image = Img.fromarray(image_array)
        image = image.filter(ImageFilter.EMBOSS)
        self.previewImage = pygame.surfarray.make_surface(np.array(image))

    def contour(self):
        image_array = pygame.surfarray.array3d(self.previewImage)
        image = Img.fromarray(image_array)
        image = image.filter(ImageFilter.CONTOUR)
        self.previewImage = pygame.surfarray.make_surface(np.array(image))