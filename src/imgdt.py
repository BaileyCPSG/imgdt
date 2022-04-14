import csv
import os
import requests
from tkinter import filedialog as fd

def main():
    try:
        fns = []    # filenames list
        urls = []   # urls list
        errfilepath = fd.askopenfilename(title="Select Location of Error File") # location of error file
        errfile = open(errfilepath, 'w')
        csvfilepath = fd.askopenfilename(title="Select The CSV File", filetypes=[('csvfiles', '.csv')]) # location of csv file containing urls and filenames
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
        with open(csvfilepath) as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames != ['url', 'filename']:
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
    except Exception as e:
        print(e)
    finally:
        errfile.close()

if __name__ == '__main__':
    main()
