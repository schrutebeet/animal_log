from pathlib import Path

import tkinter
import customtkinter as ctk
from PIL import ImageTk, Image

import animal_logger


class LoginPage:

    def __init__(self) -> None:
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        self.app = ctk.CTk() # Creates window
        self.app.geometry('1000x660') # Set default window size
        self.app.title("Login") # Name window tab
        self.login_image = None
        self.login_image_label = None

        self.initialize_ui()
        self.app.mainloop()

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

    def resize_image(self, event:str = None) -> None:
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
        new_width = self.app.winfo_width()
        new_height = self.app.winfo_height()
        # Resize to new window size using LANCZOS resampling filter
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Update login image
        self.login_image = ImageTk.PhotoImage(img)

        # If label already exists 
        if self.login_image_label:
            self.login_image_label.configure(image=self.login_image)
        else:
            self.login_image_label = ctk.CTkLabel(master=self.app, image=self.login_image, text = "")
            self.login_image_label.place(x=0, y=0, relwidth=1, relheight=1)

    def add_frame(self) -> None:
        self.frame = ctk.CTkFrame(master = self.login_image_label, width = 350, height = 370, corner_radius = 15)
        self.frame.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)
        self.frame_title = ctk.CTkLabel(master = self.frame, text = "Log in into your account", font = ("Century Gothic", 20))
        self.frame_title.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

    def add_username_password(self) -> None:
        self.username = ctk.CTkEntry(master = self.frame, width = 235, placeholder_text = "Username")
        self.username.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.password = ctk.CTkEntry(master = self.frame, width = 235, show = "*", placeholder_text = "Password")
        self.password.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

    def add_forgot_password(self) -> None:
        self.hyperlink_label = ctk.CTkLabel(master = self.frame, text="Forgot password?", cursor="hand2")
        self.hyperlink_label.place(relx=0.68, rely=0.53, anchor=tkinter.CENTER)

    def add_login_button(self) -> None:
        self.login_button = ctk.CTkButton(master = self.frame, width = 235, text = "Login")
        self.login_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def add_exit_button(self) -> None:
        self.login_button = ctk.CTkButton(master = self.frame, width = 235, text = "Exit", fg_color = "#727272")
        self.login_button.place(relx=0.5, rely=0.82, anchor=tkinter.CENTER)

if __name__ == "__main__":
    LoginPage()
