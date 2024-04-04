"""
Set Up Settings for the GUI
"""

import pygame as p


gui_settings = {
    "WIDTH": 512,
    "HEIGHT": 512,
    "DIMENSION": 8,
    "SQ_SIZE": 64,
    "MAX_FPS": 15,
    "IMAGES": {},
    "SOUNDS": {}
}


def load_images() -> None:
    """
    A function that initializes a global dictionary of the images
    """
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for i in range(len(pieces)):
        index = "0" + str(i + 1) if i < 9 else str(i + 1)
        image = p.image.load("Game/images/64_" + index + ".png")
        size = (gui_settings["SQ_SIZE"] - 2, gui_settings["SQ_SIZE"] - 2)
        gui_settings["IMAGES"][pieces[i]] = p.transform.scale(image, size)


def load_sounds() -> None:
    """
    A function that loads in the sounds
    """
    p.mixer.init()
    """
    A function that initializes a global dictionary of the sounds
    """
    sounds = ["move", "capture", "check", "castle", "game_end", "game_start"]
    for sound in sounds:
        sound_file = p.mixer.Sound("Game/sounds/" + sound + ".mp3")
        gui_settings["SOUNDS"][sound] = sound_file


load_images()
load_sounds()

if __name__ == '__main__':

    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
