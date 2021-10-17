from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


class GUI(Frame):
    img = None
    img_is_found = False

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.file = Button(self, width=30, text='Cari gambar disini', command=self.choose)
        self.label = Label(image=None, width=900, height=600)

        self.low_contrast = Button(self, width=30, text='Kontras Rendah', command=self.lowContrast)
        self.negative_trans = Button(self, width=30, text='Transformasi negatif', command=self.negativeTrans)

        self.pack()
        self.label.pack()
        self.file.pack()
        self.low_contrast.pack()
        self.negative_trans.pack()

    def choose(self):
        ifile = filedialog.askopenfile(parent=self, mode='rb', title='Choose a file')
        if ifile:
            path = Image.open(ifile)
            self.image2 = ImageTk.PhotoImage(path)
            self.label.configure(image=self.image2)
            self.label.image = self.image2
            self.img = np.array(path)
            self.img = self.img[:, :, ::-1].copy()
            self.img_is_found = True

    def lowContrast(self):
        if self.img_is_found:
            img_after = change_contrast(self.img, 0.5, 10)
            img_after = ImageTk.PhotoImage(Image.fromarray(img_after))
            self.label.configure(image=img_after)
            self.label.image = img_after

    
    
    
    def negativeTrans(self):
        if self.img_is_found:
            img_after = negative_transformation(self.img)
            img_after = ImageTk.PhotoImage(Image.fromarray(img_after))
            self.label.configure(image=img_after)
            self.label.image = img_after


def change_contrast(img, alpha, beta):
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(img.shape[2]):
                img[y, x, c] = np.clip(alpha *img[y, x, c] + beta, 0, 255)
    return img


def negative_transformation(img):
    height, widht, _ = img.shape

    for i in range(0, height - 1):
        for j in range(0, widht - 1):
            pixel = img[i, j]

            pixel[0] = 255 - pixel[0]
            pixel[1] = 255 - pixel[1]
            pixel[2] = 255 - pixel[2]

            img[i, j] = pixel
    return img
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

# root.attributes('-fullscreen', True)
gui = GUI(root)
gui.mainloop()
