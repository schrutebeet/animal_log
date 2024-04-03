from pathlib import Path

import customtkinter as ctk

from animal_logger.opt.img import menu
from animal_logger.src.frames.baseframe import BaseFrame
from animal_logger.src.frames.add_animal import AddAnimal


class Dashboard(BaseFrame):

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.icon_size = (18, 18)
        self.sidebar_width = 0.05
        self.header_height = 0.1
        self.header_color = '#627254'
        self.sidebar_color = '#DDDDDD'
        self.main_background = '#EEEEEE'
        self.header = None
        self.sidebar = None
        self.main_frame = None
        self.search_bar = None
        self.main_frame = None
        self.image_pool = Path(menu.__file__).parent

    def initialize_ui(self):
        self.configure_grid_layout()
        self.create_header_frame()
        self.create_sidebar_frame()
        self.create_main_content_frame()
        self.add_company_logo()
        self.add_searchbar()
        self.add_account_settings()
        self.add_buttons_to_sidebar()
        self.window.mainloop()

    def configure_grid_layout(self) -> None:
        # Sidebar
        self.window.columnconfigure(0, weight=int(self.sidebar_width * 100))
        # Rest of the content
        self.window.columnconfigure(1, weight=int((1 - self.sidebar_width) * 100))
        # Header
        self.window.rowconfigure(0, weight=int((self.header_height) * 100))
        # Rest of the content
        self.window.rowconfigure(1, weight=int((1 - self.header_height) * 100))

    def create_header_frame(self):
        self.header = ctk.CTkFrame(self.window, fg_color = self.header_color, bg_color = self.header_color)
        self.header.grid(row = 0, column = 0, columnspan = 2, sticky='nsew')

    def create_sidebar_frame(self):
        self.sidebar = ctk.CTkFrame(self.window, fg_color = self.sidebar_color, bg_color = self.sidebar_color)
        self.sidebar.grid(row = 1, column = 0, sticky = 'nsew')

    def create_main_content_frame(self):
        self.main_frame = ctk.CTkFrame(self.window, fg_color = self.main_background)
        self.main_frame.grid(row = 1, column = 1, sticky = "nsew")

    def add_company_logo(self):
        logo = ctk.CTkLabel(self.header, 
                            text = '', 
                            image = self.get_image(self.image_pool, 'logo_no_bg'))
        logo.pack(side = 'left', padx = 10)

    def add_searchbar(self):
        self.search_bar = ctk.CTkEntry(self.header)
        self.search_bar.pack(side = 'left', fill = 'x', expand = True, padx = 100)

    def add_account_settings(self):
        account_settings = ctk.CTkLabel(self.header, text="Account Settings", fg_color='#1f2f40', text_color = 'white')
        account_settings.pack(side='right', padx=10)

    def add_buttons_to_sidebar(self):
        button_names = ["Home", "Recent", "Create record", "View record"]
        icon_names = ["home", "recent", "edit", "view"]
        icons = [self.get_image(self.image_pool, icon_name, self.icon_size) for icon_name in icon_names]
        for name, icon in zip(button_names, icons):
            attr_name = name.replace(" ", "_").lower()
            button = ctk.CTkButton(self.sidebar,
                                   text = name,
                                   image = icon,
                                   anchor = 'w',
                                   fg_color = self.sidebar_color,
                                   bg_color = self.sidebar_color,
                                   hover_color = self.sidebar_color,
                                   text_color = '#4d4d4d',
                                   command = getattr(self, 'set_' + attr_name + '_button'))
            button.pack(fill = 'x', padx = 20, pady = 10)
            setattr(self, attr_name, button)

    def set_home_button(self):
        print("Something")

    def set_recent_button(self):
        pass

    def set_create_record_button(self):
        AddAnimal(self.window, self.main_frame).initialize_ui()

    def set_view_record_button(self):
        pass