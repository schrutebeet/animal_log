from pathlib import Path
import customtkinter as ctk

from config.config import Config
from animal_logger.opt.img import add_animal
from animal_logger.src.frames.baseframe import BaseFrame


class AddAnimal(BaseFrame):

    def __init__(self, window, main_frame: ctk.CTkFrame) -> None:
        super().__init__(window)
        self.main_frame = main_frame
        self.image_pool = Path(add_animal.__file__).parent

    def initialize_ui(self) -> None:
        self.choose_class_of_animal()

    def choose_class_of_animal(self):
        animal_classes = Config.get_info()['animal_classes']
        animal_class_colors = ['#EFBC9B', '#FFE4CF', '#FFEDD8', '#F1F5A8', '#78A083', '#B7C9F2']
        for animal_class, color in zip(animal_classes, animal_class_colors):
            button = ctk.CTkButton(self.main_frame,
                                   text = animal_class.capitalize(),
                                   image = self.get_image(self.image_pool, animal_class),
                                   fg_color = color,
                                   bg_color = color,
                                   hover_color = color,
                                   text_color = 'white',
                                   command = getattr(self, 'set_' + animal_class + '_button'))
            button.pack(fill = 'x', padx = 20, pady = 10)
            setattr(self, animal_class, button)

    def set_mammal_button(self):
        pass

    def set_invertebrate_button(self):
        pass

    def set_fish_button(self):
        pass

    def set_amphibian_button(self):
        pass

    def set_reptile_button(self):
        pass

    def set_bird_button(self):
        pass
