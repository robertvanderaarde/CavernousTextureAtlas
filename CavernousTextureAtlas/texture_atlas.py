import numpy as np
from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt
from files import Files

class TextureAtlas:
    atlas = None

    # rows = Number of rows
    # columns = Number of columns
    # texture_size = final size of the texture
    # texture_padding = how many pixels to pad each texture
    def __init__(self, rows, columns, texture_size, texture_padding):
        self.rows = rows
        self.columns = columns
        self.texture_size = texture_size
        self.texture_padding = texture_padding
        self.path = "."

    def set_path(self, path):
        self.path = path

    def create(self):
        self.atlas = np.zeros((self.rows * (self.texture_size + (2 * self.texture_padding)),
                               self.columns * (self.texture_size + (2 * self.texture_padding)),
                               3), dtype=np.uint8)

        f = Files(self.path)
        filenames = f.get_numeric_files()

        # ID: numpy image
        images = {}
        for file in filenames:
            if file == "":
                continue

            key = int(file.split(".")[0])
            images[key] = np.array(Image.open(self.path + file))

        for id in images:
            row, column = self.get_row_column(id)
            img = self.prepare(images[id])

            row_pos = self.row_to_pos(row)
            col_pos = self.col_to_pos(column)

            self.atlas[row_pos:row_pos + img.shape[0], col_pos:col_pos + img.shape[1], 0:3] = img[:, :, 0:3]
        self.atten_atlas = self.create_atten_atlas()

    def create_atten_atlas(self):
        img = Image.fromarray(self.atlas, mode='RGB').convert('LA')
        img = img.filter(ImageFilter.BoxBlur(radius=int(self.texture_size / 25)))
        return np.array(img)

    def save(self, filename):
        Image.fromarray(self.atlas).save(filename)

    def save_atten(self, filename):
        Image.fromarray(self.atten_atlas).save(filename)

    def col_to_pos(self, col):
        return self.row_to_pos(col)

    def row_to_pos(self, row):
        return int(row * (self.texture_size + (self.texture_padding * 2)))

    def get_row_column(self, id):
        row = int(id / self.columns)
        col = int(id % self.columns)
        return row, col

    def empty_image(self):
        return np.zeros((self.texture_size, self.texture_size))

    def prepare(self, img):
        img = self.resize(img, (self.texture_size, self.texture_size))
        img = self.pad(img)
        return img

    def resize(self, img_arr, shape):
        img = Image.fromarray(img_arr)
        img = img.resize(shape)
        return np.array(img)

    def pad(self, img_arr):
        new_image = np.zeros(((self.texture_padding * 2) + img_arr.shape[0],
                              (self.texture_padding * 2) + img_arr.shape[1], img_arr.shape[2]),
                             dtype=np.uint8)
        new_image[self.texture_padding:img_arr.shape[0] + self.texture_padding,
                  self.texture_padding:img_arr.shape[1] + self.texture_padding, :] = img_arr[:, :, :]

        # Top Row
        new_image[0:self.texture_padding, self.texture_padding:img_arr.shape[1] + self.texture_padding, :]\
            = img_arr[0, :, :]

        # Bottom Row
        new_image[self.texture_padding + img_arr.shape[0]:, self.texture_padding:img_arr.shape[1] + self.texture_padding, :]\
            = img_arr[-1, :, :]

        # Left side
        new_image[self.texture_padding:img_arr.shape[0] + self.texture_padding, 0:self.texture_padding, :]\
            = img_arr[:, 0:1, :]

        # Right side
        new_image[self.texture_padding:img_arr.shape[0] + self.texture_padding, img_arr.shape[1] + self.texture_padding:, :]\
            = img_arr[:, -2:-1, :]

        # Top Left
        new_image[0:self.texture_padding, 0:self.texture_padding, :] = img_arr[0, 0, :]

        # Top Right
        new_image[0:self.texture_padding, self.texture_padding + img_arr.shape[1]:, :] = img_arr[0, -1, :]

        # Bottom Right
        new_image[self.texture_padding + img_arr.shape[0]:, self.texture_padding + img_arr.shape[1]:, :] = img_arr[-1, -1, :]

        # Bottom Left
        new_image[self.texture_padding + img_arr.shape[0]:, 0:self.texture_padding, :] = img_arr[-1, 0, :]

        return new_image

    def show(self):
        Image._show(Image.fromarray(self.atlas))
