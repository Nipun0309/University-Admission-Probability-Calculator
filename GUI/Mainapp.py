from joblib import load
import sklearn
from tkinter import *
import tkinter as tk
import numpy as np
import os
from tkinter import ttk
from tkinter import messagebox
import sys
import predict as pr
from datetime import datetime

from tkinter import tix
## ================================================================
# An instantiation (object) of the Home Page is created. By doing so, it is ensured that the Home Page
# and the main page are all created through one python file and executable. The values therefore
# chosen in the Homepage by the user(client) would be accessible to the Main Page based
# on which the appropriate labels and data is set
import Homepage as hp
## ================================================================
from tkinter import font as tkfont
root = tk.Tk()
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
## ================================================================
# Dynamic size of the window is chosen that would therefore have the size based on the
# values chosen by the client in the Home page
root.geometry("")
## ================================================================
# Setting the aesthetics of the Main page
LabelFont = tkfont.Font(family='Times', size=16)
ButtonFont = tkfont.Font(family='Times', size=12)
## ================================================================
# If the user chooses to close the application from Home Page, the Main Page will also get closed
if hp.QuitApplication.get():
    sys.exit()
## ================================================================
# Based on the College Choice, Score type, and Test type chosen by the user in the Home Page,
# the appropriate directory is accessed and files are loaded
MajorDir = (
        hp.backend_path + '/Original College Data/Datasets/' + hp.CollegeChoice.get() + '.csv')
ScalerFile = (
        hp.backend_path + '/Optimized Weights for ' + hp.Scoretype.get() + '/' + hp.CollegeChoice.get() + '/' + hp.Testtype.get() + '/scaler_file.joblib')
Theta1Dir = (
        hp.backend_path + '/Optimized Weights for ' + hp.Scoretype.get() + '/' + hp.CollegeChoice.get() + '/' + hp.Testtype.get() + '/Theta1.csv')
Theta2Dir = (
        hp.backend_path + '/Optimized Weights for ' + hp.Scoretype.get() + '/' + hp.CollegeChoice.get() + '/' + hp.Testtype.get() + '/Theta2.csv')
Features = np.loadtxt(
        hp.backend_path + '/College Data/' + hp.CollegeChoice.get() + '/' + hp.Testtype.get() + '/Featuresdata.csv',
        delimiter=',')
## ================================================================
# No of Features is calculated so as to know whether the college is public or private as
# private colleges do not consider the residency status of the applicant
NoOfFeatures = Features.shape[1]
# Entry widget is created for entering the values of the Test type and Score type chosen by the user
SATScore = tk.Entry()
ACTScore = tk.Entry()
IBScore = tk.Entry()
PercentageScore = tk.Entry()
# The optimized weights Theta1 and Theta2 based on the user's input in the Home page is loaded
Theta1 = np.loadtxt(Theta1Dir, delimiter=',')
Theta2 = np.loadtxt(Theta2Dir, delimiter=',')
# The appropriate list of majors and scaling values are loaded that are based
# on the user's input in the Home page
X = np.loadtxt(MajorDir, delimiter=',', dtype='object', skiprows=0)
scaler = load(ScalerFile)
# Integer variable is created that will hold the appropriate integer equivalent of the major that was
# mapped for each and every major in each college. This will thus be utilized as part of the probability
# calculation
MajorEquivalentVal = tk.IntVar()

## ================================================================
# A callback method is created that will be utilized to check if the values entered are digits
def callback(P):
    if str.isdigit(P):
        return True
    elif P == "":
        return True
    else:
        return False
