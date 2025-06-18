from app_controller import AppController
from app_state import state

if __name__ == "__main__":
    app = AppController(state)
    app.mainloop()