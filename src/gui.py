import tkinter as tk
from tkinter import ttk
import imgdt

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0)

        self.inputLabel = ttk.Label(self.mainframe, text="Input File:", width=15)
        self.inputLabel.grid(column=0, row=0, sticky=tk.W)

        self.inputTextbox = ttk.Entry(self.mainframe, width=50)
        self.inputTextbox.grid(column=1, row=0)

        self.inputBrowseButton = ttk.Button(self.mainframe, text="Browse...", command=(lambda: imgdt.getInputFile(self.inputTextbox)))
        self.inputBrowseButton.grid(column=2, row=0)


        self.imageDirLabel = ttk.Label(self.mainframe, text="Image Folder:")
        self.imageDirLabel.grid(column=0, row=1, sticky=tk.W)

        self.imageDirTextbox = ttk.Entry(self.mainframe, width=50)
        self.imageDirTextbox.grid(column=1, row=1)

        self.imageDirButton = ttk.Button(self.mainframe, text="Browse...", command=(lambda: imgdt.getImageDir(self.imageDirTextbox)))
        self.imageDirButton.grid(column=2, row=1)


        self.resizeFlag = tk.StringVar()
        self.resizeCheckButton = ttk.Checkbutton(self.mainframe, text="Resize", variable=self.resizeFlag, onvalue=True, offvalue=False)
        self.resizeCheckButton.grid(column=0, row=2, sticky=tk.W)


        self.buttonFrame = ttk.Frame(self.mainframe)
        self.buttonFrame.grid(column=1, row=2)

        self.goButton = ttk.Button(self.buttonFrame, text="Go", command=(lambda: imgdt.start(self)))
        self.goButton.grid(column=0, row=0)

        self.cancelButton = ttk.Button(self.buttonFrame, text="Cancel", command=(lambda: self.quit()))
        self.cancelButton.grid(column=1, row=0)
