import os

import tkinter as tk
import tkinter.filedialog
import PIL

from custom_log import print_log
import Constants as CONST
import App

def make_blurScale(parent, ancestor):
    return [
        tk.Scale(
            parent,
            from_=1,
            to=50,
            foreground="Black",
            orient=tk.HORIZONTAL,
            showvalue=1,
            command=ancestor.blur_image,
            length=400,
            sliderlength=20,
            label=CONST.GAUSS_BLR,
            font="Tahoma 16",
        )
    ]


def make_whiteliftScale(parent, ancestor):
    return [
        tk.Scale(
            parent,
            from_=-255,
            to=255,
            foreground="Black",
            orient=tk.HORIZONTAL,
            showvalue=1,
            command=ancestor.white_lift,
            length=400,
            sliderlength=20,
            label=CONST.WHITE_LIFT,
            font="Tahoma 16",
        )
    ]


def make_sobelScale(parent, ancestor):
    return [
        tk.Scale(
            parent,
            from_=3,
            to=15,
            resolution=2,
            foreground="Black",
            orient=tk.HORIZONTAL,
            showvalue=1,
            command=ancestor.sobel_filter,
            length=400,
            sliderlength=20,
            label=CONST.SOBEL,
            font="Tahoma 16",
        )
    ]


def make_highBoostScale(parent, ancestor):
    return [
        tk.Scale(
            parent,
            from_=3,
            to=15,
            resolution=2,
            foreground="Black",
            orient=tk.HORIZONTAL,
            showvalue=1,
            command=ancestor.high_boost,
            length=400,
            sliderlength=20,
            label=CONST.HIGH_BOOST,
            font="Tahoma 16",
        )
    ]


def make_hueSpinScale(parent, ancestor):
    return [
        tk.Scale(
            parent,
            from_=0,
            to=255,
            resolution=1,
            foreground="Black",
            orient=tk.HORIZONTAL,
            showvalue=1,
            command=ancestor.hue_spin,
            length=400,
            sliderlength=20,
            label=CONST.HUE_SPIN,
            font="Tahoma 16",
        )
    ]


function_mapping = {
    CONST.GAUSS_BLR: make_blurScale,
    CONST.WHITE_LIFT: make_whiteliftScale,
    CONST.SOBEL: make_sobelScale,
    CONST.HIGH_BOOST: make_highBoostScale,
    CONST.HUE_SPIN: make_hueSpinScale,
}


class ImageSettings(tk.Frame):
    def __init__(self, parent, app_state, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.app_state = app_state
        self.parent = parent
        self.scales = function_mapping[self.app_state[CONST.PROCESS]](self, parent)
        self.resize(width=self.winfo_width(), height=self.winfo_height())

        self.effectDropDownSel = tk.StringVar(self)
        self.effectDropDownSel.set(self.app_state[CONST.PROCESS])
        self.effectDropDownSel.trace("w", self.effectDropDownSelCallback)
        self.effectDropDown = tk.OptionMenu(
            self,
            self.effectDropDownSel,
            *function_mapping.keys(),
        )
        self.effectDropDown.config(fg="black", bg="green")
        self.effectDropDown.place(relx=0.05, rely=0.25, relwidth=0.2)

        def save_image():
            file = tk.filedialog.asksaveasfile(
                mode="w", defaultextension=".jpg", initialfile="image.jpg"
            )
            image = self.app_state[CONST.ARR][CONST.ORIGINAL_IMG]
            pil_image = PIL.Image.fromarray(image)
            pil_image.save(file)

        self.save_button = tk.Button(
            self, text="save image", bg="purple", fg="blue", command=save_image
        )
        
        self.save_button.place(relx=0.8, rely=0.1, relwidth=0.1)

        self.count = 0
        button_text = ["change to candle", "change to star", "change to lena"]
        def select_image():
            filepaths = [App.resource_path("./img/lena.bmp"), App.resource_path("./img/candle.png"), App.resource_path("./img/star.jpg")]
            print_log(f"filepath:{filepaths[self.count]}")
            parent.reset(img=filepaths[self.count])
            self.change_image['text'] = button_text[self.count]
            self.count  = (self.count + 1)%len(filepaths)

        self.change_image = tk.Button(
            self, text=button_text[-1], bg="purple", fg="blue", command=select_image
        )
        self.change_image.place(relx=0.8, rely=0.4, relwidth=0.1)

        def change_to_custom_image():
            file_url = tk.filedialog.askopenfilename(
                initialdir=os.path.expanduser("~"),
                title="Please select image file",
                filetypes=(("image files", ("*.jpg", "*.png")),
                           ("all files", "*.*"))
            )
            if os.path.isfile(file_url):
                print_log(f"file_url to load:{file_url}")
                parent.reset(img=file_url)

        self.custom_image = tk.Button(
            self, text="change to custom image", bg="purple", fg="blue", command=change_to_custom_image
        )
        self.custom_image.place(relx=0.8, rely=0.7, relwidth=0.2)

    def effectDropDownSelCallback(self, *args):
        effect_str = self.effectDropDownSel.get()
        if effect_str in function_mapping.keys():
            self.app_state[CONST.PROCESS] = effect_str
            print_log(f"current effect {self.app_state[CONST.PROCESS]}")
            self.scales = function_mapping[self.app_state[CONST.PROCESS]](
                self, self.parent
            )
        self.resize(width=self.winfo_width(), height=self.winfo_height())
        self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = self.app_state[CONST.ARR][
            CONST.ORIGINAL_IMG
        ]
        self.parent.rerender()

    def resize(self, width, height):
        self.configure(width=width, height=height)
        self.padding = 0.05
        self.width = 0.5 / len(self.scales) - self.padding / 2
        for idx, scale in enumerate(self.scales):
            scale.place(
                relx=0.25 + idx * (self.width + self.padding),
                rely=0.1,
                relwidth=self.width,
                relheight=0.5,
            )
        print_log(f"resizing Image Settings Frame")
        return self.winfo_width(), self.winfo_height()

    def getScales(self):
        ret = []
        for scale in self.scales:
            ret.append(scale.get())
        return ret

    def reset_scales(self):
        for scale in self.scales:
            scale.set(0)
