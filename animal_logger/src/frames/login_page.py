import os
from pathlib import Path

import tkinter
import customtkinter as ctk
from PIL import ImageTk, Image

import animal_logger
from config.config import Config
from config.log_config import LOGGER
from animal_logger.src.db.utils_db import UtilsDB
from animal_logger.src.frames.baseframe import BaseFrame
from animal_logger.src.frames.dashboard import Dashboard


class LoginPage(BaseFrame):

    def __init__(self, window) -> None:
        super().__init__(window)
        self.window = window
        self.login_image = None
        self.login_image_label = None
        self.error_message = None

    def get_image_path(self, img_name: str) -> Path:
        # Adjust this method to find your image correctly
        repo_path = Path(animal_logger.__file__).parent
        return repo_path / "opt/img" / img_name

    def initialize_ui(self):
        """Initialize the UI of the newly-created window.
        """
        # self.resize_image()
        # self.app.bind('<Configure>', self.resize_image)
        self.add_frame()
        self.add_username_password()
        self.add_forgot_password()
        self.add_login_button()
        self.add_exit_button()
        self.window.mainloop()

    def resize_image(self, event: str = None) -> None:
        """Take image and automatically resize it according to the current window shape requirements
        by the user. If the image label is not created, it proceeds to do so, otherwise it configures
        the image label with the latest reshaped version of the image.
        
        IMPORTANT:
        In the context of GUI development, labels and canvases refer to the object that holds an image 
        and can perform several actions to it, like change its relative position, respond to mouse clicks...

        Args:
            event (str, optional): Type of event that needs to happen for the method to work. 
            Defaults to None.
        """
        img_path = self.get_image_path('login.jpg')
        img = Image.open(img_path)

        # Resize the image to the current window size
        new_width = self.window.winfo_width()
        new_height = self.window.winfo_height()
        # Resize to new window size using LANCZOS resampling filter
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Update login image
        self.login_image = ImageTk.PhotoImage(img)

        # If label already exists 
        if self.login_image_label:
            self.login_image_label.configure(image=self.login_image)
        else:
            self.login_image_label = ctk.CTkLabel(master=self.window, image=self.login_image, text = "")
            self.login_image_label.place(x=0, y=0, relwidth=1, relheight=1)

    def add_frame(self) -> None:
        self.frame = ctk.CTkFrame(master = self.login_image_label, width = 350, height = 370, corner_radius = 15)
        self.frame.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)
        self.frame_title = ctk.CTkLabel(master = self.frame, text = "Log in into your account", 
                                        font = ("Montserrat", 20))
        self.frame_title.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

    def add_username_password(self) -> None:
        self.username = ctk.CTkEntry(master = self.frame, width = 235, placeholder_text = "Username")
        self.username.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.password = ctk.CTkEntry(master = self.frame, width = 235, show = "*", placeholder_text = "Password")
        self.password.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

    def add_forgot_password(self) -> None:
        self.hyperlink_label = ctk.CTkLabel(master = self.frame, text="Forgot password?", 
                                            font = ("Montserrat", 12), cursor="hand2")
        self.hyperlink_label.place(relx=0.68, rely=0.53, anchor=tkinter.CENTER)

    def add_login_button(self) -> None:
        self.login_button = ctk.CTkButton(master = self.frame, width = 235, text = "Login", command=self.attempt_login)
        self.login_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def add_exit_button(self) -> None:
        self.login_button = ctk.CTkButton(master = self.frame, width = 235, text = "Exit", 
                                          fg_color = "#727272", command=self.exit_application)
        self.login_button.place(relx=0.5, rely=0.82, anchor=tkinter.CENTER)

    def attempt_login(self) -> None:
        # Fetch username and password
        username = str(self.username.get())
        os.environ["USERNAME"] = username
        password = str(self.password.get())
        os.environ["PASSWORD"] = password
        LOGGER.info(f"Attempting to login with {username}:{password}")
        db_url = Config.get_info()['db_url']
        login_table, message = UtilsDB.get_table(schema = 'credentials', table_name = 'login_app', engine = db_url)
        # Erase any previous text if any
        if self.error_message:
            self.error_message.configure(text='')
        if not message: # user is correctly logged in
            user_exists = len(login_table.loc[(login_table['username'] == username) 
                                            & (login_table['password'] == password)].index)
            if user_exists: # user is in login database
                for widget in self.window.winfo_children():
                    widget.destroy()
                    # Dashboard(self.window).initialize_ui()
        else:
            self.error_message = ctk.CTkLabel(master = self.frame, text = message, 
                                                font = ("Montserrat", 12, "bold"), text_color = '#FF0000')
            self.error_message.place(relx=0.17, rely=0.58)
        
    def exit_application(self):
        self.window.destroy()
