from gui import App
from tkinter import PhotoImage

def main():
    app = App()
    app.iconphoto(False, PhotoImage(file="../images/centre.ico"))
    app.title("IMGDT")
    app.resizable(False, False)
    app.mainloop()

if __name__ == '__main__':
    main()
