import customtkinter as ctk
from gui.app import PlacementApp

def main():
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    app = PlacementApp()
    app.mainloop()

if __name__ == "__main__":
    main()
