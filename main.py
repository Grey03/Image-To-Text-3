#Imports
from fileinput import filename

import tkinter
from tkinter import filedialog

import customtkinter

import math

from pathlib import Path

import json

import os
import os.path

from PIL import Image, ImageEnhance, ImageTk
import PIL.ImageOps


import time

import numpy as np
#-------------------------



#Global Vars
global selected_image

global fileLocation
fileLocation =  str(Path(__file__).resolve().parent)

global allowedFiletypes
allowedFiletypes = ("*.png;*.jpg;*webp")

global selectedImage
selectedImage = ""

global cords
cords = [0,0]

global bgImg
bgImg = ("test.txt")


global complexTheme
complexTheme = "Normal"


#-------------------------
root = customtkinter.CTk()
root.title("Img2Txt 3.0")
root.geometry("595x270")
root.resizable(False, False)

PATH = os.path.dirname(os.path.realpath(__file__))
root.iconbitmap(PATH + "/materials/Logo.ico")



#Have 3 seperate menu funcs

#All should have inverts and size control with sensitivties
#1. Basic, uses the single bullet points, maybe even allow the option to use their own choice
#2. Compact, uses old braille method.
#3. Complex, Using a multitude of character such as #/$ for shading allows better qual images.

#Setting for multicore risk test?! If on use

#Exrta settings tab will have multicore stuff as described before, 
# It will also contain replacements of the things used EXCEPT FOR IMG TO BRAILLE. 
# Allows you to change simple bullet points to whatever, allows different shading characters for complex


#-------------------------













def errormessage(errorTxt):
   tkinter.messagebox.showerror("Uh oh!",str(errorTxt))



def getsettings():
    filename = "settings.json"
    filepath = Path(__file__).resolve().parent/filename

    with open(filepath) as f:
        settingsJson = json.load(f)
        f.close()

    return settingsJson


def selectimage():
    global allowedFiletypes
    global selectedImage
    #Selects File
    selectedImage = filedialog.askopenfilename(initialdir = "C:/",
                                          title = "Select a File",
                                          filetypes = [("Accepted files", allowedFiletypes)])



















