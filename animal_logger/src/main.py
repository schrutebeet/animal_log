import customtkinter as ctk

from config.config import Config
from animal_logger.src.frames.login_page import LoginPage
from animal_logger.src.frames.dashboard import Dashboard


if __name__ == "__main__":
    from config.config import Config
    Config()
    window = ctk.CTk() # Creates window
    LoginPage(window).initialize_ui()
    Dashboard(window).initialize_ui()
