import imgdt
from tkinter import scrolledtext
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # Main Frame that all Widgets go inside
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0)

        # Frame for all the input Widgets
        self.inputFrame = ttk.Frame(self.mainframe)
        self.inputFrame.grid(column=0, row=0)

        # Frame for all the progress Widgets
        self.progressFrame = ttk.Frame(self.mainframe, padding="0 10 0 0")
        self.progressFrame.grid(column=0, row=1)

        # Frame for all Loggin Widgets
        self.loggerFrame = ttk.Frame(self.mainframe, padding = "0 10 0 0")
        self.loggerFrame.grid(column=0, row=2)

        # Frame for the Start and Exit Buttons
        self.buttonFrame = ttk.Frame(self.inputFrame)
        self.buttonFrame.grid(column=1, row=2)


        # Input CSV Widgets
        self.inputLabel = ttk.Label(self.inputFrame, text="Input File:", width=18)
        self.inputLabel.grid(column=0, row=0, sticky=tk.W)

        self.inputTextbox = ttk.Entry(self.inputFrame, width=50)
        self.inputTextbox.grid(column=1, row=0)

        self.inputBrowseButton = ttk.Button(self.inputFrame, text="Browse...", command=(lambda: imgdt.getInputFile(self.inputTextbox)))
        self.inputBrowseButton.grid(column=2, row=0)


        # Image Directory Widgets
        self.imageDirLabel = ttk.Label(self.inputFrame, text="Image Folder:", width=18)
        self.imageDirLabel.grid(column=0, row=1, sticky=tk.W)

        self.imageDirTextbox = ttk.Entry(self.inputFrame, width=50)
        self.imageDirTextbox.grid(column=1, row=1)

        self.imageDirButton = ttk.Button(self.inputFrame, text="Browse...", command=(lambda: imgdt.getImageDir(self.imageDirTextbox)))
        self.imageDirButton.grid(column=2, row=1)


        # Resize Checkbox Widgets
        self.resizeFlag = tk.IntVar()
        self.resizeCheckButton = ttk.Checkbutton(self.inputFrame, text="Resize", variable=self.resizeFlag, onvalue=True, offvalue=False)
        self.resizeCheckButton.grid(column=0, row=2, sticky=tk.W)


        # Start and Exit Button Widgets
        self.startButton = ttk.Button(self.buttonFrame, text="Start", command=(lambda: imgdt.start(self)))
        self.startButton.grid(column=0, row=0)

        self.exitButton = ttk.Button(self.buttonFrame, text="Exit", command=(lambda: self.quit()))
        self.exitButton.grid(column=1, row=0)

        
        # Progress Bar Widgets
        self.progressLabel = ttk.Label(self.progressFrame, text="Waiting:", width=18)
        self.progressLabel.grid(column=0, row=0, sticky=tk.W)

        self.progressBar = ttk.Progressbar(self.progressFrame, orient="horizontal", mode="determinate", length=380)
        self.progressBar.grid(column= 1, row = 0)


        # Logger Widgets
        self.loggerView = scrolledtext.ScrolledText(self.loggerFrame, state="disabled")
        self.loggerView.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