## ================================================================
## ================================================================
# Following methods are created that will based, on the values chosen in the Home Page and the Main page,
# will perform the appropriate validations, display the appropriate messages,
# and calculate the correct probability
# In case the user has chosen Percentage as Score type in the Home Page, the perecentage entered in the entry
# field will be recalculated to percentage
## ================================================================
def CalcProbwithSATandIB():
    SATValidation = tk.BooleanVar(value=False)
    IBValidation = tk.BooleanVar(value=False)
    if (SATScore.get()).isdigit():
        if (int(SATScore.get()) >= 720) and (int(SATScore.get()) <= 1600) and (int(SATScore.get()) % 10 == 0):
            SATValidation.set(True)
        else:
            messagebox.showerror("Error", "Enter appropriate SAT Score between 720 and 1600")
    elif (SATScore.get() == " ") or ((SATScore.get()).isdigit() == False):
        messagebox.showerror("Error", "Enter appropriate SAT Score between 720 and 1600")
    if (IBScore.get()).isdigit():
        if (int(IBScore.get()) >= 24) and (int(IBScore.get()) <= 42):
            IBValidation.set(True)
        else:
            messagebox.showerror("Error", "Enter IB Predicted Score between 24 and 42")
    elif (IBScore.get() == " ") or ((IBScore.get()).isdigit() == False):
        messagebox.showerror("Error", "Enter IB Predicted Score between 24 and 42")
    if (IBValidation.get() == True) and (SATValidation.get() == True):
        for i in range(len(list1)):
            if MajorChoice.get() == list1[i]:
                MajorEquivalentVal.set((MajEquivalent[i]))
        if NoOfFeatures == 5:
            Prob = np.array([SATScore.get(), IBScore.get(), ResidencyStatus.get(), MajorEquivalentVal.get()])[
                np.newaxis]
            Prob = scaler.transform(Prob)
            probability = float(pr.predict(Theta1, Theta2, Prob)[3])
            message = ("The probability of getting admission into " + hp.CollegeChoice.get() + " is " + str(
                round(probability * 100, 2)) + "%")
            messagebox.showinfo("Probability", message)
        else:
            Prob = np.array([SATScore.get(), IBScore.get(), MajorEquivalentVal.get()])[np.newaxis]
            Prob = scaler.transform(Prob)
            probability = float(pr.predict(Theta1, Theta2, Prob)[3])
            message = ("The probability of getting admission into " + hp.CollegeChoice.get() + " is " + str(
                round(probability * 100, 2)) + "%")
            messagebox.showinfo("Probability", message)

def CalcProbwithACTandIB():
    ACTValidation = tk.BooleanVar(value=False)
    IBValidation = tk.BooleanVar(value=False)
    if (ACTScore.get()).isdigit():
        if (int(ACTScore.get()) >= 15) and (int(ACTScore.get()) <= 36):
            ACTValidation.set(True)
        else:
            messagebox.showerror("Error", "Enter ACT Score between 15 and 36")
    elif (ACTScore.get() == " ") or ((ACTScore.get()).isdigit() == False):
        messagebox.showerror("Error", "Enter ACT Score between 15 and 36")
    if (IBScore.get()).isdigit():
        if (int(IBScore.get()) >= 24) and (int(IBScore.get()) <= 42):
            IBValidation.set(True)
        else:
            messagebox.showerror("Error", "Enter IB Predicted Score between 24 and 42")
    elif (IBScore.get() == " ") or ((IBScore.get()).isdigit() == False):
        messagebox.showerror("Error", "Enter IB Predicted Score between 24 and 42")
    if (IBValidation.get() == True) and (ACTValidation.get() == True):
        for i in range(len(list1)):
            if MajorChoice.get() == list1[i]:
                MajorEquivalentVal.set((MajEquivalent[i]))
        if NoOfFeatures == 5:
            Prob = np.array([ACTScore.get(), IBScore.get(), ResidencyStatus.get(), MajorEquivalentVal.get()])[
                np.newaxis]
            Prob = scaler.transform(Prob)
            probability = float(pr.predict(Theta1, Theta2, Prob)[3])
            message = ("The probability of getting admission into " + hp.CollegeChoice.get() + " is " + str(
                round(probability * 100, 2)) + "%")
            messagebox.showinfo("Probability", message)
            #print(probability)
        else:
            Prob = np.array([ACTScore.get(), IBScore.get(), MajorEquivalentVal.get()])[np.newaxis]
            Prob = scaler.transform(Prob)
            probability = float(pr.predict(Theta1, Theta2, Prob)[3])
            message = ("The probability of getting admission into " + hp.CollegeChoice.get() + " is " + str(
                round(probability * 100, 2)) + "%")
            messagebox.showinfo("Probability", message)
            #print(probability)

