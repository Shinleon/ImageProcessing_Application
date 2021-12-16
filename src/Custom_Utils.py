import cv2

from custom_log import print_log


def rescale(photo, goal_geom):
    ph_w, ph_h, _ = photo.shape
    win_w, win_h = goal_geom
    scale_factor = min(win_w / ph_w, win_h / ph_h)
    return cv2.resize(
        photo, (int(max(ph_h * scale_factor, 3)), int(max(ph_w * scale_factor, 3)))
    )
