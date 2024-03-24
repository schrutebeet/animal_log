from pathlib import Path
from typing import Union, Tuple
from abc import ABC, abstractmethod

import customtkinter as ctk
from PIL import Image, ImageTk

class BaseFrame(ABC):

    def __init__(self, window) -> None:
        self.window = window
        self.window.geometry('1000x660') # Set default window size
        self.window.title("Myapp") # Name window tab
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

    @abstractmethod
    def initialize_ui(self):
        pass

    @staticmethod
    def get_image(image_folder: Union[str, Path], img_name: str, new_shape: Tuple = None) -> ctk.CTkImage:
        if isinstance(image_folder, str):
            image_folder = Path(image_folder)
        open_image = Image.open(image_folder / Path(img_name + ".png"))
        if new_shape:
            open_image = open_image.resize(new_shape)
        ctk_image = ctk.CTkImage(open_image)
        return ctk_image