def CalcProbwithSATandPercentage():
    SATValidation = tk.BooleanVar(value=False)
    PercentageValidation = tk.BooleanVar(value=False)
    if (SATScore.get()).isdigit():
        if (int(SATScore.get()) >= 720) and (int(SATScore.get()) <= 1600) and (int(SATScore.get()) % 10 == 0):
            SATValidation.set(True)
        else:
            messagebox.showerror("Error", "Enter appropriate SAT Score between 720 and 1600")
    elif (SATScore.get() == " ") or ((SATScore.get()).isdigit() == False):
        messagebox.showerror("Error", "Enter appropriate SAT Score between 720 and 1600")
    if (PercentageScore.get()).isdigit():
        if (int(PercentageScore.get()) >= 40) and (int(PercentageScore.get()) <= 100):
            PercentageValidation.set(True)
        else:
            messagebox.showerror("Error", "Enter Percentage between 40 and 100")
    elif (PercentageScore.get() == " ") or ((PercentageScore.get()).isdigit() == False):
        messagebox.showerror("Error", "Enter Percentage between 40 and 100")
    if (PercentageValidation.get() == True) and (SATValidation.get() == True):
        ## ================================================================
        # Validated percentage will be converted to GPA Score
        PercentagetoGPA = (int(PercentageScore.get()) / 20) - 1
        for i in range(len(list1)):
            if MajorChoice.get() == list1[i]:
                MajorEquivalentVal.set((MajEquivalent[i]))
        if NoOfFeatures == 5:
            Prob = np.array([SATScore.get(), PercentagetoGPA, ResidencyStatus.get(), MajorEquivalentVal.get()])[
                np.newaxis]
            Prob = scaler.transform(Prob)
            probability = float(pr.predict(Theta1, Theta2, Prob)[3])
            message = ("The probability of getting admission into " + hp.CollegeChoice.get() + " is " + str(
                round(probability * 100, 2)) + "%")
            messagebox.showinfo("Probability", message)
        else:
            Prob = np.array([SATScore.get(), PercentagetoGPA, MajorEquivalentVal.get()])[np.newaxis]
            Prob = scaler.transform(Prob)
            probability = float(pr.predict(Theta1, Theta2, Prob)[3])
            message = ("The probability of getting admission into " + hp.CollegeChoice.get() + " is " + str(
                round(probability * 100, 2)) + "%")
            messagebox.showinfo("Probability", message)

