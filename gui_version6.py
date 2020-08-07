'''
SOFTWARE DEVELOPMENT PROJECT
Client Search & Filtering Utility - GUI Module

Made by Gerard 12SDA
Started on 16/07/2020

Naming Convention - CamelCase

Module Description
This module creates the main GUI elements for the database searching and filtering utility.
It also includes the functionality of the GUI elements such as closing preservation and creating/editing
custom filters.

This Uses
- database_functionality.py
'''

#--------------------------------------------------------------------------------------------------------------------------------------------

#WINDOW CONFIGURATION + IMPORTS



#imports all required libraries
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

#imports project modules
import database_functionality as database

root = Tk() #sets up main window
root.geometry("540x960")    #sets main window size
root.title("Database Filtering Solution")   #sets main window title
root.wm_iconbitmap("data/images/icon.ico")  #sets icon of the main window
root.configure(bg="#333333") #sets the background colour of the main window
root.resizable(width=False, height=False)   #disables the ability to resize the window

#function to clear text files to be able to be re-written to
def deleteContent(pfile): 
    pfile.seek(0)
    pfile.truncate()



#--------------------------------------------------------------------------------------------------------------------------------------------

#MENU BAR CODE



#Creates the Menu Bar Frame
topCanvas = Frame(root, width=540, height=80, bg='#5B5B5B', bd=0, highlightthickness=0, relief='flat')
topCanvas.pack() 

searchButton = Button(topCanvas, width=15, text="Search", font=("helevetica",9),bd=0, highlightthickness=0, relief='flat')
searchButton.place(x=385,y=49)

#Creates the main search entry box
searchEntry = Entry(topCanvas, fg='#333333', bg='#5B5B5B',width=60)
searchEntry.place(x=10,y=50)
searchEntry.insert(END, "Enter Search Term",)  
searchEntry.configure(state=DISABLED)   #sets default state of the entry 

#function to remove placeholder text when clicked on
def searchClick(event):
    searchEntry.configure(state=NORMAL) #changes entry state to allow entry
    searchEntry.delete(0, END)  #clears entry box

searchEntry.bind('<Button-1>', searchClick) #binds the search entry to an event

profileImage = PhotoImage(file='data/images/profile_icon.png')  #imports the profile_icon image
profileButton = Label(topCanvas,image=profileImage, bd=0, highlightthickness=0, relief='flat')  #sets the image to a label (to be changed to link users salesforce profile in the far futrue)
profileButton.place(x=500,y=1)  

backLabel = Label(topCanvas, text="<-- Back To Salesforce Mobile",fg='cyan',bg='#5B5B5B')   #creates a link that goes to the salesforce website
backLabel.place(x=10,y=10)  



#END OF MENU BAR CODE

#--------------------------------------------------------------------------------------------------------------------------------------------

#DATABASE DISPLAY CODE



displayCanvas = Canvas(root, width=540, height=880, bg="#333333")   #creates the main frame (canvas) to hold the GUI related to the database displaying
displayCanvas.pack()    #places the database display canvas

scrollbar = Scrollbar(displayCanvas)    #Creates a scrollbar
scrollbar.pack(side=RIGHT,fill=Y)   #places the scrollbar

#funtion to link all the listboxes to the scrollbar
def setListboxScrollbar(*args):
    myList1.yview(*args)
    myList2.yview(*args)
    myList3.yview(*args)

def OnMouseWheel(event):
    myList1.yview("scroll",event.delta,"units")
    myList2.yview("scroll",event.delta,"units")
    myList3.yview("scroll",event.delta,"units")
    # this prevents default bindings from firing, which
    # would end up scrolling the widget twice
    return "break"
    
#Creates the listboxs that is linked to the scrollbar in order for database displaying
myList1 = Listbox(displayCanvas, width=20, height=100 ,font="helevetica",fg="white",bg="#333333", bd=0, highlightthickness=0, relief='flat', yscrollcommand = scrollbar.set)
myList2 = Listbox(displayCanvas, width=20, height=100 ,font="helevetica",fg="white",bg="#333333", bd=0, highlightthickness=0, relief='flat', yscrollcommand = scrollbar.set) 
myList3 = Listbox(displayCanvas, width=20, height=100 ,font="helevetica",fg="white",bg="#333333", bd=0, highlightthickness=0, relief='flat', yscrollcommand = scrollbar.set)

