#import required libraries
import tkinter as tk
import subprocess as sp
import os
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD


def dropFile(event):
    """allows file to be drag and dropped on gui
        additionally creates entry field for the sheet when an xlsx file is used
    Args:
        event (drop file): triggers on the event of a file being dropped
    """
    #sets required variables to global as they will need to be accessed outside the function
    global filePath, sheetLabel, sheetEntry 

    #obtains file path from the event
    filePath = event.data
    #removes { } which can occur when dragging and dropping file from local onedrive folder
    if filePath[0]=="{":
        filePath=filePath[1:-1]
    #displays selected file
    dragdrop.config(text=f"Dropped file:\n{filePath}")
    
    #checks if sheet field already exists by trying to pull the input from it, if no entry exists then sets entry to false
    try:
        exists=sheetEntry.get()
        
    except NameError:
        exists=False
    
    #removes the previous field from the gui if it exists
    if exists!=False:
        sheetEntry.pack_forget()
        sheetLabel.pack_forget()
    
    #checks if the file is xlsx and if so adds new input field for the sheet on which the data for the graph is found (as required by pandas)
    if filePath[-4:]=="xlsx":
        #creates and displays label for the sheet entry field
        sheetLabel = tk.Label(xyframe, text="Sheet:")
        sheetLabel.pack(side='left',pady=5)
        #creates and displays the sheet entry field
        sheetEntry = tk.Entry(xyframe)
        sheetEntry.pack(side='left',pady=5)
        sheetEntry.insert(0, "Sheet1") #placeholder text 
        sheetEntry.config(fg="gray")  #set placeholder text colour
        #bind focusIn and FocusOut functions to entry field to add placeholder txt
        sheetEntry.bind("<FocusIn>", lambda event: onFocusIn(sheetEntry, "Sheet1"))
        sheetEntry.bind("<FocusOut>", lambda event: onFocusOut(sheetEntry, "Sheet1"))

def onFocusIn(entry, placeholderText):
    """Focus on input box
    When an entry field is clicked on clears the placeholder text if it's still there
    """
    if entry.get() == placeholderText:#checks if placeholder text is in textbox
        entry.delete(0, tk.END) #deletes placeholder text
        entry.config(fg="black")  #change text colour to black 

def onFocusOut(entry, placeholderText):
    """Focus off input box
    When an entry field is clicked off of restores the placeholder text if the field is empty
    """
    if entry.get() == "": #checks if the textbox is empty
        entry.insert(0, placeholderText) #adds appropriate placeholder text
        entry.config(fg="grey")  #makes the placeholder text colour grey


def runGraph():
    """runs graph.py to create a plot, passing the user inputs as arguments
    """
    #gets the current working directory of the program
    scriptFolder = os.path.dirname(os.path.realpath(__file__))
    #change the current working directory to the folder of this file the program can call graph.py 
    os.chdir(scriptFolder)
    
    #obtains user inputs from all entry fields
    x=xcolEntry.get()
    y=ycolEntry.get()
    xerr=xerrEntry.get()
    yerr=yerrEntry.get()
    func=fit.get()
    
    #attempts to get input from sheet field but if it does not exist sets sheet var to a blank string
    try:
        sheet=sheetEntry.get()
    except NameError:
        sheet=""

    #attempts to run graph.py
    try:
        sp.run(['python', 'graph.py',filePath,sheet,x,y,xerr,yerr,func], check=True, capture_output=True, text=True)
    
    #if there is an error running graph.py displays it on the gui
    except sp.CalledProcessError as e:
        error.config(text=f"Error running graph.py: \n{e.stderr.strip().split('\n')[-1]}") 
        

#create the main window as a drag and drop enabled window
root = TkinterDnD.Tk()
root.title("Graph Config")


#creates label to display any error to the user in the gui
error = tk.Label(root)
error.pack()

#creates and displays label for the fit drop down menu
fitLabel = tk.Label(root, text="Fit:")
fitLabel.pack()

#Creates drop down menu with option for fittings and defaults to scatter
options = ["Linear", "Scatter", "nth order polynomial"]
fit = ttk.Combobox(root, values=options)
fit.pack(pady=10,padx=10)
fit.set("Scatter") 

#creates frame for the x and y column entry fields
xyframe = tk.Frame(root)
xyframe.pack()

#creates and displays label for the x column entry field
xcolLabel = tk.Label(xyframe, text="x column name:")
xcolLabel.pack(side='left',pady=5)
#creates and displays the x column entry field
xcolEntry = tk.Entry(xyframe)
xcolEntry.pack(side='left',pady=5)
xcolEntry.insert(0, "x") #placeholder text 
xcolEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field to add placeholder txt
xcolEntry.bind("<FocusIn>", lambda event: onFocusIn(xcolEntry, "x"))
xcolEntry.bind("<FocusOut>", lambda event: onFocusOut(xcolEntry, "x"))


#creates and displays label for the y column entry field
ycolLabel = tk.Label(xyframe, text="y column name:")
ycolLabel.pack(side='left',pady=5)
#creates and displays the y column entry field
ycolEntry = tk.Entry(xyframe)
ycolEntry.pack(side='left',pady=5)
ycolEntry.insert(0, "y") #placeholder text 
ycolEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field to add placeholder txt
ycolEntry.bind("<FocusIn>", lambda event: onFocusIn(ycolEntry, "y"))
ycolEntry.bind("<FocusOut>", lambda event: onFocusOut(ycolEntry, "y"))

#creates frame for the error columns entry fields
errframe = tk.Frame(root)
errframe.pack()

#creates and displays label for the x error column entry field
xerrLabel = tk.Label(errframe, text="x error:")
xerrLabel.pack(side='left',pady=5)
#creates and displays the x error column entry field
xerrEntry = tk.Entry(errframe)
xerrEntry.pack(side='left',pady=5)
xerrEntry.insert(0, "xerr") #placeholder text 
xerrEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field to add placeholder txt
xerrEntry.bind("<FocusIn>", lambda event: onFocusIn(xerrEntry, "xerr"))
xerrEntry.bind("<FocusOut>", lambda event: onFocusOut(xerrEntry, "xerr"))


#creates and displays label for the y error column entry field
yerrLabel = tk.Label(errframe, text="y error:")
yerrLabel.pack(side='left',pady=5)
#creates and displays the y error column entry field
yerrEntry = tk.Entry(errframe)
yerrEntry.pack(side='left',pady=5)
yerrEntry.insert(0, "yerr") #placeholder text 
yerrEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field to add placeholder txt
yerrEntry.bind("<FocusIn>", lambda event: onFocusIn(yerrEntry, "yerr"))
yerrEntry.bind("<FocusOut>", lambda event: onFocusOut(yerrEntry, "yerr"))

#creates a drag and drop field for the user to drop a file
dragdrop = tk.Label(root, text="Drag & Drop a csv or xlsx file here", bg="lightgray", width=50, height=10)
dragdrop.pack(pady=50)
dragdrop.drop_target_register(DND_FILES)
dragdrop.dnd_bind("<<Drop>>", dropFile)



#create the create graph button which activates the runGraph function when pressed
graphButton = tk.Button(root, text="Create Graph", command=runGraph)
graphButton.pack(pady=10)



#start the main event loop to display GUI
root.mainloop()