def CalcProbwithACTandPercentage():
    ACTValidation = tk.BooleanVar(value=False)
    PercentageValidation = tk.BooleanVar(value=False)
    if (ACTScore.get()).isdigit():
        if (int(ACTScore.get()) >= 15) and (int(ACTScore.get()) <= 36):
            ACTValidation.set(True)
        else:
            messagebox.showerror("Error", "Enter ACT Score between 15 and 36")
    elif (ACTScore.get() == " ") or ((ACTScore.get()).isdigit() == False):
        messagebox.showerror("Error", "Enter ACT Score between 15 and 36")
    if (PercentageScore.get()).isdigit():
        if (int(PercentageScore.get()) >= 40) and (int(PercentageScore.get()) <= 100):
            PercentageValidation.set(True)
        else:
            messagebox.showerror("Error", "Enter Percentage between 40 and 100")
    elif (PercentageScore.get() == " ") or ((PercentageScore.get()).isdigit() == False):
        messagebox.showerror("Error", "Enter Percentage between 40 and 100")
    if (PercentageValidation.get() == True) and (ACTValidation.get() == True):
        ## ================================================================
        # Validated percentage will be converted to GPA Score
        PercentagetoGPA = (int(PercentageScore.get()) / 20) - 1
        for i in range(len(list1)):
            if MajorChoice.get() == list1[i]:
                MajorEquivalentVal.set((MajEquivalent[i]))
        if NoOfFeatures == 5:
            Prob = np.array([ACTScore.get(), PercentagetoGPA, ResidencyStatus.get(), MajorEquivalentVal.get()])[
                np.newaxis]
            Prob = scaler.transform(Prob)
            probability = float(pr.predict(Theta1, Theta2, Prob)[3])
            message = ("The probability of getting admission into " + hp.CollegeChoice.get() + " is " + str(
                round(probability * 100, 2)) + "%")
            messagebox.showinfo("Probability", message)
        else:
            Prob = np.array([ACTScore.get(), PercentagetoGPA, MajorEquivalentVal.get()])[np.newaxis]
            Prob = scaler.transform(Prob)
            probability = float(pr.predict(Theta1, Theta2, Prob)[3])
            message = ("The probability of getting admission into " + hp.CollegeChoice.get() + " is " + str(
                round(probability * 100, 2)) + "%")
            messagebox.showinfo("Probability", message)
## ================================================================

# method is created, a function that will be utilized to create the button Go Back, in case
# the user would like to go back the the Home Page
def method():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# String Varaibles are initialized so as to to store the Major and Residency status that will
# be chosen by the user
MajorChoice = tk.StringVar()
ResidencyStatus = tk.IntVar()
# Residency status is by default set to 9, the integer equivalent mapped to In-state Residency
ResidencyStatus.set(9)
## ================================================================
# This is done to get the the chosen college's list of major's integer equivalent mapped
# to the list of majors
size = X.shape[1]
List = X[:, size - 4]
list2 = X[:, size - 3]
MajEquivalent = np.unique(list2)
list1 = np.unique(List)
Majorlist = list1.tolist()
## ================================================================

## ================================================================
## ================================================================
# Based on the Test type and Score type chosen by the user in the Home Page,
# the appropiate window is created to display the appropriate labels, entry
# widgets.

# Configurations are done to ensure that the values entered in the entry field are limited
# to integer values

# In addition, based on the college chosen, the type of college is detected i.e. public or private,
# using the number of features in the featuresdata file of the college. If the no of features is 5,
# a label and radia button is added to choose the residency status (as it is a public college), else
# it is omitted
## ================================================================
if (hp.Testtype.get() == "SAT") and (hp.Scoretype.get() == "IB"):
    reg = root.register(callback)
    label1 = tk.Label(text="Enter SAT Score", font=LabelFont)
    label1.grid(row=2, column=0, pady=30, padx=10)

    SATScore.grid(row=2, column=1)
    SATScoreTooltip = CreateToolTip(SATScore,'Enter numeric digits only')

    SATScore.config(validate="key",
                    validatecommand=(reg, '%P'))
    label2 = tk.Label(text="Enter your IB Score ( /42)", font=LabelFont)
    label2.grid(row=3, column=0, padx=10, pady=20)

    IBScore.grid(row=3, column=1)
    IBScoreTooltip = CreateToolTip(IBScore, 'Enter numeric digits only')
    IBScore.config(validate="key",
                   validatecommand=(reg, '%P'))
    label3 = tk.Label(text="Choose your Major", font=LabelFont)
    label3.grid(row=4, column=0, padx=10, pady=20)
    Majors = ttk.Combobox(state="readonly", textvariable=MajorChoice, values=Majorlist, width=35)
    Majors.current(0)
    Majors.grid(row=4, column=1)
    if NoOfFeatures == 5:
        label4 = tk.Label(text="Choose Residency Status", font=LabelFont)
        label4.grid(row=5, column=0, pady=20, padx=10)
        Radiobutton(text="In-State", variable=ResidencyStatus, value=9).grid(row=5, column=1)
        Radiobutton(text="Out-of-State", variable=ResidencyStatus, value=10).grid(row=5, column=2)
    Calculate = tk.Button(text="Calculate Chance ", height=1, width=14, font=ButtonFont,
                          command=CalcProbwithSATandIB)
    Calculate.grid(row=6, column=1, pady=10)
    GoBack = tk.Button(text="Click to go back ", height=1, width=14, font=ButtonFont, command=method)
    GoBack.grid(row=6, column=0, pady=10)