#places the listboxes
myList1.pack(side=LEFT)
myList2.pack(side=LEFT)
myList3.pack(side=LEFT) 

#connects all the listboxes to the same mousewheel scroll
myList1.bind("<MouseWheel>", OnMouseWheel)
myList2.bind("<MouseWheel>", OnMouseWheel)
myList3.bind("<MouseWheel>", OnMouseWheel)

#Creates a default header for the database display
def drawHeader():
    myList1.insert(END,"")
    myList2.insert(END,"")
    myList3.insert(END,"")
    myList1.insert(END,"Job")
    myList2.insert(END,"Amount")
    myList3.insert(END,"Job Code")
    myList1.insert(END,"")
    myList2.insert(END,"")
    myList3.insert(END,"")

scrollbar.config(command=setListboxScrollbar)  #binds the scrollbar to the listboxes

database.importDatabase()   #Runs to function that imports the database csv 

#Function to add database to the listboxes on the first load/setting back to default
def appendDataToListboxes():
    myList1.delete(0,END)
    myList2.delete(0,END)
    myList3.delete(0,END)
    drawHeader()
    #loops through the main data arrays in order to put the fields into there correct listboxes
    for i in database.jobTitle:
        myList1.insert(END,str(i))
    for i in database.amount:
        myList2.insert(END,str(i))
    for i in database.jobCode:
        myList3.insert(END,str(i))

#Function to add the filtered/sorted/serached database to the listboxes
def filteredOutput():
    myList1.delete(0,END)
    myList2.delete(0,END)
    myList3.delete(0,END)
    drawHeader()
    database.sortDatabase() #sorts the database based on jobTitle
    for record in database.filteredJobTitle:
        myList1.insert(END,str(record))
    for record in database.filteredAmount:
        myList2.insert(END,str(record))
    for record in database.filteredJobCode:
        myList3.insert(END,str(record))

drawHeader()    #Draws the first header of the database
appendDataToListboxes()     #draws the first instance of the database

#Function that gathers the search term in order to send over to the other module
def search(event):
    term = searchEntry.get()
    #Checks to see if the term is blank, if so applies default display
    if term == "Enter Search Term" or term == "":
        term = ""
        appendDataToListboxes()
    #searches the database based on the search term if it is not blank
    else:    
        database.searchDatabase(term)
        filteredOutput()
searchButton.bind('<Button-1>', search)



#END OF DATABASE DISPLAY CODE

#--------------------------------------------------------------------------------------------------------------------------------------------

#START OF FILTER MENU CODE



filterFrame = Frame(root, width=200, height=350)    #creates the frame that holds the custom filter objects

filterFrameShown = False    #global variable that indicates if the filter menu is open

#Function bound to the filterButton as an event, in order to open/hide the filter menu
def filterMenu(event):  
    global filterFrameShown    #defined variables from the global scope
    if not filterFrameShown:    #checks if the filterFrameShown variable equals false
        filterFrame.place(x=340,y=80)   #places it on the GUI
        filterFrameShown = True     #sets the filterFrameShown variable to true
    else:
        filterFrame.place_forget()  #removes it from the GUI
        filterFrameShown = False    #sets the filterFrameShown variable to false


#Creates the default filter creation menu
customFilterFrame = Frame(root, width=540, height=960,bg='#333333')
customFilterMainFrame = Frame(customFilterFrame,width=340,height=660,bg='#5b5b5b')
customFilterMainFrame.place(x=100,y=150)


#Create a tickbox class which can be applied to multiple boxes
class tickBox():
    def __init__(self,X,Y,ticked): #Takes x,y arguments for its position on screen
        self.ticked = ticked
        #Changes image based on if it is ticked or not
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

    #Method called when the tick state is needed to be set
    def setState(self, s):
        self.ticked = s
        if not self.ticked:
            self.image = "data/images/checkbox_unchecked.png"
        else:
            self.image = "data/images/checkbox_checked.png"
        self.img.config(file=self.image) #Change image to match button's state


