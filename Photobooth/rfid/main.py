from appUI import AppUI
import customtkinter as ctk

def main():
    root = ctk.CTk()
    root.attributes("-fullscreen", True)
    app = AppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
