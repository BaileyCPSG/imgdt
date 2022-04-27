import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
from PIL import Image
import requests
import os
import csv

# Global varialbes
errfilepath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), "log.txt"))
errfile = open(errfilepath, 'w')
sucfilepath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), "success.txt"))
sucfile = open(sucfilepath, 'w')

def resizeAllImages(imagedir):
    errfile.write("\nINFO: Resizing Started\n")
    imgs = os.listdir(imagedir)
    counter = 0
    for x in range(len(imgs)):
        try:
            fp = imagedir + imgs[x]
            img = Image.open(fp)
            img.thumbnail((600, 600))
            img.save(fp)
            img.close()
            sucfile.write(f"RESIZE: {fp} was resized successfully!\n")
            counter += 1
        except Exception as e:
            errfile.write(f"RESIZE: {e}\n")
    showinfo(title="Success", message=(f"\n{counter}/{len(imgs)} files were resized!\nCheck the log file for errors!"))

def hasFileExt(filenames):
    flag = True
    errfile.write("INFO: File Extension Check Started\n")
    fileExts = ["jpg", "png", "peg"]
    for f in filenames:
        ext = f[-3:]
        if not ext in fileExts:
            errfile.write(f"FILEEXT: {f} has the wrong file extension!\n")
            flag = False
    return flag

def getInputFile(inputTextbox):
    csvfilepath = fd.askopenfilename(title="Select the csv input file...", filetypes=[('.csv', '.csv')])
    inputTextbox.delete(0, tk.END)
    inputTextbox.insert(0, csvfilepath)

def getImageDir(imageDirTextbox):
    imagedir = fd.askdirectory(title="Select the location of image download directory...")
    imagedir = imagedir + "/"
    imageDirTextbox.delete(0, tk.END)
    imageDirTextbox.insert(0, imagedir)

def stop(code):
    errfile.close()
    sucfile.close()
    exit(code)

def start(app):
    try:
        fns = []    # filenames list
        urls = []   # urls list
        csvfilepath = app.inputTextbox.get()
        imagedir = app.imageDirTextbox.get()

        # Check for blank input fields
        if csvfilepath == "" or imagedir == "":
            errfile.write("ERROR: Locations cannot be null\n")
            showerror(title="File Error", message="File locations cannot be blank!")
            return

        # Check if exists
        if os.path.exists(csvfilepath) and os.path.isfile(csvfilepath) and os.path.exists(imagedir) and os.path.isdir(imagedir):
            errfile.write("INFO: Starting Script...\n")
        else:
            showerror(title="Error", message="Cannot open file or directory. Please double check spelling.")
            errfile.write("Error: Cannot open file or directory. Please double check spelling.\n")
            return

    except Exception as e:
        showerror(title="Error", message="Cannot open file or directory. Please double check spelling.")
        errfile.write("Error: Cannot open file or directory. Please double check spelling.\n")
        stop(-1)


    # tries to make a request the image link and download the file
    try:
        # try to open the file normally and check for correct headers
        csvfile = open(csvfilepath, "r")
        reader = csv.DictReader(csvfile)
        if reader.fieldnames != ['url', 'filename']:
            # if headers are bad then try opening with utf-8 encoding and check headers again
            csvfile.close()
            sucfile.write("INFO: Opening file with UTF-8 encoding.\n")
            csvfile = open(csvfilepath, "r", encoding="utf-8-sig")
            reader = csv.DictReader(csvfile)
        if reader.fieldnames != ['url', 'filename']:
            #exit for bad headers
            errfile.write("ERROR: File must have the headers: url,filename\n")
            showerror(title="Error", message="File must have the headers: url,filename")
            stop(-1)
        for row in reader:
            fns.append(row['filename'])
            urls.append(row['url'])

        # after lists are loaded, check for filename extensions
        if not hasFileExt(fns):
            showerror(title="Error", message="Filenames must include extensions\nPlease check the log file for more info!\n")
            stop(-1)

        errfile.write("\nINFO: Downloading Started\n")

        counter = 0
        for x in range(len(urls)):
            try:
                res = requests.get(urls[x], stream=True)
                if res.status_code == 200:
                    with open(imagedir + fns[x], "wb") as outFile:
                        for chunk in res:
                            outFile.write(chunk)
                    sucfile.write(f"DOWNLOAD: {fns[x]} downloaded successfully!\n")
                    counter += 1
                else:
                    errfile.write(f"DOWNLOAD: {urls[x]} had status code: {res.status_code}\n")
            except Exception as e:
                print(e)
                errfile.write(f"DOWNLOAD: {e}\n")
        sucfile.write(f"\nDOWNLOAD:{counter}/{len(urls)} files downloaded successfully!\n")
        showinfo(title="Success", message=(f"{counter}/{len(urls)} files downloaded successfully!\nCheck the log file for errors."))
        
        if app.resizeFlag.get():
            resizeAllImages(imagedir)

        stop(0)

    except Exception as e:
        errfile.write(f"{e}\n")
