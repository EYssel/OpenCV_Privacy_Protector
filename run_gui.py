from tkinter import *
import tkinter.font as tkFont
import tkinter.messagebox as tkMsgBox
import PIL.Image
from PIL import ImageTk
from tkinter import filedialog
from tkinter import *
import cv2
import numpy
import object_extraction

def raise_frame(frame):
    frame.tkraise()

def merge_image_click(choice):
    if(choice.get() == 0):
        tkMsgBox.showerror("Select Type","Please select a type of feature to be obscured")
        return
    else:
        path = filedialog.askopenfilename()
        object_extraction.merge_image(choice.get(), path)

def merge_video_click(choice):
    if(choice.get() == 0):
        tkMsgBox.showerror("Select Type","Please select a type of feature to be obscured")
        return
    else:
        use_webcam = tkMsgBox.askyesno("Use Webcam","Do you want to use your webcam?")
        if(use_webcam):
            path = 0
            object_extraction.merge_video(choice.get(),path)
        else:
            path = filedialog.askopenfilename()
            object_extraction.merge_video(choice.get(), path)

def unmerge_image_click():
    #if(choice.get() == 0):
    #    tkMsgBox.showerror("Select Type","Please select a type of feature to be obscured")
    #    return
    #else:
    object_extraction.unmerge_image()

def unmerge_video_click():
    #if(choice.get() == 0):
    #    tkMsgBox.showerror("Select Type","Please select a type of feature to be obscured")
    #    return
    #else:
        #path = filedialog.askopenfilename()
    object_extraction.unmerge_video()

def select_image():
    global panelA, panelB
    path = filedialog.askopenfilename()
    
    if(len(path)>0):
        image = cv2.imread(path)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray,50,100)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        image = PIL.Image.fromarray(image)
        edged = PIL.Image.fromarray(edged)

        image = ImageTk.PhotoImage(image)
        edged = ImageTk.PhotoImage(edged)
        
        if(panelA is None or panelB is None):
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            panelB = Label(image=edged)
            panelB.image = edged
            panelB.pack(side="right", padx=10, pady=10)
        else:
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged

root = Tk()
root.geometry("500x450")
#root.eval('tk::PlaceWindow . center')
fontStyle = tkFont.Font(family="Lucida Grande", size=15)

panelA = None
panelB = None

fMain = Frame(root, width=500,height=450, background="#E7E7E7")
fMain.pack()
fMerge = Frame(root, width=500,height=450, background="#E7E7E7")
fUnmerge = Frame(root, width=500,height=450, background="#E7E7E7")

for frame in (fMain, fMerge, fUnmerge):
    frame.grid(row=0, column=0, sticky='news')

### Main ###
Label(fMain, text="Please select the operation you would like to use:",bg="#E7E7E7", font=fontStyle).place(x=25,y=25)
Button(fMain, text="Hide Features\nin Image/Video",bg="#195e83",fg="white", font=fontStyle, command=lambda:raise_frame(fMerge)).place(x=125,y=75,width=250,height=125)
Button(fMain, text="Extract Features\nfrom Image/Video",bg="#195e83",fg="white", font=fontStyle, command=lambda:raise_frame(fUnmerge)).place(x=125,y=275,width=250,height=125)

### Merge ###
vMerge = IntVar()
Label(fMerge, text="Please select the type of feature and type of file:",bg="#E7E7E7", font=fontStyle).place(x=25,y=25)
Radiobutton(fMerge, text="Faces",bg="#E7E7E7", font=fontStyle, variable=vMerge, value=1).place(x=125,y=75)
Radiobutton(fMerge, text="License Plates",bg="#E7E7E7", font=fontStyle, variable=vMerge, value=2).place(x=225,y=75)
Button(fMerge, text="Image",bg="#195e83",fg="white",command=lambda:merge_image_click(vMerge), font=fontStyle).place(x=125,y=125,width=250,height=75)
Button(fMerge, text="Video",bg="#195e83",fg="white",command=lambda:merge_video_click(vMerge), font=fontStyle).place(x=125,y=225,width=250,height=75)
Button(fMerge, text="Main Menu",bg="#195e83",fg="white", font=fontStyle, command=lambda:raise_frame(fMain)).place(x=125,y=325,width=250,height=75)

### Unmerge ###
vUnmerge = IntVar()
Label(fUnmerge, text="Please select the type of file to be unblurred:",bg="#E7E7E7", font=fontStyle).place(x=25,y=25)
#Radiobutton(fUnmerge, text="Faces",bg="#E7E7E7", font=fontStyle, variable=vUnmerge, value=1).place(x=125,y=75)
#Radiobutton(fUnmerge, text="License Plates",bg="#E7E7E7", font=fontStyle, variable=vUnmerge, value=2).place(x=225,y=75)
Button(fUnmerge, text="Extract from Image",bg="#195e83",fg="white", command=lambda:unmerge_image_click(), font=fontStyle).place(x=125,y=125,width=250,height=75)
Button(fUnmerge, text="Extract from Video",bg="#195e83",fg="white", command=lambda:unmerge_video_click(), font=fontStyle).place(x=125,y=225,width=250,height=75)
Button(fUnmerge, text="Main Menu",bg="#195e83",fg="white", font=fontStyle, command=lambda:raise_frame(fMain)).place(x=125,y=325,width=250,height=75)

root.title("Privacy Protector")
root.resizable(False, False)
raise_frame(fMain)
root.mainloop()