def mainimageconverter(*args):
    #Should be filename as a string, dimensions as (x,y) (If they are 0, 0 leave be), true false invert, constrast level, material, finally which mode (0-2), true false multicore
    imagePresets = ["filepath", [0,0], True, 128, ["Symbols"], "Simple", False] #example
    errors = []
    if (len(imagePresets) == len(args)):
        for i in range(len(imagePresets)):
            if (type(imagePresets[i]) != type(args[i])):
                errors.append(str(i))
                errors.append(type(imagePresets[i]))
        if (len(errors) > 0):
            for i in range(0, len(errors), 2):
                message = ("ERROR: IMG CON MAIN: Problem with var type on var: " + str(errors[i]) + ". It is currently a(n) " + str(errors[i+1]) + "it should be " + str(type(imagePresets[i])))
                errormessage(message)
                return
        else:
            imagePresets = args
    else:
        errormessage("ERROR: IMG CON MAIN: Not enough vars for main img convert func.")
        return

    try:
        image = Image.open(imagePresets[0]).convert("L")
    except:
        errormessage("ERROR: IMG CON MAIN: Image; does not exist, cannot be opened, or has not been selected.")
        return



    if imagePresets[1] != [0,0]:
        image = image.resize((imagePresets[1][0], imagePresets[1][1]))
        
        
    if imagePresets[5] == "Compressed":
        while (image.size[0]%2 != 0):
            image = image.resize((image.size[0] + 1, image.size[1]))
        while (image.size[1]%3 != 0):
            image = image.resize((image.size[0], image.size[1] + 1))
        

    print(image.size)

    if (imagePresets[2] == True):
        image = PIL.ImageOps.invert(image)






    def simpleconvert(img, sens, sym):
        global fileLocation
        
        

        print ("STARTING SIMPLE CONVERT")
        f = open(fileLocation + "output.txt", "a", encoding="utf-8")
        for y in range(image.size[1]):
            if (y != 0):
                f.write("\n")
            for x in range(image.size[0]):
                if image.getpixel((x,y)) >= sens:
                    f.write(sym)
                else:
                    f.write(" ")
        f.close()
        
        os.startfile(fileLocation + "output.txt")
        time.sleep(.5)
        os.remove(fileLocation + "output.txt")
        
    def chunkAnalyzer(chunklist, sens):
        global Invert 
        thelist = [
        chunklist[5],
        chunklist[3],
        chunklist[1],
        chunklist[4],
        chunklist[2],
        chunklist[0]
      ]
        temp = ("")
        for n in range(len(thelist)):
            if thelist[n] >= sens:
                thelist[n] = 1
            else:
                thelist[n] = 0
        for i in range(len(thelist)):
            temp = (str(temp) + str(thelist[i]))
        temp = int(temp,2)
        temp = (temp + 10240)
        return (chr(temp))
        
    def compressedconvert(img, sens):
        temp = []
        temp2 = []
        f = open(fileLocation + "output.txt", "a", encoding="utf-8")

        print ("STARTING COMPRESSED")
        for y in range(0,img.size[1],3):
            temp.append(temp2)
            temp2 = []
            for x in range(0, img.size[0],2):
                chunk = [
                (img.getpixel((x,y))),
                (img.getpixel((x + 1,y))),
                (img.getpixel((x,y + 1))),
                (img.getpixel((x + 1,y + 1))),
                (img.getpixel((x,y + 2))),
                (img.getpixel((x + 1,y + 2)))
                ]

                f.write((chunkAnalyzer(chunk, sens)))
            f.write("\n")
        f.close()
        os.startfile(fileLocation + "output.txt")
        time.sleep(.5)
        os.remove(fileLocation + "output.txt")

    def complexconvert(img, syms):
        global fileLocation

        skipNum = math.floor(256 / len(syms))
        limitList = []

        for n in range(len(syms)):
            limitList.append(n * skipNum)

        def closestNum(list, val, syms):
            arr = np.asarray(list)
            i = (np.abs(arr-val)).argmin()

            return syms[i]

        print("STARTING COMPLEX")
        f = open(fileLocation + "output.txt", "a", encoding="utf-8")
        for y in range(img.size[1]):
            if (y != 0):
                f.write("\n")
            for x in range(img.size[0]):
                f.write(closestNum(limitList,img.getpixel((x,y)), syms))
        f.close()
        
        os.startfile(fileLocation + "output.txt")
        time.sleep(.5)
        os.remove(fileLocation + "output.txt")


    if (imagePresets[5] == "Simple"):
        simpleconvert(image,imagePresets[3],str(imagePresets[4][0]))
    if (imagePresets[5] == "Compressed"):
        compressedconvert(image,imagePresets[3])
    if (imagePresets[5] == "Complex"):
        complexconvert(image, imagePresets[4])

    print ("Finished Convert")
    























def helpmenu():
    menu = customtkinter.CTkToplevel()
    menu.geometry("700x600")

    PATH = os.path.dirname(os.path.realpath(__file__))
    menu.iconbitmap(PATH  + "/materials/Logo.ico")

    menu.title("Help Menu")

    helpTitle = customtkinter.CTkLabel(master=menu, text="Welcome to the Help Menu!\n", text_font=(0,12))
    helpTitle.pack()

    aboutSection = customtkinter.CTkLabel(master=menu, text=("Hello and welcome to Text To Image!\nThis program takes an image and creates text in a file to look like it.\nThis have been a project that I keep redoing with slight improvements.\nThere are 3 modes that have different unique outputs.\n"))
    aboutSection.pack()


    aboutVariables = customtkinter.CTkLabel(master=menu, text=("Before we can discuss generator types you should know the controls you have over it.\nInvert takes the negative of you image and uses that in the process. Invert works with all modes.\nSensitivity changes how easy it is for a spot to be \"filled\".This setting only applies to simple and compact mode.\nFinally are dimensions, dimensions resize the image to fit in the dimentions of characters.\nSo, (5,10) would be 5 letters wide and 10 tall. This is useful when you are limited with character count.\nThere are some secret features where you can change the symbol for simple and complex.\n"))
    aboutVariables.pack()

    # = customtkinter.CTkLabel(master=menu, text=(""))

    simpleExplanation = customtkinter.CTkLabel(master=menu, text=("The simple mode is, well, simple!\nIn simple mode the output with either have a character per pixel or not.\nThis makes very large images because it wastes space but it can look great.\n I recommend compact, It looks similar to simple but takes up less space.\nIt does allow for custom symbols while also allowing control over sensitivity.\n"))
    simpleExplanation.pack()

    compactExplanation = customtkinter.CTkLabel(master=menu, text=("The compact mode is similar to simple\n You cannot change the look of each dot because this is made up of braille.\nThe braille dots allow for a small file with the same resolution as simple.\nIt lacks the custom symbol feature but still works with sensitvity and Invert.\n"))
    compactExplanation.pack()

    complexExplanantion = customtkinter.CTkLabel(master=menu, text=("Lastly is Complex\nComplex mode is similar to simple mode. Each pixel has one letter.\nInstead of it being a single symbol, It chooses from a list to what is closest to the darkness of the pixel.\nUnlike the other modes this one has shading.\n"))
    complexExplanantion.pack()

