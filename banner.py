'''
    https://stackoverflow.com/questions/53638972/displaying-an-image-full-screen-in-python
'''
# TODO: one loop: do next image immediately

import os
from tkinter import *
from PIL import Image, ImageTk
import tomllib

logit = False
debug = False

# set default locations
defaultDir : str = "C:\\FSC\\banner\\default_pictures\\" # default photo(s) in case picDir is empty
picDir : str = "P:\\Banner\\Pictures\\"
config_file_name : str = "P:\\Banner\\banner.cfg"

# runtime defaults
imageTypes = [".jpg", ".png", "jpeg"] # check the last four characters of the filename
delay : int = 10 # number of seconds to show each pic, override in config
keepCycling : bool = True # change to False to stop the program
win : Tk = None # main Tk window
canvas : Canvas = None # Tk canvas for drawing the pics
width : int = None # screen width in pixels
height : int = None # screen height in pixedils
counter : int = 0 # seconds remaining to next image
thisImage : ImageTk.PhotoImage = None # image being displayed
nextImage : ImageTk.PhotoImage = None # next image to be displayed when counter < 1
pathNames = [] # current list of files to show
cycleTime : int = 999 # milliseconds per "second" (adjust for different speed machines)

doCycleLoop = None # Tk after pointer
countDownLoop = None # Tk after pointer

def init():
    global debug, win, canvas, width, height, delay
    if debug: # adjust default locations for debugging
        defaultDir = "C:\\FSC\\banner\\default_pictures\\" # default photo(s) in case picDir is empty
        picDir = "C:\\Users\\rfsc\\Pictures\\" # where to find pictures to show (in alpha order)
        config_file_name = "C:\\Users\\rfsc\\rfslib\\banner\\banner.cfg"
        delay = 5

    # set up the display window
    win = Tk()
    width = win.winfo_screenwidth() # get the display width
    height = win.winfo_screenheight() # get the display height
    if debug: # only show on a ninth of the screen for debugging
        width = int(width / 3)
        height = int(height / 3)
    win.geometry("%dx%d+0+0" % (width, height)) # create a window that covers the screen
    win.focus_set() # give it the focus
    if not debug: # if not debugging, ensure the images completely cover the screen
        win.attributes("-topmost", 1) # and to be extra careful, force it to the top
        win.overrideredirect(1) # don't show the title bar
    win.bind("<Escape>", quit) # escape key stops the program

    # canvas is our workarea in the window
    canvas = Canvas(win, width=width, height=height)
    canvas.pack()
    canvas.configure(background='black')

    doCycle() # start the build/getparms cycle
    countDown() # start the display next cycle
    win.mainloop() # and go, go, go

def doCycle():
    global debug, keepCycling, doCycleLoop, nextImage, pathNames, win, cycleTime, doNextImage
    if debug: print('doCycle():')
    if keepCycling == False:
        doCycleLoop = None
        return
    if nextImage == None:
        getParms() # get parms (??? ony when prepping next image ???)
        if len(pathNames) < 1:
            getImagePaths()
        buildNextImage(pathNames.pop(0))
        
    doCycleLoop = win.after(cycleTime, doCycle)

def countDown():
    global debug, keepCycling, countDownLoop, counter, nextImage, cycleTime, doNextImage
    if debug: print('countDown():')
    if keepCycling == False:
        countDownLoop = None
        return
    showNextImage()
    nextImage = None
    '''
    counter -= 1
    if counter < 1:
        if nextImage != None:
            showNextImage()
            nextImage = None
            counter = delay
    '''
    countDownLoop = win.after(cycleTime*delay, countDown)

def quit(e):
    global debug, keepCycling, doCycleLoop, win, countDownLoop
    if debug: print(f'quit(): {e}')
    keepCycling = False
    if doCycleLoop != None:
        win.after_cancel(doCycleLoop)
    if countDownLoop != None:
        win.after_cancel(countDown)
    win.destroy()
    return

def getImagePaths():
    global debug, picDir, sourceDir, pathNames, logit
    '''
        this isn't thread-safe with doCycle, so let doCycle call it
    '''
    if debug: print('getImagePaths():')
    # try to get a list from the working image directory
    try:
        sourceDir = picDir
        fileNames = os.listdir(sourceDir)
    except:
        fileNames = []

    # if no files in the working directory, use the defaults
    if fileNames == []:
        sourceDir = defaultDir
        fileNames = os.listdir(sourceDir)

    # only return pathnames that are images (based on Windows extension)
    #if logit: print(fileNames)
    for fileName in fileNames:
        path = sourceDir + fileName
        if path[-4:] in imageTypes:
            pathNames.append(path)

    if logit: print('  files to show: ', pathNames)
    return

def buildNextImage(path) -> ImageTk.PhotoImage:
    global debug, logit, nextImage, width, height, canvas
    if debug: print(f'buildNextImage({path}):')
    try: # read the image from disk
        image=Image.open(path)
    except: # read failure (image deleted? not an image?)
        if logit: print(f"{path} failed")
        return None
    # if necessary, size the image to fit in the canvas
    imgWidth, imgHeight = image.size
    ratio = min(width/imgWidth, height/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    nextImage = ImageTk.PhotoImage(image.resize((imgWidth, imgHeight), Image.LANCZOS))
    return

def showNextImage():
    global debug, canvas, width, height, thisImage, nextImage
    if debug: print('showNextImage():')
    thisImage = nextImage
    canvas.create_image(width/2, height/2, image=thisImage)
    return

def getParms():
    global debug, config_file_name, delay, logit
    if debug: print('getParms():')
    # get config parameters that might override defaults
    try:
        with open(config_file_name, "rb") as config_file:
            cfg = tomllib.load(config_file)
        if debug: print(type(cfg), cfg)
        delay = cfg["runtime"]["delay_time"]
        if logit: print(f'setting delay to: {delay}')
    except Exception as err:
        if logit: print(f'>>> Error: Could not set configuration overrides because: {err}')
    return

if __name__ == '__main__':            
    init()

