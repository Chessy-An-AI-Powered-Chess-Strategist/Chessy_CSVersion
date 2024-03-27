import pygame as p
"""
Set Up Settings for the GUI
"""

gui_settings = {
    "WIDTH": 512,
    "HEIGHT": 512,
    "DIMENSION": 8,
    "SQ_SIZE": 64,
    "MAX_FPS": 15,
    "IMAGES": {}
}


def load_images():
    """
    Initialize a global dictionary of the images
    """
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for i in range(len(pieces)):
        index = "0" + str(i + 1) if i < 9 else str(i + 1)
        image = p.image.load("images/64_" + index + ".png")
        size = (gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"])
        gui_settings["IMAGES"][pieces[i]] = p.transform.scale(image, size)



load_images()

