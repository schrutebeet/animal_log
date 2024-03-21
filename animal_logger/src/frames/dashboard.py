import customtkinter as ctk

from animal_logger.src.frames.login_page import LoginPage

class Dashboard(LoginPage):

    def __init__(self):
        super().__init__()
        self.frame = ctk.CTkFrame(master = self.window, width = 500, height = 500, corner_radius = 0)
