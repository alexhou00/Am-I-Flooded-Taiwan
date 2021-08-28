# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 21:57:14 2021

@author: MonkeyPair
"""
### In this project, long is latitude, lati is longtitude
from tkinter import Tk, Entry, Frame, Label, DoubleVar, IntVar, StringVar, Spinbox, Button, Toplevel
import queue
#from PIL import Image, ImageTk
from tkinter import BOTH, PhotoImage, Canvas, NW, LEFT
from geopy.geocoders import Nominatim

def findflood():
    d2dms()
    placevar.set("")
    lbladdress.config(text='')
    whatever.config(text="Loading...", fg='gray')
    if altitude.get()>1000: altitude.set(1000)
    h = altitude.get()
    a = [int(longvar.get()*100), int(lativar.get()*100)]
    q = queue.Queue(maxsize = -1)
    q.put(a)
    f = open('data_all.txt','r')
    datas = f.read()
    datas = datas.split('\n')
    finded= []
    flooded = 0
    isAlreadySea = 1
    while(not q.empty()):
        m = q.get()
        coord = str(m[0])+' '+str(m[1])
        #print(coord)
        k = [s for s in datas if coord in s]
        if k == []: 
            whatever.config(text="The place is not near Taiwan", fg='#999999')
            return 0
        #print(k)
        word = float(k[0].split(' ')[-1])
        if word<=0 or word == 9999.0:#Touching Sea Water
            #print('flooded')
            if isAlreadySea:
                whatever.config(text="The place is already in the sea or below sea level", fg='blue')
            else:
                whatever.config(text="Flooded!", fg='red')
            return 1
            #flooded = 1
            #break
        elif word<=h:#往周圍八格擴散
            for i in range(-1,2):
                for j in range(-1,2):
                    if not(i == 0 and j == 0) and (coord not in finded):
                        q.put([m[0]+i,j+m[1]])
        finded.append(coord)#Record where we steped on
        isAlreadySea = 0
    if flooded == 0:
        whatever.config(text="Safe!", fg='green')
        #print('safe!')
        return 0
    f.close()

def dms2d(*args):
    try:
        longvar.set(round(longvard.get() + longvarm.get()/60 + longvars.get()/(60*60), 2))
        lativar.set(round(lativard.get() + lativarm.get()/60 + lativars.get()/(60*60), 2))
        whatever.config(text="")
    except:
        whatever.config(text="Plz enter correct format", fg='red')

def d2dms(*args):
    global dot, canvas
    try:
        d = int(longvar.get())
        md = abs(longvar.get() - d) * 60
        m = int(md)
        s = (md - m) * 60
        longvard.set(d)
        longvarm.set(m)
        longvars.set(round(s*100)/100)
        d = int(lativar.get())
        md = abs(lativar.get() - d) * 60
        m = int(md)
        s = (md - m) * 60
        lativard.set(d)
        lativarm.set(m)
        lativars.set(round(s*100)/100)
        whatever.config(text="")
        x = long2x(lativar.get())
        y = lati2y(longvar.get())
    except:
        whatever.config(text="Plz enter correct format", fg='red')
    try:
        canvas.coords(dot, (x, y, x+10, y+10))
    except:
        pass

def how():
    global top1
    top1 = Toplevel(win)
    top1.title("How to Use the Application")
    top1.iconbitmap("flood.ico")
    top1.configure(bg=BGCOLOR)
    top1.resizable(False, False)
    labeltoptitle = Label(top1, text='Instructions of Am I Flooded in Taiwan', bg=BGCOLOR, font=("Arial", 16))
    labeltoptitle.pack(padx=10, pady=10)
    labeltop = Label(top1, text='''
1. Enter the latitude and longtitude in the corresponding boxes,\n
    you may also use the "Show Map of Taiwan" button and place a mark on the map.\n
    Entering the name of the place is also accepted.\n
2. Select the rising height of the sea level.\n
3. Press "Submit", the program will run its datasets,\n
    and you will see if the place will be flooded when the sea level rise.''', bg=BGCOLOR, font=("Arial", 12), justify=LEFT)
    labeltop.pack(padx=10, pady=10)
    okay = Button(top1, text="OK, I got it", command=destro, bg='#99bbff', activebackground=BGCOLOR)
    okay.pack(pady=10)
    top1.mainloop()

def destro():
    global top1
    top1.destroy()

def showMap():
    global dot, canvas
    top2 = Toplevel(win)
    top2.title("Map of Taiwan")
    top2.iconbitmap("flood.ico")
    top2.configure(bg='#deebf7')
    top2.resizable(False, False)
    #img = Image.open("taiwan.png")
    #tkimage = ImageTk.PhotoImage(img)
    #lbl = Label(top2, image=tkimage, bd=0)
    #lbl.image = tkimage
    #lbl.pack() #791
    maptitle = Label(top2, text='Map of Taiwan', font=("Arial", 16), bg='#deebf7')
    maptitle.pack()
    mapintro = Label(top2, bg='#deebf7', text='Enter coordinates or click on a place', font=("Arial", 12))
    mapintro.pack()
    canvas = Canvas(top2, width=632, height=815, bd=0, bg='#deebf7', highlightthickness=0)
    canvas.pack(fill=BOTH)
    img = PhotoImage(file='taiwan.png')
    canvas.create_image(0, 0, anchor=NW, image=img)
    
    dot = canvas.create_oval(long2x(lativar.get()), lati2y(longvar.get()), long2x(lativar.get())+10, lati2y(longvar.get())+10, fill="#ff0000")
    canvas.create_oval(190, 804, 200, 814, fill='#ff0000')
    canvas.create_text(205, 800, text=': The position you\'ve entered or clicked on', anchor=NW)
    lblwiki = Label(top2, text="Source: Wikipedia", bg='#deebf7')
    lblwiki.pack()
    canvas.bind("<Button-1>", markmap)
    top2.mainloop()

def long2x(long):
    return (long-120)*182+194

def lati2y(lati):
    return (lati-22)*(-201)+721

def x2long(x):
    return (x-194)/182+120

def y2lati(y):
    return (y-721)/(-201)+22

def markmap(event):
    global dot, canvas
    try:
        x = event.x-5
        y = event.y-5
        canvas.coords(dot, (x, y, x+10, y+10))
        longvar.set(round(y2lati(y), 2))
        lativar.set(round(x2long(x), 2))
    except NameError as e:
        pass

def add():
    try:
        n = geolocator.geocode(placevar.get())
        lbladdress.config(text='Place found: '+n.address)
        longvar.set(round(n.latitude, 2))
        lativar.set(round(n.longitude, 2))
    except:
        lbladdress.config(text='Place not found: '+n.address)

BGCOLOR = '#bbddff'
LIGHTBGCOLOR = '#cceeff'
win = Tk()
win.title("Am I Flooded Taiwan")
win.configure(bg=BGCOLOR)
win.resizable(False, False)
win.iconbitmap("flood.ico")

geolocator = Nominatim(user_agent="LKhfHlkikLHUauf")

title = Label(win, text="Enter Your Coordinates to See if You're Flooded when Sea Level Rises", font=("Arial", 16), bg=BGCOLOR)
title.pack(padx=5, pady=5)
frame_sub = Frame(win, bg=BGCOLOR)
frame_sub.pack()
title2 = Label(frame_sub, text="Note: Enter the coordinates of Taiwan only", font=("Arial", 12), bg=BGCOLOR)
title2.grid(padx=5, row=0, column=0)
btnhow = Button(frame_sub, text="How to Use", command=how, activebackground=BGCOLOR, bg=BGCOLOR)
btnhow.grid(padx=5, row=0, column=1)
btnmap = Button(frame_sub, text="Show Map of Taiwan", command=showMap, activebackground=BGCOLOR, bg=BGCOLOR)
btnmap.grid(padx=5, row=0, column=2)

frame1 = Frame(win, bg=BGCOLOR)
frame1.pack(padx=5, pady=15)

whatever = Label(frame1, bg=BGCOLOR, font=("Arial", 19))
whatever.grid(row=9, columnspan=7)

longvar = DoubleVar()
lativar = DoubleVar()
longvard = IntVar()
longvarm = IntVar()
longvars = DoubleVar()
lativard = IntVar()
lativarm = IntVar()
lativars = DoubleVar()
placevar = StringVar()
longvar.set(22.9)
lativar.set(120.3)
d2dms()
altitude = IntVar()
altitude.set(1)

dot = 0
canvas = Canvas()
top1 = 0

decimal = Label(frame1, text="Enter Coordinates in decimal form: ", bg=BGCOLOR)
decimal.grid(row=1, column=0, sticky='e')
longtxt = Label(frame1, text="Latitude:", bg=BGCOLOR)
longtxt.grid(row=1, column=1)
longtitude = Entry(frame1, textvariable=longvar, bg=LIGHTBGCOLOR, bd=0, width=15)
longtitude.grid(row=1, column=2)
latitxt = Label(frame1, text="Longtitude:", bg=BGCOLOR)
latitxt.grid(row=1, column=4)
latitude = Entry(frame1, textvariable=lativar, bg=LIGHTBGCOLOR, bd=0, width=15)
latitude.grid(row=1, column=5)
submitd = Button(frame1, command=d2dms, text='Convert', bg=BGCOLOR, activebackground=BGCOLOR)
submitd.grid(row=1, column=6)

OR = Label(frame1, text="OR", bg=BGCOLOR)
OR.grid(row=2, column=0, columnspan=6, pady=8)

dms = Label(frame1, text="Enter Coordinates in DMS form and convert: ", bg=BGCOLOR)
dms.grid(row=3, column=0, sticky='e')
framelong = Frame(frame1, bg=BGCOLOR)
framelong.grid(row=3, column=2)
longtxt2 = Label(frame1, text="Latitude:", bg=BGCOLOR)
longtxt2.grid(row=3, column=1)
label1 = Label(framelong, text="°", bg=BGCOLOR)
label2 = Label(framelong, text="'", bg=BGCOLOR)
label3 = Label(framelong, text='"', bg=BGCOLOR)
longtituded = Entry(framelong, width=3, textvariable=longvard, bg=LIGHTBGCOLOR, bd=0)
longtituded.grid(row=0, column=0)
longtitudem = Entry(framelong, width=3, textvariable=longvarm, bg=LIGHTBGCOLOR, bd=0)
longtitudem.grid(row=0, column=2)
longtitudes = Entry(framelong, width=5, textvariable=longvars, bg=LIGHTBGCOLOR, bd=0)
longtitudes.grid(row=0, column=4)
label1.grid(row=0, column=1)
label2.grid(row=0, column=3)
label3.grid(row=0, column=5)

framelati = Frame(frame1, bg=BGCOLOR)
framelati.grid(row=3, column=5)
latitxt2 = Label(frame1, text="Longtitude:", bg=BGCOLOR)
latitxt2.grid(row=3, column=4)
label4 = Label(framelati, text="°", bg=BGCOLOR)
label5 = Label(framelati, text="'", bg=BGCOLOR)
label6 = Label(framelati, text='"', bg=BGCOLOR)
latituded = Entry(framelati, width=3, textvariable=lativard, bg=LIGHTBGCOLOR, bd=0)
latituded.grid(row=0, column=0)
latitudem = Entry(framelati, width=3, textvariable=lativarm, bg=LIGHTBGCOLOR, bd=0)
latitudem.grid(row=0, column=2)
latitudes = Entry(framelati, width=5, textvariable=lativars, bg=LIGHTBGCOLOR, bd=0)
latitudes.grid(row=0, column=4)
label4.grid(row=0, column=1)
label5.grid(row=0, column=3)
label6.grid(row=0, column=5)
submitdms = Button(frame1, command=dms2d, text='Convert', bg=BGCOLOR, activebackground=BGCOLOR)
submitdms.grid(row=3, column=6)

OR2 = Label(frame1, text="OR", bg=BGCOLOR)
OR2.grid(row=4, column=0, columnspan=6, pady=8)

address = Label(frame1, text="Enter address or landmark name: ", bg=BGCOLOR)
address.grid(row=5, column=0, sticky='e')
place = Entry(frame1, textvariable=placevar, bg=LIGHTBGCOLOR, bd=0, width=45)
place.grid(row=5, column=1, columnspan=5)
submitadd = Button(frame1, command=add, text=' Enter ', bg=BGCOLOR, activebackground=BGCOLOR)
submitadd.grid(row=5, column=6)
lbladdress = Label(frame1, text="", bg=BGCOLOR)
lbladdress.grid(row=6, column=0, columnspan=6)

height_frame = Frame(frame1, bg=BGCOLOR)
height_frame.grid(row=7, columnspan=7, pady=19)
height_label = Label(height_frame, text='With Sea Level Risen', font=("Arial", 12), bg=BGCOLOR)
height_label.grid(row=0, column=0)
height_entry = Spinbox(height_frame, from_=0, to=1000, textvariable=altitude, width=5, highlightbackground=BGCOLOR, bg=LIGHTBGCOLOR)
height_entry.grid(row=0, column=1)
height_label2 = Label(height_frame, text='meters', font=("Arial", 12), bg=BGCOLOR)
height_label2.grid(row=0, column=2)

submitbtn = Button(frame1, command=findflood, text='Submit', font=("Arial", 12), bg='#99bbff', activebackground=BGCOLOR)
submitbtn.grid(row=8, pady=5, columnspan=7)

#longvar.trace('w', d2dms)
#lativar.trace('w', d2dms)

win.mainloop()
