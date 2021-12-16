import sys
import os

import tkinter as tk
import cv2
import numpy as np

import HistoryFrame
import ImageCanvas
import ImageSettings
from custom_log import print_log
import Constants as CONST

# <a href='https://www.freepik.com/vectors/background'>Background vector created by vectorpocket - www.freepik.com</a>


# https://stackoverflow.com/questions/51264169/pyinstaller-add-folder-with-images-in-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainApplication(tk.Frame):
    def blur_image(self, _):
        # get value from the corresponding scale from the settings_frame
        k = self.settings_frame.getScales()
        self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = cv2.blur(
            self.app_state[CONST.ARR][CONST.ORIGINAL_IMG], (k[0], k[0])
        )
        self.modified_canvas.redraw()

    def white_lift(self, _):
        k = self.settings_frame.getScales()
        self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = (
            np.clip(
                self.app_state[CONST.ARR][CONST.ORIGINAL_IMG].astype(np.int16) + k[0],
                0,
                255,
            )
        ).astype(np.uint8)
        self.modified_canvas.redraw()

    def sobel_filter(self, _):
        k = self.settings_frame.getScales()
        self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = cv2.Sobel(
            self.app_state[CONST.ARR][CONST.ORIGINAL_IMG],
            cv2.CV_32F,
            dx=1,
            dy=1,
            ksize=k[0],
        )
        self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = self.app_state[CONST.ARR][
            CONST.MODIFIED_IMG
        ].astype(np.uint8)
        self.modified_canvas.redraw()

    def high_boost(self, _):
        k = self.settings_frame.getScales()
        temp = self.app_state[CONST.ARR][CONST.ORIGINAL_IMG].astype(
            np.float32
        ) + cv2.Sobel(
            self.app_state[CONST.ARR][CONST.ORIGINAL_IMG],
            cv2.CV_32F,
            dx=1,
            dy=1,
            ksize=k[0],
        )
        self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = temp.astype(np.uint8)
        self.modified_canvas.redraw()

    def hue_spin(self, _):
        k = self.settings_frame.getScales()
        temp = cv2.cvtColor(
            self.app_state[CONST.ARR][CONST.ORIGINAL_IMG], cv2.COLOR_RGB2HSV
        )
        temp[:, :, 0] = temp[:, :, 0] + k
        self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = cv2.cvtColor(
            temp, cv2.COLOR_HSV2RGB
        )
        self.modified_canvas.redraw()

    def __init__(self, parent, app_state, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.app_state = app_state

        # get the image using cv2
        if not os.path.exists(self.app_state[CONST.IMAGE_PATH]):
            self.app_state[CONST.ORIGINAL_IMG] = np.ones((200, 200, 3))
        else:
            self.app_state[CONST.ORIGINAL_IMG] = cv2.cvtColor(
                cv2.imread(self.app_state[CONST.IMAGE_PATH]), cv2.COLOR_BGR2RGB
            )
        # self.NEWcv_img = self.cv_img.copy()  # for recursive processing
        self.app_state[CONST.ARR][CONST.ORIGINAL_IMG] = self.app_state[
            CONST.ORIGINAL_IMG
        ].copy()
        self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = self.app_state[
            CONST.ORIGINAL_IMG
        ].copy()

        # ascertain and define the window size
        print_log(parent.geometry())
        self.width, self.height = parent.winfo_width(), parent.winfo_height()
        print_log(f"window geometry: {self.width}x{self.height}")

        settings_w, settings_h = self.width, max(self.height // 6, 120)
        self.settings_frame = ImageSettings.ImageSettings(
            self,
            self.app_state,
            width=settings_w,
            height=settings_h,
            bg="grey",
        )
        self.settings_frame.pack(side=tk.TOP, fill=tk.X)

        # make the history frame
        h_frame_w, h_frame_h = (
            max(20, self.winfo_width() // 4),
            self.height - settings_h,
        )
        print_log(f"history_frame geometry: {h_frame_w}x{h_frame_h}")
        self.history_frame = HistoryFrame.HistoryFrame(
            self,
            app_state,
            width=h_frame_w,
            height=h_frame_h,
            bg="blue",
        )
        self.history_frame.pack(side=tk.LEFT, fill=tk.Y)

        ## start on the drawing panels
        oc_w, oc_h = (self.width - h_frame_w) // 2, self.height - settings_h
        print_log(f"original geometry: {oc_w}x{oc_h}")
        self.original_canvas = ImageCanvas.ImageCanvas(
            self,
            self.app_state,
            CONST.ORIGINAL_IMG,
            width=oc_w,
            height=oc_h,
            bg="yellow",
        )  # make the canvas
        self.original_canvas.pack(side=tk.LEFT)

        # next drawing panel
        mc_w, mc_h = (self.width - h_frame_w) // 2, self.height - settings_h
        print_log(f"modified geometry: {mc_w}x{mc_h}")
        self.modified_canvas = ImageCanvas.ImageCanvas(
            self,
            self.app_state,
            CONST.MODIFIED_IMG,
            width=mc_w,
            height=mc_h,
            bg="orange",
        )
        self.modified_canvas.pack(side=tk.LEFT)

        # define the bottom bar which will have the adjustable settings

    def rerender(self, width=200, height=200):
        self.width, self.height = width, height

        settings_w, settings_h = self.width, max(self.height // 6, 80)
        self.settings_frame.resize(width=settings_w, height=settings_h)

        # change to resize
        h_frame_w, h_frame_h = min(150, self.width // 3), self.height
        self.history_frame.configure(width=h_frame_w, height=h_frame_h)

        oc_w, oc_h = (self.width - h_frame_w) // 2, self.height - settings_h
        self.original_canvas.resize(width=oc_w, height=oc_h)

        mc_w, mc_h = (self.width - h_frame_w) // 2, self.height - settings_h
        self.modified_canvas.resize(width=mc_w, height=mc_h)

    def add_to_history(self):
        self.app_state[CONST.ARR][CONST.ORIGINAL_IMG] = self.app_state[CONST.ARR][
            CONST.MODIFIED_IMG
        ]
        to_append = (
            self.app_state[CONST.PROCESS],
            self.settings_frame.getScales(),
            self.app_state[CONST.ARR][CONST.ORIGINAL_IMG],
        )
        print_log(f"appending {to_append}")
        self.app_state[CONST.HISTORY].append(to_append)
        self.history_frame.add_history(to_append)
        self.settings_frame.reset_scales()
        self.modified_canvas.redraw()
        self.original_canvas.redraw()
        # rerender history frame

    def reset(
        self,
        img=resource_path("./img/lena.bmp"),
    ):
        self.app_state[CONST.IMAGE_PATH] = img
        self.app_state[CONST.ORIGINAL_IMG] = self.app_state[
            CONST.ORIGINAL_IMG
        ] = cv2.cvtColor(
            cv2.imread(self.app_state[CONST.IMAGE_PATH]), cv2.COLOR_BGR2RGB
        )
        self.app_state[CONST.ARR] = {
            CONST.ORIGINAL_IMG: self.app_state[CONST.ORIGINAL_IMG],
            CONST.MODIFIED_IMG: self.app_state[CONST.ORIGINAL_IMG],
        }
        self.rerender()


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(width=300, height=300)
    root.title("Leonard Shin's image processing application")
    root.geometry("1200x700")
    state = {
        CONST.IMAGE_PATH: "./img/candle.png",
        CONST.HISTORY: list(),
        CONST.ORIGINAL_IMG: None,  # holds the actual original image
        CONST.PHOTO: dict(),  # hold tk.photo version of current images
        CONST.ARR: dict(),  # hold np version of current images
        CONST.PROCESS: CONST.WHITE_LIFT,
    }
    application = MainApplication(root, state)
    application.pack(side="top", fill="both", expand=True)

    def handle_configure(event):
        text = f"window geometry: {root.geometry()}"
        print_log(text)
        application.rerender(width=root.winfo_width(), height=root.winfo_height())

    root.bind("<Configure>", handle_configure)
    root.mainloop()