def hmbutton():
    helpmenu()





def settingsmenu():
    global simpleKey
    global complexPicker
    

    global complexTheme 
    settings = getsettings()
    menu = customtkinter.CTkToplevel()

    PATH = os.path.dirname(os.path.realpath(__file__))
    menu.iconbitmap(PATH + "/materials/Logo.ico")
    

    menu.title("Settings Menu")

    settingsTitle = customtkinter.CTkLabel(master=menu, text="Welcome to the Settings Menu!", text_font=(0,12))
    settingsTitle.grid(row=0,column=0,pady=10)

    simpleKey = customtkinter.CTkEntry(master=menu, placeholder_text=("Current Simple Letter: " + str(settings["SimpleSym"])), width=250)
    simpleKey.grid(row=1,column=0, padx=20,pady=20)

    complexPicker = customtkinter.CTkComboBox(master=menu, values=(list(settings["ComplexThemes"])))
    complexPicker.grid(row=2,column=0, pady=10)

    def save():
        global simpleKey
        global complexPicker
        global complexTheme

        settings = getsettings()
        if (str(simpleKey.get()) != ""):
            settings["SimpleSym"] = str(simpleKey.get())


        filename = "settings.json"
        filepath = Path(__file__).resolve().parent/filename

        with open(filepath, "w") as jsonFile:
            json.dump(settings, jsonFile)
        jsonFile.close()

        complexTheme = complexPicker.get()


    def resetsettings():
        filename = "settings.json"
        filepath = Path(__file__).resolve().parent/filename

        filename1 = "materials\defaultsettings.json"
        filepath1 = Path(__file__).resolve().parent/filename1

        data = {}

        with open(filepath1, "r") as jsonFile:
            data = json.load(jsonFile)
        jsonFile.close()


        with open(filepath, "w") as jsonFile:
            json.dump(data, jsonFile)
        jsonFile.close()


    saveButton = customtkinter.CTkButton(master=menu, text="Save", command=save)
    saveButton.grid(row=3,column=0,pady=10)

    resetButton = customtkinter.CTkButton(master=menu, text="Reset", command=resetsettings)
    resetButton.grid(row=4,column=0,pady=10)



def stmenustart():
    settingsmenu()



