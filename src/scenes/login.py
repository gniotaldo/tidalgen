import tkinter as tk
from core import auth

class LoginScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        login_button = tk.Button(
            self,
            text="Log In",
            font=("Arial", 16),
            width=15,
            height=2,
            command=self.on_login_click
        )
        login_button.pack(expand=True)

    def on_login_click(self):
        print("[LoginScene] Logging in...")
        self.controller.app_state.session = auth.authorize_tidal()

        if self.controller.app_state.session is not None:
            print("[LoginScene] Session acquired. Redirecting to Main Menu...")
            self.controller.show_frame("main_menu")
        else:
            print("[LoginScene] Login failed.")
