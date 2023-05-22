 # https://stackoverflow.com/questions/53638972/displaying-an-image-full-screen-in-python

import sys, os

import tkinter
# PIL == pillow
from PIL import Image, ImageTk
import time

logit = False

defaultDir = "C:\\FSC\\banner\\default_photos\\"
picDir = "C:\\Users\\rfsc\\Pictures\\"
imageTypes = [".jpg", ".png"] # assume three-letter file types (MS Windows)
delay = 5
keepCycling = True
win = None
canvas = None
width = None
height = None

def init():
    global win, canvas, width, height
    win = tkinter.Tk()
    width = win.winfo_screenwidth() # get the display size
    height = win.winfo_screenheight() # get the display size
    win.overrideredirect(1) # no title bar
    win.geometry("%dx%d+0+0" % (width, height)) # create a window that covers the screen
    win.focus_set() # give it the focus
    win.attributes("-topmost", 1) # and to be extra careful, force it to the top
    win.bind("<Escape>", lambda e: endCycling(e))

    # canvas is our workarea in the window
    canvas = tkinter.Canvas(win,width=width,height=height)
    canvas.pack()
    canvas.configure(background='black')

def quit():
    win.destroy()

def showPIL(pilImage):
    global win, canvas, width, height
    imgWidth, imgHeight = pilImage.size
    # resize photo to full screen 
    ratio = min(width/imgWidth, height/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    pilImage = pilImage.resize((imgWidth,imgHeight), Image.LANCZOS)   
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(width/2,height/2,image=image)
    win.update_idletasks()
    win.update()
    #root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    #win.bind("<Escape>", lambda e: endCycling(e))


def cycle():
    global win, canvas, width, height
    sourceDir = picDir
    try:
        fileNames = os.listdir(sourceDir)
    except:
        fileNames = []
    # if no files in the target directory, use the defaults
    if(fileNames == []):
        sourceDir = defaultDir
        fileNames = os.listdir(sourceDir)
    if logit: print(fileNames)
    for fileName in fileNames:
        path = sourceDir + fileName
        if logit: print("showing:", path)
        if path[-4:] in imageTypes:
            try:
                image=Image.open(path)
                foo = delay
                while((foo > 0) and (keepCycling)):
                    foo -= 1
                    if logit: print("foo, keepCycling:", foo, keepCycling)
                    showPIL(image)
                    time.sleep(1)

            except:
                if logit: print(f"{path} failed")

def endCycling(e):
    global keepCycling

    keepCycling = False
    if logit: print("stopping:", e)

if __name__ == '__main__':            
    init()
    while(keepCycling):
        if logit: print("\nNext pass:")
        cycle()
    quit()