import customtkinter as ctk
from gui.app import PlacementApp

def main():
    ctk.set_appearance_mode("Dark")  # Enforce Dark Theme
    ctk.set_default_color_theme("blue")  # Base structure
    
    app = PlacementApp()
    app.mainloop()

if __name__ == "__main__":
    main()