if (hp.Testtype.get() == "ACT") and (hp.Scoretype.get() == "IB"):
    reg = root.register(callback)
    label1 = tk.Label(text="Enter ACT Score", font=LabelFont)
    label1.grid(row=2, column=0, pady=30, padx=10)

    ACTScore.grid(row=2, column=1)
    ACTScoreTooltip = CreateToolTip(ACTScore, 'Enter numeric digits only')
    ACTScore.config(validate="key",
                    validatecommand=(reg, '%P'))
    label2 = tk.Label(text="Enter your IB Score ( /42)", font=LabelFont)
    label2.grid(row=3, column=0, padx=10, pady=20)

    IBScore.grid(row=3, column=1)
    IBScoreTooltip = CreateToolTip(IBScore, 'Enter numeric digits only')
    IBScore.config(validate="key",
                    validatecommand=(reg, '%P'))
    label3 = tk.Label(text="Choose your Major", font=LabelFont)
    label3.grid(row=4, column=0, padx=10, pady=20)
    Majors = ttk.Combobox(state="readonly", textvariable=MajorChoice, values=Majorlist, width=35)
    Majors.current(0)
    Majors.grid(row=4, column=1)
    if NoOfFeatures == 5:
        label4 = tk.Label(text="Choose Residency Status", font=LabelFont)
        label4.grid(row=5, column=0, pady=20, padx=10)
        Radiobutton(text="In-State", variable=ResidencyStatus, value=9).grid(row=5, column=1)
        Radiobutton(text="Out-of-State", variable=ResidencyStatus, value=10).grid(row=5, column=2)
    Calculate = tk.Button(text="Calculate Chance ", height=1, width=14, font=ButtonFont,
                          command=CalcProbwithACTandIB)
    Calculate.grid(row=6, column=1, pady=10)
    GoBack = tk.Button(text="Click to go back ", height=1, width=14, font=ButtonFont, command=method)
    GoBack.grid(row=6, column=0, pady=10)
if (hp.Testtype.get() == "SAT") and (hp.Scoretype.get() == "GPA"):
    reg = root.register(callback)
    label1 = tk.Label(text="Enter SAT Score", font=LabelFont)
    label1.grid(row=2, column=0, pady=30, padx=10)

    SATScore.grid(row=2, column=1)
    SATScoreTooltip = CreateToolTip(SATScore, 'Enter numeric digits only')
    SATScore.config(validate="key",
                    validatecommand=(reg, '%P'))
    label2 = tk.Label(text="Enter your Percentage ( /100)", font=LabelFont)
    label2.grid(row=3, column=0, padx=10, pady=20)

    PercentageScore.grid(row=3, column=1)
    PercentageScoreTooltip = CreateToolTip(PercentageScore, 'Enter numeric digits only')
    PercentageScore.config(validate="key",
                    validatecommand=(reg, '%P'))
    label3 = tk.Label(text="Choose your Major", font=LabelFont)
    label3.grid(row=4, column=0, padx=10, pady=20)
    Majors = ttk.Combobox(state="readonly", textvariable=MajorChoice, values=Majorlist, width=35)
    Majors.current(0)
    Majors.grid(row=4, column=1)
    if NoOfFeatures == 5:
        label4 = tk.Label(text="Choose Residency Status", font=LabelFont)
        label4.grid(row=5, column=0, pady=20, padx=10)
        Radiobutton(text="In-State", variable=ResidencyStatus, value=9).grid(row=5, column=1)
        Radiobutton(text="Out-of-State", variable=ResidencyStatus, value=10).grid(row=5, column=2)
    Calculate = tk.Button(text="Calculate Chance ", height=1, width=14, font=ButtonFont,
                          command=CalcProbwithSATandPercentage)
    Calculate.grid(row=6, column=1, pady=10)
    GoBack = tk.Button(text="Click to go back ", height=1, width=14, font=ButtonFont, command=method)
    GoBack.grid(row=6, column=0, pady=10)
