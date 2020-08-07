'''

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


searchEntry = Entry(topCanvas, fg='#333333', bg='#5B5B5B')
searchEntry.place(x=10,y=10)
searchEntry.insert(END, "Search",)
searchEntry.configure(state=DISABLED)

def searchClick(event):
    searchEntry.configure(state=NORMAL)
    searchEntry.delete(0, END)

searchEntry.bind('<Button-1>', searchClick)

profileButton = Button(topCanvas, width=4, height=2)
profileButton.place(x=200,y=0)

backLabel = Label(topCanvas, text="<-- Back To Salesforce Mobile",bg='#5B5B5B')
backLabel.place(x=10,y=20)

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
customFilterMainFrame = Frame(customFilterFrame,width=340,height=660)
customFilterMainFrame.place(x=100,y=150)

v = tk.IntVar()

class customFilter():
   def __init__(self,Y):
      global v
      self.radioButton = Radiobutton(filterFrame, variable=v, width=4)
      self.radioButton.place(y=Y)
      self.name = tk.StringVar()
      self.name.set("")
      self.customFilterButton = Button(filterFrame,textvariable=self.name, width=10, height=1,bd=0, highlightthickness=0, relief='flat', bg="#5B5B5B", command=openFilterMenu)
      self.customFilterButton.place(x=40,y=Y)

      

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

    #Method to remove button
    def remove(self):
        try:
            self.btn.destroy()
        except:
            pass



posY = 15
def createNewCustomFilter():
    global posY
    if posY < 295:
        filterWidget = customFilter(posY)
        posY += 40

def createFilterMenu():
    if posY < 295:
        customFilterFrame.place(x=0,y=0)
    else:
        messagebox.showwarning(title="Warning", message="You can have no more than 7 custom filters.")

createFilterButton = Button(filterFrame,text="Create New Custom Filter", command=createFilterMenu,width=21,height=1)
createFilterButton.place(x=21,y=300)
    
def removeFilterMenu():
    customFilterFrame.place_forget()

filternameEntry = Entry(customFilterMainFrame,width=10)
filternameEntry.place(x=40,y=0)
filternameEntry.insert(END, "Enter Custom Filter Name",)
filternameEntry.configure(state=DISABLED)
def filternameClick(event):
    filternameEntry.configure(state=NORMAL)
    filternameEntry.delete(0, END)
filternameEntry.bind('<Button-1>', filternameClick)


PosY2 = 50
for i in range(0,3):
    t = tickBox(10,PosY2,False)
    PosY2 += 80

jobTitleLabel = Label(customFilterMainFrame, text="Sort by Job Title")
jobTitleLabel.place(x=60,y=60)
amountLabel = Label(customFilterMainFrame, text="Sort by Amount")
amountLabel.place(x=60,y=140)
jobCodeLabel = Label(customFilterMainFrame, text="Sort by Job Code")
jobCodeLabel.place(x=60,y=220)


def saveFilterValues():
    filterValues = open("data/filtervalues.txt","r+")

def openFilterMenu():
    print("load in values")

def setCustomFilter():
    saveFilterValues()
    createNewCustomFilter()
    removeFilterMenu()

closeFilterButton = Button(customFilterMainFrame, command=setCustomFilter)
closeFilterButton.place(x=20,y=0)


'''
image = Image.open('data/images/filtermenu_background.jpg')
filterBackground = ImageTk.PhotoImage(image)
createFilterBackground = Canvas(root)
createFilterBackground.place(x=0,y=0)
createFilterBackground.create_image(0,0,image=filterBackground)


def create5Filter():
    customFilterMenu()
'''  
   
#END OF FILTER MENU CODE

#------------------------------------------------------

root.mainloop()
