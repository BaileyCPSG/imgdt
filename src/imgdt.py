import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
from PIL import Image
import requests
from math import floor
import os
import csv

# Global varialbes
errfilepath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), "log.txt"))
errfile = open(errfilepath, 'w')
sucfilepath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), "success.txt"))
sucfile = open(sucfilepath, 'w')

def writeLoggerView(message, app):
    app.loggerView['state'] = "normal"
    app.loggerView.insert(tk.END, message)
    app.loggerView['state'] = "disabled"

def resizeAllImages(imagedir, app):
    errfile.write("\nINFO: Resizing Started\n")
    writeLoggerView("INFO: Resizing Started\n", app)
    imgs = os.listdir(imagedir)
    counter = 0
    valuecnt = 0
    for x in range(len(imgs)):
        try:
            fp = imagedir + imgs[x]
            img = Image.open(fp)
            img.thumbnail((600, 600))
            img.save(fp)
            img.close()
            sucfile.write(f"RESIZE: {fp} was resized successfully!\n")
            writeLoggerView(f"RESIZE: {fp} was resized successfully!\n", app)
            counter += 1
        except Exception as e:
            errfile.write(f"RESIZE: {e}\n")
            writeLoggerView(f"RESIZE: {e}\n", app)
        valuecnt += 1
        value = floor((valuecnt / len(imgs) * 100))
        app.progressBar['value'] = value
        app.progressLabel['text'] = f"Resizing {value}%"
        app.update()
    sucfile.write(f"\nRESIZE: {counter}/{len(imgs)} files resized successfully!\n\n")
    writeLoggerView(f"RESIZE: {counter}/{len(imgs)} files resized successfully!\n", app)
    showinfo(title="Success", message=(f"\n{counter}/{len(imgs)} files were resized!\nCheck the log file for errors!"))

def hasFileExt(filenames, app):
    flag = True
    errfile.write("INFO: File Extension Check Started\n")
    writeLoggerView("INFO: File Extension Check Started\n", app)
    fileExts = ["jpg", "png", "peg"]
    for f in filenames:
        ext = f[-3:]
        if not ext in fileExts:
            errfile.write(f"FILEEXT: {f} has the wrong file extension!\n")
            writeLoggerView(f"FILEEXT: {f} has the wrong file extension!\n", app)
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
            writeLoggerView("ERROR: Locations cannot be null\n", app)
            showerror(title="File Error", message="File locations cannot be blank!")
            return

        # Check if exists
        if os.path.exists(csvfilepath) and os.path.isfile(csvfilepath) and os.path.exists(imagedir) and os.path.isdir(imagedir) and (imagedir[-1] == "\\" or imagedir[-1] == "/"):
            errfile.write("INFO: Starting Script...\n")
            writeLoggerView("INFO: Starting Script...\n", app)
        else:
            showerror(title="Error", message="Cannot open file or directory. Please double check spelling.")
            errfile.write("ERROR: Cannot open file or directory. Please double check spelling.\n")
            writeLoggerView("Error: Cannot open file or directory. Please double check spelling.\n", app)
            return

    except Exception as e:
        showerror(title="Error", message="Cannot open file or directory. Please double check spelling.")
        errfile.write("Error: Cannot open file or directory. Please double check spelling.\n")
        writeLoggerView("Error: Cannot open file or directory. Please double check spelling.\n", app)
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
            writeLoggerView("INFO: Opening file with UTF-8 encoding.\n", app)
            csvfile = open(csvfilepath, "r", encoding="utf-8-sig")
            reader = csv.DictReader(csvfile)
        if reader.fieldnames != ['url', 'filename']:
            #exit for bad headers
            errfile.write("ERROR: File must have the headers: url,filename\n")
            writeLoggerView("ERROR: File must have the headers: url,filename\n", app)
            showerror(title="Error", message="File must have the headers: url,filename")
            stop(-1)
        for row in reader:
            fns.append(row['filename'])
            urls.append(row['url'])

        # after lists are loaded, check for filename extensions
        if not hasFileExt(fns, app):
            showerror(title="Error", message="Filenames must include extensions\nPlease check the log file for more info!\n")
            stop(-1)

        errfile.write("\nINFO: Downloading Started\n")
        writeLoggerView("INFO: Downloading Started\n", app)

        counter = 0
        valuecnt = 0
        for x in range(len(urls)):
            try:
                res = requests.get(urls[x], stream=True)
                if res.status_code == 200:
                    with open(imagedir + fns[x], "wb") as outFile:
                        for chunk in res:
                            outFile.write(chunk)
                    sucfile.write(f"DOWNLOAD: {fns[x]} downloaded successfully!\n")
                    writeLoggerView(f"DOWNLOAD: {fns[x]} downloaded successfully!\n", app)
                    counter += 1
                else:
                    errfile.write(f"DOWNLOAD: {urls[x]} had status code: {res.status_code}\n")
                    writeLoggerView(f"DOWNLOAD: {urls[x]} had status code: {res.status_code}\n", app)
            except Exception as e:
                print(e)
                errfile.write(f"DOWNLOAD: {e}\n")
                writeLoggerView(f"DOWNLOAD: {e}\n", app)
            valuecnt += 1
            value = floor((valuecnt / len(urls)) * 100)
            app.progressBar['value'] = value
            app.progressLabel['text'] = f"Downloading {value}%"
            app.update()
        sucfile.write(f"\nDOWNLOAD:{counter}/{len(urls)} files downloaded successfully!\n\n")
        writeLoggerView(f"DOWNLOAD:{counter}/{len(urls)} files downloaded successfully!\n", app)
        showinfo(title="Success", message=(f"{counter}/{len(urls)} files downloaded successfully!\nCheck the log file for errors."))

        if app.resizeFlag.get():
            resizeAllImages(imagedir, app)

        app.progressLabel['text'] = "Done"
        return

    except Exception as e:
        errfile.write(f"{e}\n")
        writeLoggerView(f"{e}\n", app)
