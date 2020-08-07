from tkinter import *

root = Tk()
root.geometry("540x960")
root.title("Database Filtering Solution")
root.wm_iconbitmap("icon.ico")
root.configure(bg="#333333")
root.resizable(width=False, height=False)



topCanvas = Canvas(root, width=540, height=80, bg='#5B5B5B', bd=0, highlightthickness=0, relief='flat')
topCanvas.pack()

searchEntry = Entry(topCanvas, fg='#333333', bg='#5B5B5B')
searchEntry.place(x=10,y=10)
searchEntry.insert(END, "Search",)
searchEntry.configure(state=DISABLED)

def on_click(event):
    searchEntry.configure(state=NORMAL)
    searchEntry.delete(0, END)

    #make the callback only work once
    searchEntry.unbind('<Button-1>', on_click_id)

on_click_id = searchEntry.bind('<Button-1>', on_click)

profileButton = Button(topCanvas, width=4, height=2)
profileButton.place(x=200,y=0)

def customFilterMenu(event):
   print("Opens filter menu")

img1 = PhotoImage(file='img1.png')
filterButton = Label(topCanvas, image=img1, bd=0, highlightthickness=0, relief='flat')
filterButton.bind("<Button-1>", customFilterMenu)
filterButton.place(x=500,y=40)

backLabel = Label(topCanvas, text="<-- Back To Salesforce Mobile",bg='#5B5B5B')
backLabel.place(x=10,y=20)



displayCanvas = Canvas(root, width=540, height=880, bg="#333333")
displayCanvas.pack()

scrollbar = Scrollbar(displayCanvas)
scrollbar.pack(side=RIGHT,fill=Y)

myList = Listbox(displayCanvas, width=540, height=880 ,bg="#333333", bd=0, highlightthickness=0, relief='flat', yscrollcommand = scrollbar.set)
myList.insert(END, "")
myList.insert(END, "Test")
myList.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = myList.yview )




root.mainloop()
