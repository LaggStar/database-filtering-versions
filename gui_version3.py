'''
SOFTWARE DEVELOPMENT PROJECT
Client Search & Filtering Utility - GUI Module

Made by Gerard 12SDA
Started on 16/07/2020


'''

#------------------------------------------------------

#WINDOW CONFIGURATION + IMPORTS

from tkinter import *
import tkinter as tk
from tkinter import messagebox


root = Tk()
root.geometry("540x960")
root.title("Database Filtering Solution")
root.wm_iconbitmap("data/images/icon.ico")
root.configure(bg="#333333")
root.resizable(width=False, height=False)

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

#------------------------------------------------------

#MENU BAR CODE

#Creates the Menu Bar Frame
topCanvas = Frame(root, width=540, height=80, bg='#5B5B5B', bd=0, highlightthickness=0, relief='flat')
topCanvas.pack()


searchEntry = Entry(topCanvas, fg='#333333', bg='#5B5B5B',width=80)
searchEntry.place(x=10,y=50)
searchEntry.insert(END, "Search",)
searchEntry.configure(state=DISABLED)

def searchClick(event):
    searchEntry.configure(state=NORMAL)
    searchEntry.delete(0, END)

searchEntry.bind('<Button-1>', searchClick)

profileImage = PhotoImage(file='data/images/profile_icon.png')
profileButton = Label(topCanvas,image=profileImage, bd=0, highlightthickness=0, relief='flat')
profileButton.place(x=500,y=1)

backLabel = Label(topCanvas, text="<-- Back To Salesforce Mobile",fg='cyan',bg='#5B5B5B')
backLabel.place(x=10,y=10)

#END OF MENU BAR CODE

#------------------------------------------------------

#DATABASE DISPLAY CODE

displayCanvas = Canvas(root, width=540, height=880, bg="#333333")
displayCanvas.pack()

scrollbar = Scrollbar(displayCanvas)
scrollbar.pack(side=RIGHT,fill=Y)

myList = Listbox(displayCanvas, width=540, height=880 ,bg="#333333", bd=0, highlightthickness=0, relief='flat', yscrollcommand = scrollbar.set)
myList.insert(END, "")
myList.insert(END, "Test")
myList.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = myList.yview )

#END OF DATABASE DISPLAY CODE

#------------------------------------------------------

#START OF FILTER MENU CODE

filterFrame = Frame(root, width=200, height=350)
filterFrameShown = False

def filterMenu(event):
   global filterFrameShown
   if not filterFrameShown:
      filterFrame.place(x=340,y=80)
      filterFrameShown = True
   else:
      filterFrame.place_forget()
      filterFrameShown = False

filterImage = PhotoImage(file='data/images/filter_button.png')
filterButton = Label(topCanvas, image=filterImage, bd=0, highlightthickness=0, relief='flat')
filterButton.bind("<Button-1>", filterMenu)
filterButton.place(x=500,y=40)

#Creates the default filter creation menu
customFilterFrame = Frame(root, width=540, height=960,bg='#333333')
customFilterMainFrame = Frame(customFilterFrame,width=340,height=660,bg='#5b5b5b')
customFilterMainFrame.place(x=100,y=150)

posY = 15
v = tk.IntVar()
counter = 0
idCounter = 0
class customFilter():
    def __init__(self,Y,name,myID):
        global v
        self.id = myID
        self.radioButton = Radiobutton(filterFrame, variable=v, value=self.id, width=4)
        self.radioButton.place(y=Y)
        self.name = tk.StringVar()
        self.name.set(name)
        self.customFilterButton = Button(filterFrame,textvariable=self.name, width=20, height=1,bd=0,fg="white", highlightthickness=0, relief='flat', bg="#5B5B5B", command=lambda: openFilterMenu(self.id))
        self.customFilterButton.place(x=40,y=Y)

    def delete(self):
        self.customFilterButton.destroy()
        self.radioButton.destroy()
      

#Create a tickbox class which can be applied to multiple boxes
class tickBox():
    def __init__(self,X,Y,ticked): #Takes x,y arguments for its position on screen
        self.ticked = ticked
        if self.ticked:
            self.image = "data/images/checkbox_checked.png"
        else:
            self.image = "data/images/checkbox_unchecked.png"

        self.img = PhotoImage(file=self.image)
        self.btn = Button(customFilterMainFrame, image=self.img,bd=0,highlightthickness=0, command=self.changeState)
        self.btn.place(x=X,y=Y)

    #Method called when tick button is clicked
    def changeState(self):
        if not self.ticked:
            self.ticked = True
            self.image = "data/images/checkbox_checked.png"
        else:
            self.ticked = False
            self.image = "data/images/checkbox_unchecked.png"

        self.img.config(file=self.image) #Change image to match button's state

    def setState(self, s):
        self.ticked = s
        if not self.ticked:
            self.image = "data/images/checkbox_unchecked.png"
        else:
            self.image = "data/images/checkbox_checked.png"
        self.img.config(file=self.image) #Change image to match button's state


        
filternameEntry = Entry(customFilterMainFrame,width=42)
filternameEntry.place(x=40,y=10)
filternameEntry.insert(END, "Enter Custom Filter Name (Optional)",)
filternameEntry.configure(state=DISABLED)
def filternameClick(event):
    filternameEntry.configure(state=NORMAL)
    filternameEntry.delete(0, END)
filternameEntry.bind('<Button-1>', filternameClick)

defaultNameCounter = 0
customFilterArray = []