def mainmenu():

    #---|---|---
    #img|   |set <Maybe Make Graphic
    #---|---|---
    #   |st2|
    #---|---|---
    #   |gen|    <Maybe Make Graphic
    #---|---|---

    


    



    valuesFrame = customtkinter.CTkFrame(master=root)





    contrastFrame = customtkinter.CTkFrame(master=root)

    def cvalupdate(*args):
        contrastvalue.configure(text="Contrast: " + str(contrast.get()))

    contrast = customtkinter.CTkSlider(master=contrastFrame, from_=0, to=256, number_of_steps=256, width=256, command=cvalupdate)
    contrast.set(128)

    contrastvalue = customtkinter.CTkLabel(master=contrastFrame, text="Contrast: " + str(contrast.get()))

    contrast.grid(row=1,column=0)
    contrastvalue.grid(row=2,column=0)

    contrastFrame.grid(row=1,column=1, padx=10,pady=10)





    invertVal = tkinter.BooleanVar()
    invertBox = customtkinter.CTkCheckBox(master=valuesFrame, text="Invert Output", variable=invertVal, onvalue=True, offvalue=False)

    invertBox.grid(row=1,column=1, padx=10)

    modeBox = customtkinter.CTkOptionMenu(master=valuesFrame, values=["Simple","Compressed","Complex"])
    modeBox.grid(row=1,column=2, padx=10)









    cordsFrame = customtkinter.CTkFrame(master=valuesFrame)

    leftParenthesis = customtkinter.CTkLabel(master=cordsFrame, text="(", width=10)
    xEntry = customtkinter.CTkEntry(master=cordsFrame, placeholder_text="X", width=50)
    commaLabel = customtkinter.CTkLabel(master=cordsFrame, text=",", width=10)
    yEntry = customtkinter.CTkEntry(master=cordsFrame, placeholder_text="Y", width=50)
    rightParenthesis = customtkinter.CTkLabel(master=cordsFrame, text=")", width=10)

    leftParenthesis.pack(side="left")
    xEntry.pack(side="left")
    commaLabel.pack(side="left")
    yEntry.pack(side="left")
    rightParenthesis.pack(side="left")

    cordsFrame.grid(row=1,column=0)






    valuesFrame.grid(row=2,column=1, padx=20,pady=20)



    helpButton = customtkinter.CTkButton(master=root, text="Help!", width=15, height=15, command=helpmenu)
    helpButton.grid(row=4,column=2)

    def symbolmanager(modeName):
        global complexTheme
        settings = getsettings()

        if modeName == "Simple":
            return list(settings["SimpleSym"])
        if modeName == "Compressed":
            return ["Braille"]
        if modeName == "Complex":
            return list(settings["ComplexThemes"][complexTheme])
            #return [".",";","/","$","#"]

    def updatecords():
        global cords

        try:
            x = int(xEntry.get())
            y = int(yEntry.get())
        except:
            x = 0
            y = 0

        if(x != 0 or y != 0):
            cords = [x,y]
        else:
            cords = [0,0]
        


    def startconvert():
        global selectedImage
        global cords
        global loadingBar
        #loadingBar.set(value=0)
        updatecords()
        if (selectedImage != ""):
            mainimageconverter(str(selectedImage), list(cords), bool(invertVal.get()), int(contrast.get()), symbolmanager(modeBox.get()), modeBox.get(), False)
            #First img location
            #Then final dimensions
            #Invert
            #Sensitivity
            #Symbols used, use first for the normal ones, then use 5 for complex maybe more?!
    PATH = os.path.dirname(os.path.realpath(__file__))

    #PUT THIS HERE CAUSE I JUST WANA LAUCH 3.0 AND TOO LAZY TO GET PATH UP THERE
    

    imgSelectIcon = customtkinter.CTkImage(light_image=Image.open(PATH + "/materials/image_icon.png"))

    imgSelectButton = customtkinter.CTkButton(master=root, text="",width=50, height=50, image=imgSelectIcon,command=selectimage)
    imgSelectButton.grid(row=0, column=0, pady=10, padx=10)




    startConvertButton = customtkinter.CTkButton(master=root,text="Convert Image",command=startconvert)
    startConvertButton.grid(row=3, column=1)

    

    
    settingsIcon = customtkinter.CTkImage(light_image=Image.open(PATH + "/materials/settings_icon.png"))

    settingsButton = customtkinter.CTkButton(master=root, text="",width=50, height=50, image=settingsIcon ,command=stmenustart)
    settingsButton.grid(row=0, column=2, pady=10, padx=10)

    #barFrame = customtkinter.CTkFrame()
    #loadingBarLabel = customtkinter.CTkLabel(master=barFrame, text=("Progress Bar"))
    #loadingBarLabel.pack()

    #global loadingBar

    #loadingBar = customtkinter.CTkProgressBar(master=barFrame)
    #loadingBar.set(value=0)
    #loadingBar.pack()

    #barFrame.grid(row=0,column=1)

        


#json["Key"]["Subkey"]

mainmenu()
#mainimageconverter("file", [5,4], True, 128, ["symbols light  to dark or first for just plain"], 1, True)

root.mainloop()


