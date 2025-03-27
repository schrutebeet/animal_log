import math
from pathlib import Path
import customtkinter as ctk

from config.config import Config
from animal_logger.opt.img import add_animal
from animal_logger.src.frames.baseframe import BaseFrame


class AddAnimal(BaseFrame):
    
    _is_ui_initialized = False

    def __init__(self, window, main_frame: ctk.CTkFrame) -> None:
        super().__init__(window)
        self.main_frame = main_frame
        self.main_frame.pack(expand=True)  
        self.image_pool = Path(add_animal.__file__).parent

    def initialize_ui(self) -> None:
        if not self._is_ui_initialized:
            self.choose_class_of_animal()

    def choose_class_of_animal(self):
        animal_classes = Config.get_info()['animal_classes']
        len_animal_classes = len(animal_classes)
        animal_class_colors = ['#EFBC9B', '#FFE4CF', '#FFEDD8', '#F1F5A8', '#78A083', '#B7C9F2']
        num_cols = 3
        num_rows = math.ceil(len_animal_classes / num_cols)
        col_list = [col for col in range(num_cols)] * num_rows
        row_list = [row for row in range(num_rows) for _ in range(num_cols)]
        for animal_class, color, col, row in zip(animal_classes, animal_class_colors, col_list, row_list):
            button = ctk.CTkButton(self.main_frame,
                                   text = animal_class.capitalize(),
                                   image = self.get_image(self.image_pool, animal_class),
                                   fg_color = color,
                                   bg_color = color,
                                   hover_color = color,
                                   text_color = 'white',
                                   command = getattr(self, 'set_' + animal_class + '_button',),
                                   height = 100,
                                   width = 100)
            button.grid(row = row, column = col, padx = 5, pady = 5, sticky = 'nsew', in_ = self.main_frame)
            setattr(self, animal_class, button)
        AddAnimal._is_ui_initialized = True

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
