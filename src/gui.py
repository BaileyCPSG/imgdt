from tkinter import *
from tkinter import ttk


def main():
    root = Tk()
    root.title("IMGDT")
    

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0)

    inputLabel = ttk.Label(mainframe, text="Input File:")
    inputLabel.grid(column=0, row=0)

    inputTextbox = ttk.Entry(mainframe)
    inputTextbox.grid(column=1, row=0)

    inputBrowseButton = ttk.Button(mainframe, text="Browse...")
    inputBrowseButton.grid(column=2, row=0)
    

    imageDirLabel = ttk.Label(mainframe, text="Image Folder")
    imageDirLabel.grid(column=0, row=1)

    imageDirTextbox = ttk.Entry(mainframe)
    imageDirTextbox.grid(column=1, row=1)
    
    imageDirButton = ttk.Button(mainframe, text="Browse...")
    imageDirButton.grid(column=2, row=1)
    

    resizeCheckButton = ttk.Checkbutton(mainframe, text="Resize")
    resizeCheckButton.grid(column=0, row=2)


    goButton = ttk.Button(mainframe, text="Go")
    goButton.grid(column=1, row=2)

    cancelButton = ttk.Button(mainframe, text="Cancel", command=exit)
    cancelButton.grid(column=2, row=2)

    root.mainloop()

if __name__ == '__main__':
    main()
