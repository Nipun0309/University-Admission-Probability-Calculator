import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import os
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
## ================================================================
# obtaining path of the GUI folder
my_path = os.path.abspath(os.path.dirname(__file__))
drop_GUI_path = os.path.normpath(my_path + os.sep + os.pardir)
# optaining path of backend folder
backend_path = (drop_GUI_path +'/backend')
## ================================================================
# Setting the aesthetics of the Home page
LabelFont = tkfont.Font(family='Times', size=16)
ButtonFont = tkfont.Font(family='Times', size=12)
## ================================================================
# Getting the list of colleges available
coll = []
for r, d, f in os.walk(backend_path + '/College Data'):
    coll.append(d)
colleges = coll[0]
## ================================================================
# Boolean variable is created having the default value of false
# that would later be utilized by method on_closing() based on which the message
# confirm and close the application might be displayed

QuitApplication = tk.BooleanVar()

## ================================================================
# Default value for the TestType and ScoreType chosen is set so as to avoid
# error of moving to the next window without choosing any of the values
Testtype = tk.StringVar()
Testtype.set("SAT")
Scoretype = tk.StringVar()
Scoretype.set("IB")
# Default value for the College chosen is set so as to avoid
# error of moving to the next window without choosing any of the values
CollegeChoice = tk.StringVar()
CollegeChoice.set(colleges[0])
## ================================================================
# Combo box is created so as to choose the College
label1 = tk.Label(text="Choose the College", font=LabelFont)
label1.grid(row=2, column=0, pady=20)
collegelist = ttk.Combobox(state="readonly", textvariable=CollegeChoice, values=coll[0], width=30)
collegelist.grid(row=2, column=1, pady=10)
## ================================================================
# Radio button is created so as to choose Standardized test type
label2 = tk.Label(text="Choose Type of Standardized Test", font=LabelFont)
label2.grid(row=3, column=0, padx=10, pady=20)
Radiobutton(text="SAT", variable=Testtype, value="SAT").grid(row=3, column=1)
Radiobutton(text="ACT", variable=Testtype, value="ACT").grid(row=3, column=2)
## ================================================================
# Radio button is created so as to choose high school score type
# The text for one of the radio button is set to Percentage while the value of that is set to GPA
# because ultimzately the client would like to use percentage to calculate the probability. However,
# since the data available was for GPA, the Percentage score entered in the next window, if chosen, would
# be converted to GPA as the optimized weights are calculated for GPA
label3 = tk.Label(text="Choose High School Score Type", font=LabelFont)
label3.grid(row=4, column=0, pady=20, padx=10)
Radiobutton(text="IB", variable=Scoretype, value="IB").grid(row=4, column=1)
Radiobutton(text="Percentage", variable=Scoretype, value="GPA").grid(row=4, column=2)
## ================================================================
# Calculate button is created that would based on the client's input would open the appropriate
# window and close the Home Page window
Calculate = tk.Button(text="Click to Proceed", height=1, width=14, command=root.destroy, font=ButtonFont)
Calculate.grid(row=7, column=1, pady=20)
## ================================================================
# Creating method that would quit the application in case the close button
# is clicked
def on_closing():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        root.destroy()
        QuitApplication.set(True)

root.protocol('WM_DELETE_WINDOW', on_closing)
## ================================================================
root.mainloop()
