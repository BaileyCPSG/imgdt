import csv
import os
from PIL import Image
import requests
from tkinter import filedialog as fd

def resizeAllImages(imagedir, errfile):
    errfile.write("\nSTART OF RESIZEING ERRORS\n")
    imgs = os.listdir(imagedir)
    for x in range(len(imgs)):
        try:
            fp = imagedir + imgs[x]
            img = Image.open(fp)
            img.thumbnail((600, 600))
            img.save(fp)
            img.close()
            print(f"{fp} was resized successfully!")
        except Exception as e:
            print(f"Error on {imgs[x]}: {e}")
            errfile.write(f"{e}\n")

def main():
    try:
        fns = []    # filenames list
        urls = []   # urls list
        errfilepath = fd.askopenfilename(title="Select Location of Error File") # location of error file
        errfile = open(errfilepath, 'w')
        csvfilepath = fd.askopenfilename(title="Select The CSV File", filetypes=[('.csv', '.csv')]) # location of csv file containing urls and filenames
        imagedir = fd.askdirectory(title="Select Location of Image Direcotry")  # location of directory to download images to
        imagedir = imagedir + "/"
        
        # Make sure this is what they want
        while(True):
            print(f"Log File: {errfilepath}")
            print(f"CSV File: {csvfilepath}")
            print(f"Image Directory: {imagedir}")
            choice = input("Is this correct (y/N): ")
            if not choice or choice.lower() == "n":
                print("Goodbye")
                errfile.close()
                exit(0)
            elif choice.lower() == "y":
                print("Starting Script...")
                break
            else:
                print("Please choose y or n!")
    except Exception as e:
        print("Error: You must choose a location!")
        exit(-1)


    # tries to make a request the image link and download the file
    try:
        # try to open the file normally and check for correct headers
        csvfile = open(csvfilepath, "r")
        reader = csv.DictReader(csvfile)
        if reader.fieldnames != ['url', 'filename']:
            # if headers are bad then try opening with utf-8 encoding and check headers again
            csvfile.close()
            print("Opening file with UTF-8 encoding.")
            csvfile = open(csvfilepath, "r", encoding="utf-8-sig")
            reader = csv.DictReader(csvfile)
        if reader.fieldnames != ['url', 'filename']:
            #exit for bad headers
            print(reader.fieldnames)
            print("Error: File must have the headers: url,filename")
            exit(-1)
        for row in reader:
            fns.append(row['filename'])
            urls.append(row['url'])

        for x in range(len(urls)):
            try:
                res = requests.get(urls[x], stream=True)
                if res.status_code == 200:
                    with open(imagedir + fns[x], "wb") as outFile:
                        for chunk in res:
                            outFile.write(chunk)
                    print(f"{fns[x]} downloaded successfully!")
                else:
                    print(f"Error: {urls[x]} had status code: {res.status_code}")
                    errfile.write(f"Error: {urls[x]} had status code: {res.status_code}\n")
            except Exception as e:
                print(e)
                errfile.write(f"{e}\n")
        print(f"\n{len(os.listdir(imagedir))} files downloaded successfully!\n")
        

        # Ask for resize
        while(True):
            rsz = input("\nDo you want to resize all the images (y/N): ")
            if not rsz or rsz.lower() == "n":
                print("Goodbye!")
                exit(0)
            elif rsz.lower() == "y":
                resizeAllImages(imagedir, errfile)
                break
            else:
                print("Please choose y or n!")
    except Exception as e:
        print(e)
    finally:
        csvfile.close()
        errfile.close()

if __name__ == '__main__':
    main()