if (hp.Testtype.get() == "ACT") and (hp.Scoretype.get() == "GPA"):
    reg = root.register(callback)
    label1 = tk.Label(text="Enter ACT Score", font=LabelFont)
    label1.grid(row=2, column=0, pady=30, padx=10)

    ACTScore.grid(row=2, column=1)
    ACTScoreTooltip = CreateToolTip(ACTScore, 'Enter numeric digits only')
    ACTScore.config(validate="key",
                    validatecommand=(reg, '%P'))
    label2 = tk.Label(text="Enter your Percentage ( /100)", font=LabelFont)
    label2.grid(row=3, column=0, padx=10, pady=20)

    PercentageScore.grid(row=3, column=1)
    PercentageScoreTooltip = CreateToolTip(PercentageScore, 'Enter numeric digits only')
    PercentageScore.config(validate="key",
                    validatecommand=(reg, '%P'))
    label3 = tk.Label(text="Choose your Major", font=LabelFont)
    label3.grid(row=4, column=0, padx=10, pady=20)
    Majors = ttk.Combobox(state="readonly", textvariable=MajorChoice, values=Majorlist, width=35)
    Majors.current(0)
    Majors.grid(row=4, column=1)
    if NoOfFeatures == 5:
        label4 = tk.Label(text="Choose Residency Status", font=LabelFont)
        label4.grid(row=5, column=0, pady=20, padx=10)
        Radiobutton(text="In-State", variable=ResidencyStatus, value=9).grid(row=5, column=1)
        Radiobutton(text="Out-of-State", variable=ResidencyStatus, value=10).grid(row=5, column=2)
    Calculate = tk.Button(text="Calculate Chance ", height=1, width=14, font=ButtonFont,
                          command=CalcProbwithACTandPercentage)
    Calculate.grid(row=6, column=1, pady=10)
    GoBack = tk.Button(text="Click to go back ", height=1, width=14, font=ButtonFont, command=method)
    GoBack.grid(row=6, column=0, pady=10)
## ================================================================
## ================================================================
# Creating method that would quit the application in case the close button
# is clicked
def on_closing():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        root.destroy()
root.protocol('WM_DELETE_WINDOW', on_closing)
## ================================================================
# Creating log file to store the directory path of Theta1, Theta2 and the
# high school score type, standardized test type chosen by the user
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
log = open("log.txt", "a")  # write mode
log.write(dt_string +'\n')
log.write("College chosen is: "+ hp.CollegeChoice.get()+ '\n')
if hp.Scoretype.get() == 'GPA':
    log.write("High school score type chosen is: " + 'Percentage' + '\n')
else:
    log.write("High school score type chosen is: " + hp.Scoretype.get() + '\n')
log.write("Standardized test type chosen is: " + hp.Testtype.get()+'\n')
log.write("The directory path of Theta1 file chosen is: " + Theta1Dir+'\n')
log.write("The directory path of Theta2 file chosen is: " + Theta2Dir+'\n'+'\n')
log.close()
## ================================================================
root.mainloop()
