import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter.constants import  NSEW, W
from check_plagiarism import driver_function

# Text Widget to hold the output
output_text=None


def on_close():

    '''
    
    Handles the closure of the tkinter window

    '''

    if messagebox.askokcancel("Quit","Do you want to Quit?"):
        root.destroy()
        exit()


def on_submit():

    '''
    
    Function which executes the python script to check for plagiarism
    
    '''

    chrome_webdriver=chrome_webdriver_text.get(1.0,"end-1c")
    submission_link=submission_link_text.get(1.0,"end-1c")
    username=username_text.get(1.0,"end-1c")
    password=password_text.get()
    output=driver_function(chrome_webdriver,submission_link,username,password)
    set_output_text(output)


def get_output_text():
    
    '''
    
    Creates the output Text Widget and Positions it

    '''

    global output_text
    output_text=tk.Text(root,wrap="none",width=45,height=12)
    output_text.grid(row=6,column=0,pady=(10,0))

def set_output_text(output):

    '''

    Displays the output on output_text

    Parameters:
    output (String) : Output String to be displayed
    
    '''

    global output_text
    if output_text==None:
        get_output_text()
    output_text.delete(1.0,"end")
    output_text.insert(1.0,output)

def get_label_widget(row,text,top_pad=10):

    '''
    
    Creates Label Widget and Positions it

    Parameters:
    row (Int) : Number of row in grid layout
    text (String) : Label text
    top_pad (Int) : Padding amount on the top

    Returns:
    label_widget (Label) : Newly attatched Label widget
    
    '''

    label_widget=tk.Label(root,text=text,font=("Arial",15))
    label_widget.grid(row=row,column=0,sticky=W, padx=(13,0), pady=(top_pad,0))
    return label_widget

def get_text_widget(row,top_pad=10):

    '''
    Creates Text Widget and Positions it

    Parameters:
    row (Int) : Number of row in grid layout
    top_pad (Int) : Padding amount on the top
    
    Returns:
    label_widget (Text) : Newly attatched Text widget

    '''

    text_widget=tk.Text(root, wrap="none", width=20, height=1)
    text_widget.grid(row=row,column=0,sticky=NSEW,padx=(320,0),pady=(top_pad,0))
    return text_widget


# Title of the window
heading="Hackerrank Plagiarism Detection"

# Window element
root=tk.Tk()
root.geometry("600x600")
root.title(heading)

# Logo Image
img=PhotoImage(file="label.png")
label=tk.Label(root,image=img)
label.grid(row=0,column=0,padx=(70,0),pady=(15,0))

# Chrome Webdriver
enter_chrome_webdriver=get_label_widget(1,"Enter Chrome WebDriver Path",30)
chrome_webdriver_text=get_text_widget(1,30)

# Submission Link
enter_submission_link=get_label_widget(2,"Enter Contest Submission Link")
submission_link_text=get_text_widget(2)

# Hackerrank Username
enter_username=get_label_widget(3,"Enter Hackerrank Username")
username_text=get_text_widget(3)

# Hackerrank Password
enter_password=get_label_widget(4,"Enter Hackerrank Password")
password_text=tk.Entry(root,show="*",width=20)
password_text.grid(row=4,column=0,sticky=NSEW,padx=(320,0),pady=(10,0))

# Submit Buttton
submit=tk.Button(root,text="Submit",command=on_submit)
submit.grid(row=5,column=0,pady=(15,0))

root.protocol("WM_DELETE_WINDOW",on_close)
root.mainloop()