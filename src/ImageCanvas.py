import tkinter as tk
import PIL.Image
import PIL.ImageTk
import numpy as np

from custom_log import print_log
import Constants as CONST
import Custom_Utils as CustUtil


class ImageCanvas(tk.Canvas):
    def __init__(self, parent, app_state, text, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.app_state = app_state
        self.parent = parent
        self.text = text
        self.redraw()

    # Not finished.
    def assess_photo(self):
        width, height = self.winfo_width(), self.winfo_height()
        self.display_np = CustUtil.rescale(
            self.app_state[CONST.ARR][self.text], (height, width)
        )
        g = PIL.Image.fromarray(self.display_np)
        self.app_state[CONST.PHOTO][self.text] = PIL.ImageTk.PhotoImage(image=g)
        return self.app_state[CONST.PHOTO][self.text]

    def redraw(self):
        self.delete("all")
        self.create_image(
            self.winfo_width() // 2,
            self.winfo_height() // 2,
            image=self.assess_photo(),
            anchor=tk.CENTER,
        )
        self.create_text(
            self.winfo_width() // 2, 20, font="Tahoma 20", text=self.text, fill="black"
        )

    def resize(self, width, height):
        self.configure(width=width, height=height)
        self.redraw()