def createNewCustomFilter():
    global posY
    global counter
    global defaultNameCounter
    global idCounter
    name = filternameEntry.get()
    if name != "Enter Custom Filter Name (Optional)":
        name = name
    else:
        if defaultNameCounter == 0:
            name = "Custom Filter"
            defaultNameCounter += 1
        else:
            name = "Custom Filter" + " " + str(defaultNameCounter)
            defaultNameCounter += 1
    for i in tickboxArray:
        i.setState(False)
    if posY < 295: 
        filterWidget = customFilter(posY,name,idCounter)
        customFilterArray.append(filterWidget)
        filternameEntry.delete(0, END)
        filternameEntry.insert(END, "Enter Custom Filter Name (Optional)",)
        filternameEntry.configure(state=DISABLED)
        posY += 40
        counter += 1
        idCounter += 1
        
def setCustomFilter(event):
    saveFilterValues(-1)
    createNewCustomFilter()
    removeFilterMenu()

def saveCustomFilter(event, i):
    saveFilterValues(i)
    removeFilterMenu()

def cancelFilterMenu(event):
    customFilterFrame.place_forget()

def deleteCustomFilter(event):
    global counter
    global v
    global posY
    answer = messagebox.askquestion('Warning','Are You Sure You Want To Remove?')
    if answer == 'yes':
        for objFilter in customFilterArray:
            if objFilter.id == currentClickedFilter:
                customFilterArray.pop(customFilterArray.index(objFilter))
                objFilter.delete()
                counter -= 1
        for objFilter in customFilterArray:
            objFilter.delete()
        posY = 15
        for objFilter in customFilterArray:
            objFilter.radioButton = Radiobutton(filterFrame, variable=v, value=objFilter.id, width=4)
            objFilter.radioButton.place(y=posY)
            objFilter.customFilterButton = Button(filterFrame,textvariable=objFilter.name, width=20, height=1,bd=0,fg="white", highlightthickness=0, relief='flat', bg="#5B5B5B", command=lambda: openFilterMenu(objFilter.id))
            objFilter.customFilterButton.place(x=40,y=posY)
            posY += 40
        customFilterFrame.place_forget()
    
btnText = tk.StringVar()
btnText.set("Create")
closeFilterButton = Button(customFilterMainFrame,textvariable=btnText,width=20)
closeFilterButton.bind("<Button-1>", setCustomFilter)
closeFilterButton.place(x=10,y=620)

btnText2 = tk.StringVar()
btnText2.set("Cancel")
removeFilterButton = Button(customFilterMainFrame,textvariable=btnText2,width=20)
removeFilterButton.bind("<Button-1>", cancelFilterMenu)
removeFilterButton.place(x=180,y=620)


def createFilterMenu():
    global createFilterButton
    global btnText
    global btnText2
    
    if posY < 295:
        customFilterFrame.place(x=0,y=0)
        btnText.set("Create")
        btnText2.set("Cancel")
        closeFilterButton.bind("<Button-1>", setCustomFilter)
        removeFilterButton.bind("<Button-1>", cancelFilterMenu)
        for i in tickboxArray:
            i.setState(False)
    else:
        messagebox.showwarning(title="Warning", message="You can have no more than 7 custom filters.")

lines = []
def saveFilterValues(fID):
    filterValues = open("data/filtervalues.txt","r+")
    idNum = open("data/idnumber.txt","r+")
    deleteContent(filterValues)
    deleteContent(idNum)
    idNum.write(str(idCounter))
    
    if fID == -1:
        output = ""
        for j in tickboxArray:
            if tickboxArray.index(j) < len(tickboxArray)-1:
                output = output + str(j.ticked)+","
            else:
                output = output + str(j.ticked)+"\n"
        lines.append(output)
    else:
        lines[fID] = str(tickboxArray[0].ticked) + "," + str(tickboxArray[1].ticked) + "," + str(tickboxArray[2].ticked) + "\n"
    filterValues.writelines(lines)
    filterValues.close()
    idNum.close()

def removeFilterMenu():
    customFilterFrame.place_forget()

createFilterButton = Button(filterFrame,text="Create New Custom Filter", command=createFilterMenu,width=21,height=1)
createFilterButton.place(x=21,y=300)
    
PosY2 = 50
tickboxArray = []

for i in range(0,3):
    t = tickBox(10,PosY2,False)
    tickboxArray.append(t)
    PosY2 += 80


jobTitleLabel = Label(customFilterMainFrame, text="Sort by Job Title")
jobTitleLabel.place(x=60,y=60)
amountLabel = Label(customFilterMainFrame, text="Sort by Amount")
amountLabel.place(x=60,y=140)
jobCodeLabel = Label(customFilterMainFrame, text="Sort by Job Code")
jobCodeLabel.place(x=60,y=220)

currentClickedFilter = -1
def openFilterMenu(filterID):
    global createFilterButton
    global btnText
    global currentClickedFilter
    name = ""
    currentClickedFilter = filterID
    btnText.set("Save")
    btnText2.set("Remove")
    closeFilterButton.bind("<Button-1>", lambda event, arg=filterID: saveCustomFilter(event, arg))
    removeFilterButton.bind("<Button-1>", deleteCustomFilter)
    
    filterValues = open("data/filtervalues.txt","r")
    lines = filterValues.readlines()
    values = lines[filterID].split(",")
    values[2] = values[2].replace("\n", "")
    for i in range(0,3):
        if values[i] == "True":
            out = True
        else:
            out = False
        tickboxArray[i].setState(out)

    for i in customFilterArray:
        if i.id == currentClickedFilter:
            name = i.name
    filternameEntry.delete(0, END)
    filternameEntry.insert(END, str(name))
    filternameEntry.configure(state=DISABLED)
    customFilterFrame.place(x=0,y=0)
    filterValues.close()


   
#END OF FILTER MENU CODE

#------------------------------------------------------

root.mainloop()
