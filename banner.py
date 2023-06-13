 # https://stackoverflow.com/questions/53638972/displaying-an-image-full-screen-in-python

import os

import tkinter
from PIL import Image, ImageTk
import time
import tomllib

logit = True

class Banner:

    defaultDir = "C:\\FSC\\banner\\default_pictures\\" # default photo(s) in case picDir is empty
    #picDir = "C:\\Users\\rfsc\\Pictures\\" # where to find pictures to show (in alpha order)
    picDir = "P:\\Banner\\Pictures\\"
    config_file_name = "P:\\Banner\\banner.cfg"
    imageTypes = [".jpg", ".png", "jpeg"] # assume three-letter file types (MS Windows)
    delay = 15 # number of seconds to show each pic
    keepCycling = True # change to False to stop the program
    win = None # main Tk window
    canvas = None # Tk canvas for drawing the pics
    width = None # screen width in pixels
    height = None # screen height in pixedils

    def __init__(self):
        #global win, canvas, width, height
        # set defaults
        self.win = tkinter.Tk()
        self.width = self.win.winfo_screenwidth() # get the display width
        self.height =self.win.winfo_screenheight() # get the display height
        self.win.overrideredirect(1) # don't show the title bar
        self.win.geometry("%dx%d+0+0" % (self.width, self.height)) # create a window that covers the screen
        self.win.focus_set() # give it the focus
        self.win.attributes("-topmost", 1) # and to be extra careful, force it to the top
        #self.win.bind("<Escape>", lambda e: self.endCycling(e)) # escape key stops the program

        # get config parameters that might override defaults
        try:
            with open(self.config_file_name, "rb") as config_file:
                cfg = tomllib.load(config_file)
            if logit: print(type(cfg), cfg)
            self.delay = cfg["runtime"]["delay_time"]
            if logit: print(f'setting delay to: {self.delay}')
        except Exception as err:
            if logit: print(f'>>> Error: Could not set configuration overrides because:\n{err}')


        # canvas is our workarea in the window
        self.canvas = tkinter.Canvas(self.win,width=self.width,height=self.height,border=0)
        self.canvas.pack()
        self.canvas.configure(background='black')

        while(self.keepCycling):
            if logit: print("\nNext pass:")
            self.cycle()

        self.quit()


    def quit(self):
        self.win.destroy()

    def showPIL(self, pilImage):
        #global win, canvas, width, height
        imgWidth, imgHeight = pilImage.size
        # resize photo to full screen 
        ratio = min(self.width/imgWidth, self.height/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.LANCZOS)   
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = self.canvas.create_image(self.width/2,self.height/2,image=image)
        self.win.update_idletasks()
        self.win.update()
        self.win.bind("<Escape>", lambda e: self.endCycling(e)) # escape key stops the program
        #root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

    def cycle(self):
        #global win, canvas, width, height
        sourceDir = self.picDir
        try:
            fileNames = os.listdir(sourceDir)
        except:
            fileNames = []
        # if no files in the target directory, use the defaults
        if(fileNames == []):
            sourceDir = self.defaultDir
            fileNames = os.listdir(sourceDir)
        if logit: print(fileNames)
        for fileName in fileNames:
            path = sourceDir + fileName
            if logit: print("showing:", path)
            if path[-4:] in self.imageTypes:
                try:
                    image=Image.open(path)
                    foo = self.delay
                    while((foo > 0) and (self.keepCycling)):
                        foo -= 1
                        if logit: print("foo, keepCycling:", foo, self.keepCycling)
                        self.showPIL(image)
                        time.sleep(1)

                except:
                    if logit: print(f"{path} failed")

    def endCycling(self, e):
        global keepCycling

        self.keepCycling = False
        if logit: print("stopping:", e)

if __name__ == '__main__':            
    banner = Banner()