PosY2 = 50   #Starting Y value of the tickboxes
tickboxArray = []   #Array to store the 3 tickboxes

#loops 3 times to create tickboxes from the class and store them into the array
for i in range(0,3):     
    t = tickBox(10,PosY2,False)
    tickboxArray.append(t)
    PosY2 += 80

customFilterArray = []  #Creates Array to store all custom filter objects

posY = 15   #Starting Y value of the custom filters 
v = tk.IntVar()    #Variable to link up all the radiobuttons
counter = 0    #Stores total number of the customFilter class

#Create a custom filter class which can be applied to multiple custom filters
class customFilter():
    def __init__(self,Y,name,lineN,tickState):
        global v
        self.id = lineN
        self.radioButton = Radiobutton(filterFrame, variable=v, value=self.id, width=4, command=lambda: database.filterDatabase(self.id))
        self.radioButton.place(y=Y)
        self.name = tk.StringVar()
        self.name.set(name)
        self.tickboxStates = tickState
        self.customFilterButton = Button(filterFrame,textvariable=self.name, width=20, height=1,bd=0,fg="white", highlightthickness=0, relief='flat', bg="#5B5B5B", command=lambda: openFilterMenu(self.id))
        self.customFilterButton.place(x=40,y=Y)

    def delete(self):
        self.customFilterButton.destroy()
        self.radioButton.destroy()


defaultNameCounter = 0
def loadCustomFilter():
    global posY, counter, defaultNameCounter
    filterAttributes = []
    tickboxAttributes = []
    attributes = open("data/customfilterattributes.txt","r+")
    filtervalues = open("data/filtervalues.txt","r+")
    filterAttributes = attributes.readlines()
    tickboxAttributes = filtervalues.readlines()
    counter = len(filterAttributes)
    for i in filterAttributes:
        arrOutputTickboxStates = []
        data = tickboxAttributes[filterAttributes.index(i)].split(",")
        for j in data:
            j = j.replace("\n","")
            if j == "True":
                j = True
            elif j == "False":
                j = False
            arrOutputTickboxStates.append(j)
        content = i.split(",")
        if content[0].count("Custom Filter") != 0:
            defaultNameCounter += 1
        filterWidget = customFilter(posY,content[0],content[1],arrOutputTickboxStates)
        posY += 40
        customFilterArray.append(filterWidget)
    attributes.close()
    filtervalues.close()
loadCustomFilter()

filterImage = PhotoImage(file='data/images/filter_button.png')
filterButton = Label(topCanvas, image=filterImage, bd=0, highlightthickness=0, relief='flat')
filterButton.bind("<Button-1>", filterMenu)
filterButton.place(x=500,y=40)


filternameEntry = Entry(customFilterMainFrame,width=42)
filternameEntry.place(x=40,y=10)
filternameEntry.insert(END, "Enter Custom Filter Name (Optional)")
filternameEntry.configure(state=DISABLED)
def filternameFill(event):
    filternameEntry.configure(state=NORMAL)
def filternameClick(event):
    filternameEntry.configure(state=NORMAL)
    filternameEntry.delete(0, END)


def saveFilterAttributes():
    attributes = open("data/customfilterattributes.txt","r+")
    filtervalues = open("data/filtervalues.txt","r+")
    deleteContent(filtervalues)
    deleteContent(attributes)
    for objFilter in customFilterArray:
        attributes.write(objFilter.name.get() + "," + str(objFilter.id).strip())
        attributes.write("\n")
        output = ""
        for i in range(0,3):
            if i < 2:
                filtervalues.write(str(objFilter.tickboxStates[i])+",")
            else:
                filtervalues.write(str(objFilter.tickboxStates[i])+"\n")
    attributes.close()
    filtervalues.close()



