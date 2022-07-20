import concurrent.futures
import tkinter
from tkinter import filedialog, tix
from threading import *
from tkinter.messagebox import showinfo
from tkinter.tix import *

import PIL.Image
import os
import tkinter as tk
import numpy as np

from tkinter import *

global original_folder_size
global path
path = ""


def get_file_size_inMB(file):
    return os.stat(file).st_size / 1048576


def get_folder_size(root):
    size = 0
    for path, dirs, files in os.walk(root):
        for f in files:
            size += os.path.getsize(os.path.join(path, f)) / 1048576
    return round(size, 2)


def callback():
    print("Current quality: " + str(quality_var.get()))
    print("Current quality(png): " + str(quality_png_var.get()))
    print("Current min file size: " + str(min_file_size_var.get()))
    print("Current max file size: " + str(max_file_size_var.get()))


window = Tk()

folder_label_var = StringVar()
folder_label_var.set("Default")

quality_var = StringVar()
quality_png_var = StringVar()
min_file_size_var = StringVar()
max_file_size_var = StringVar()
finished_percent_var = StringVar()

quality_var.set(85)
quality_png_var.set(95)
min_file_size_var.set(2)
max_file_size_var.set(50)
finished_percent_var.set("Finished: 0 %")

def draw_gui():
    window.title("TheBestResizerEver")
    window.geometry("450x300")
    window.eval('tk::PlaceWindow . center')
    window.resizable(False, False)
    open_button = tkinter.Button(window, text='Choose root folder', command=select_file)
    open_button.place(x=20, y=20)
    folder_label = tkinter.Label(window, textvariable=folder_label_var)
    folder_label.place(x=200, y=22)

    quality_label = tkinter.Label(window, text="Quality: ")
    quality_label.place(x=20, y=62)
    quality_var.trace("w", lambda name, index, mode, quality_var=quality_var: callback())
    quality_field = tkinter.Entry(window, width=3, textvariable=quality_var)
    quality_field.place(x=110, y=60)

    quality_png_label = tkinter.Label(window, text="Quality(png): ")
    quality_png_label.place(x=20, y=92)
    quality_png_var.trace("w", lambda name, index, mode, quality_png_var=quality_png_var: callback())
    quality_png_field = tkinter.Entry(window, width=3, textvariable=quality_png_var)
    quality_png_field.place(x=110, y=90)

    min_file_size_label = tkinter.Label(window, text="Min size(MB): ")
    min_file_size_label.place(x=20, y=122)
    min_file_size_var.trace("w", lambda name, index, mode, min_file_size_var=min_file_size_var: callback())
    min_file_size_field = tkinter.Entry(window, width=3, textvariable=min_file_size_var)
    min_file_size_field.place(x=110, y=120)

    max_file_size_label = tkinter.Label(window, text="Min size(MB): ")
    max_file_size_label.place(x=20, y=152)
    max_file_size_var.trace("w", lambda name, index, mode, max_file_size_var=max_file_size_var: callback())
    max_file_size_field = tkinter.Entry(window, width=3, textvariable=max_file_size_var)
    max_file_size_field.place(x=110, y=150)

    start_button = tkinter.Button(window, text="Start", command=start_new_threads)
    start_button.place(x=20, y=180)

    finished_label_percent = tkinter.Label(window, width=20, textvariable=finished_percent_var)
    finished_label_percent.place(x=150, y=60)




    window.mainloop()



def select_file():
    global path
    path = filedialog.askdirectory(
        title='Open a file',
        initialdir='/')
    folder_label_var.set(path[-60:-30] +'\n'+ path[-30:])


def list_all_files():
    global original_folder_size
    filepaths = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            file_size = get_file_size_inMB(subdir + '/' + file)
            if float(min_file_size_var.get()) < file_size < float(max_file_size_var.get()):
                filepaths.append(subdir + '/' + file)

    print("Files found: " + str(len(filepaths)))
    original_folder_size = get_folder_size(path)
    return filepaths


original_folder_size = 0
global file_count
global finished_counter
global percent
file_count = 0
finished_counter = 0
percent = 0

def start_new_threads():
    global file_count
    files_fullpath = np.array(list_all_files())
    file_count = len(files_fullpath)
    chunks = np.array_split(files_fullpath,8)
    t1 = Thread(target=resize, args=[chunks[0]])
    t1.start()
    t2 = Thread(target=resize, args=[chunks[1]])
    t2.start()
    t3 = Thread(target=resize, args=[chunks[2]])
    t3.start()
    t4 = Thread(target=resize, args=[chunks[3]])
    t4.start()
    t5 = Thread(target=resize, args=[chunks[4]])
    t5.start()
    t6 = Thread(target=resize, args=[chunks[5]])
    t6.start()
    t7 = Thread(target=resize, args=[chunks[6]])
    t7.start()
    t8 = Thread(target=resize, args=[chunks[7]])
    t8.start()





def resize(file_paths):
    global finished_counter
    global percent
    for file in file_paths:
        if os.path.isfile(file) and file.split('.')[-1].lower() == 'jpg':
            try:
                im = PIL.Image.open(file)
                f, e = os.path.splitext(file)
                im.save(f + '.jpg', 'JPEG', quality=int(quality_var.get()))
            except Exception as e:
                print(e)
                print("Problem with image: " + str(file))
            finished_counter = finished_counter + 1
        if os.path.isfile(file) and file.split('.')[-1].lower() == 'bmp':
            try:
                im = PIL.Image.open(file)
                f, e = os.path.splitext(file)
                im.save(f + '.jpg', 'JPEG', quality=int(quality_var.get()))
                im.close()
                os.remove(file)
            except:
                print("Problem with image: " + str(file))
            finished_counter = finished_counter + 1
        if os.path.isfile(file) and file.split('.')[-1].lower() == 'png':
            try:
                im = PIL.Image.open(file).convert('RGB')
                f, e = os.path.splitext(file)
                im.save(f + '.jpg', 'JPEG', quality=int(quality_png_var.get()))
                im.close()
                os.remove(file)
            except:
                print("Problem with image: " + str(file))
            finished_counter = finished_counter + 1
        if percent + 1 < round(100 * finished_counter / file_count, 2):
            percent = round(100 * finished_counter / file_count, 2)
            finished_percent_var.set("Finished: "+str(percent)+"%")
        if finished_counter == file_count:
            finished_percent_var.set("Finished: " + str(100) + "%")
            showinfo("Success", "Image compression finished")
draw_gui()