tickboxStates = [False,False,False]
def createNewCustomFilter():
    global posY, counter, defaultNameCounter, tickboxStates    #defined variables from the global scope
    name = filternameEntry.get()
    if name != "Enter Custom Filter Name (Optional)" or name == "":
        if len(name) > 20:
            messagebox.showwarning(title="Warning", message="The Length of The Custom Filter Cannot Be Longer Than 20")
            return 
    else:
        if defaultNameCounter == 0:
            name = "Custom Filter"
            defaultNameCounter += 1
        else:
            name = "Custom Filter" + " " + str(defaultNameCounter)
            defaultNameCounter += 1

    tickboxStates = []
    for tickbox in tickboxArray:
        tickboxStates.append(tickbox.ticked)
        
    if posY < 295: 
        filterWidget = customFilter(posY,name,counter,tickboxStates)
        tickboxStates = [False,False,False]
        customFilterArray.append(filterWidget)
        posY += 40
        counter += 1
        
def setCustomFilter(event):
    createNewCustomFilter()
    name = filternameEntry.get()
    if len(name) > 20:
        return
    saveFilterValues(-1)
    saveFilterAttributes()
    removeFilterMenu()
    filternameEntry.configure(state=DISABLED)

def saveCustomFilter(event, i):
    saveFilterValues(i)
    name = filternameEntry.get()
    if len(name) > 20:
        return
    saveFilterAttributes()
    removeFilterMenu()
    cancelBtn.place_forget()
    filternameEntry.configure(state=DISABLED)

def cancelFilterMenu(event):
    filternameEntry.configure(state=DISABLED)
    customFilterFrame.place_forget()


def deleteCustomFilter(event):
    global counter, v, posY, defaultNameCounter    #defined variables from the global scope
    filterAttributes = []
    tickboxAttributes = []
    attributes = open("data/customfilterattributes.txt","r+")
    filtervalues = open("data/filtervalues.txt","r+")
    filterAttributes = attributes.readlines()
    tickboxAttributes = filtervalues.readlines()
    answer = messagebox.askquestion('Warning','Are You Sure You Want To Remove?')
    if answer == 'yes':
        deleteContent(attributes)
        deleteContent(filtervalues)
        for objFilter in customFilterArray:
            if objFilter.id == currentClickedFilter:
                if objFilter.name.get().count("Custom Filter") != 0:
                    defaultNameCounter -= 1
                tickboxAttributes.pop(customFilterArray.index(objFilter))
                filterAttributes.pop(customFilterArray.index(objFilter))
                customFilterArray.pop(customFilterArray.index(objFilter))
                objFilter.delete()
                counter -= 1
        newIdCounter = 0
        for objFilter in customFilterArray:
            objFilter.id = newIdCounter
            newIdCounter += 1
            attributes.write(objFilter.name.get() + "," + str(objFilter.id) + "\n")
        filtervalues.writelines(tickboxAttributes)
        for objFilter in customFilterArray:
            objFilter.delete()
        posY = 15
        for objFilter in customFilterArray:
            objFilter.radioButton = Radiobutton(filterFrame, variable=v, value=objFilter.id, width=4, command=lambda: database.filterDatabase(objFilter.id))
            objFilter.radioButton.place(y=posY)
            objFilter.customFilterButton = Button(filterFrame,textvariable=objFilter.name, width=20, height=1,bd=0,fg="white", highlightthickness=0, relief='flat', bg="#5B5B5B", command=lambda: openFilterMenu(objFilter.id))
            objFilter.customFilterButton.place(x=40,y=posY)
            posY += 40
        cancelBtn.place_forget()
        customFilterFrame.place_forget()
        filternameEntry.configure(state=DISABLED)
    attributes.close()
    filtervalues.close()

#Creates the Create/Save button
btnText = tk.StringVar()     #text variable to change between create/save
btnText.set("Create")
closeFilterButton = Button(customFilterMainFrame,textvariable=btnText,width=20)
closeFilterButton.bind("<Button-1>", setCustomFilter)   #binds the button to specific create filter function
closeFilterButton.place(x=10,y=620)

#Creates the Remove/Cancel button
btnText2 = tk.StringVar()   #text variable to change between remove/cancel
btnText2.set("Cancel")
removeFilterButton = Button(customFilterMainFrame,textvariable=btnText2,width=20)
removeFilterButton.bind("<Button-1>", cancelFilterMenu)    #binds the button to specific cancel filter function
removeFilterButton.place(x=180,y=620)


#Creates the menu option on click of the createFilterButton
def createFilterMenu():
    global createFilterButton, btnText, btnText2    #defined variables from the global scope
    
    if posY < 295:
        customFilterFrame.place(x=0,y=0)
        btnText.set("Create")
        btnText2.set("Cancel")
        closeFilterButton.bind("<Button-1>", setCustomFilter)
        removeFilterButton.bind("<Button-1>", cancelFilterMenu)
        for tickbox in tickboxArray:
            tickbox.setState(False)
        filternameEntry.configure(state=NORMAL)
        filternameEntry.delete(0, END)
        filternameEntry.insert(END, "Enter Custom Filter Name (Optional)")
        filternameEntry.configure(state=DISABLED)
        filternameEntry.bind('<Button-1>', filternameClick)
    else:
        messagebox.showwarning(title="Warning", message="You can have no more than 7 custom filters.")
    

def saveFilterValues(fId):
    global tickboxStates    #defined variables from the global scope
    name = filternameEntry.get()
    if fId != -1:
        if len(name) > 20:
            messagebox.showwarning(title="Warning", message="The Length of The Custom Filter Cannot Be Longer Than 20")
            return
    for objFilter in customFilterArray:
        if objFilter.id == fId:
            tickboxStates = []
            for tickbox in tickboxArray:
                tickboxStates.append(tickbox.ticked)
            objFilter.tickboxStates = tickboxStates
            tickboxStates = [False,False,False]
            objFilter.name.set(name)

#Creates the button for creating custom filters
createFilterButton = Button(filterFrame,text="Create New Custom Filter", command=createFilterMenu,width=21,height=1)
createFilterButton.place(x=21,y=300)

#Function to hide the filter menu
def removeFilterMenu():
    filternameEntry.configure(state=DISABLED)
    customFilterFrame.place_forget()
    cancelBtn.place_forget()

#Creates the labels that dictate what each tickbox will filter
jobTitleLabel = Label(customFilterMainFrame, text="Sort by Job Title")  #creates a label that indicates that the tickbox sorts by job title
jobTitleLabel.place(x=60,y=60)  
amountLabel = Label(customFilterMainFrame, text="Sort by Job Title")   #creates a label that indicates that the tickbox sorts by amount
amountLabel.place(x=60,y=140)   
jobCodeLabel = Label(customFilterMainFrame, text="Sort by Job Code")    #creates a label that indicates that the tickbox sorts by job code
jobCodeLabel.place(x=60,y=220)  

#Creates a cancel button that appears only when editing a custom filter
cancelBtn = Button(customFilterMainFrame, text="Cancel", width=20, command=removeFilterMenu)

currentClickedFilter = -1  #Varaible that indicates the id of the current clicked filter, defaults at -1 because 0 is a possible id

#Function that opens a custom filter for editing, parses in the the id of the clicked filter
def openFilterMenu(filterID):
    global createFilterButton, btnText, currentClickedFilter    #defined variables from the global scope
    cancelBtn.place(x=90,y=580)
    name = ""
    currentClickedFilter = filterID
    btnText.set("Save")
    btnText2.set("Remove")
    closeFilterButton.bind("<Button-1>", lambda event, arg=filterID: saveCustomFilter(event, arg))
    removeFilterButton.bind("<Button-1>", deleteCustomFilter)
    
    for objFilter in customFilterArray:
        if objFilter.id == currentClickedFilter:
            for tickbox in tickboxArray:
                tickbox.setState(bool(objFilter.tickboxStates[tickboxArray.index(tickbox)]))
            name = objFilter.name.get()
            
    filternameEntry.configure(state=NORMAL)
    filternameEntry.delete(0, END)
    filternameEntry.insert(END, name)
    filternameEntry.configure(state=DISABLED)
    filternameEntry.bind('<Button-1>', filternameFill)
    customFilterFrame.place(x=0,y=0)

root.mainloop()


    
#END OF FILTER MENU CODE

#--------------------------------------------------------------------------------------------------------------------------------------------


