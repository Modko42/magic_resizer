import datetime
import random
import shutil
import string
import tkinter
from tkinter import filedialog
from threading import *
from tkinter.messagebox import showinfo

import PIL.Image
import os
import numpy as np

from tkinter import *

global original_folder_size
global path
global file_count
global finished_counter
global percent
global thread_finished_counter
file_count = 0
finished_counter = 0
percent = 0
thread_finished_counter = 0
original_folder_size = 0
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
    print("CPU cores to use: " + str(cpu_core_count_var.get()))
    print("Keep originals: " + str(keep_originals.get()))


window = Tk()

folder_label_var = StringVar()
folder_label_var.set("No root folder selected")

quality_var = StringVar()
quality_png_var = StringVar()
min_file_size_var = StringVar()
max_file_size_var = StringVar()
finished_percent_var = StringVar()
cpu_core_count_var = StringVar()
keep_originals = StringVar()

quality_var.set(85)
quality_png_var.set(95)
min_file_size_var.set(2)
max_file_size_var.set(50)
finished_percent_var.set("Finished: 0 %")
cpu_core_count_var.set(10)
keep_originals.set(1)


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
    quality_label.place(x=20, y=60)
    quality_var.trace("w", lambda name, index, mode, quality_var=quality_var: callback())
    quality_field = tkinter.Entry(window, width=3, textvariable=quality_var)
    quality_field.place(x=130, y=60)

    quality_png_label = tkinter.Label(window, text="Quality(png): ")
    quality_png_label.place(x=20, y=90)
    quality_png_var.trace("w", lambda name, index, mode, quality_png_var=quality_png_var: callback())
    quality_png_field = tkinter.Entry(window, width=3, textvariable=quality_png_var)
    quality_png_field.place(x=130, y=90)

    min_file_size_label = tkinter.Label(window, text="Min size(MB): ")
    min_file_size_label.place(x=20, y=120)
    min_file_size_var.trace("w", lambda name, index, mode, min_file_size_var=min_file_size_var: callback())
    min_file_size_field = tkinter.Entry(window, width=3, textvariable=min_file_size_var)
    min_file_size_field.place(x=130, y=120)

    max_file_size_label = tkinter.Label(window, text="Max size(MB): ")
    max_file_size_label.place(x=20, y=150)
    max_file_size_var.trace("w", lambda name, index, mode, max_file_size_var=max_file_size_var: callback())
    max_file_size_field = tkinter.Entry(window, width=3, textvariable=max_file_size_var)
    max_file_size_field.place(x=130, y=150)

    cpu_core_count_label = tkinter.Label(window, text="CPU cores to use: ")
    cpu_core_count_label.place(x=20, y=180)
    cpu_core_count_var.trace("w", lambda name, index, mode, cpu_core_count_var=cpu_core_count_var: callback())
    cpu_core_count_field = tkinter.Entry(window, width=3, textvariable=cpu_core_count_var)
    cpu_core_count_field.place(x=130, y=180)

    cpu_core_count_label = tkinter.Checkbutton(window, text='Keep original pictures', command=clear_path,
                                               variable=keep_originals,
                                               onvalue=1, offvalue=0)
    cpu_core_count_label.place(x=20, y=203)

    start_button = tkinter.Button(window, text="Start", command=start_new_threads)
    start_button.place(x=20, y=250)

    preview_button = tkinter.Button(window, text="Preview", command=make_preview)
    preview_button.place(x=90, y=250)

    finished_label_percent = tkinter.Label(window, width=20, textvariable=finished_percent_var)
    finished_label_percent.place(x=170, y=60)

    window.mainloop()


def clear_path():
    global path
    path = "No root folder selected"
    folder_label_var.set(path)


def select_file():
    global path
    path = filedialog.askdirectory(
        title='Open a file',
        initialdir='/')
    if not os.path.isdir(path):
        folder_label_var.set("No root folder selected")
    else:
        folder_label_var.set(path[-60:-30] + '\n' + path[-30:])


def list_all_files():
    global original_folder_size
    global path
    if int(keep_originals.get()) == 1:
        current_working_directory = os.getcwd()
        new_directory_name = str(
            "resized_pictures_" + str(os.path.basename(path)) + str(datetime.datetime.now().strftime("%H_%M_%S")))
        new_directory_path = os.path.join(current_working_directory, new_directory_name)
        shutil.copytree(path, new_directory_path)
        path = new_directory_path
        folder_label_var.set(path[-60:-30] + '\n' + path[-30:])
    filepaths = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            file_size = get_file_size_inMB(subdir + '/' + file)
            if float(min_file_size_var.get()) < file_size < float(max_file_size_var.get()):
                filepaths.append(subdir + '/' + file)

    print("Files found: " + str(len(filepaths)))
    original_folder_size = get_folder_size(path)
    return filepaths


def make_preview():
    try:
        preview_path = filedialog.askopenfile(
            title='Choose a file to preview settings',
            initialdir='/').name
        shutil.copy(preview_path, os.path.join(os.getcwd(), 'preview_original.jpg'))
        shutil.copy(preview_path, os.path.join(os.getcwd(), 'preview_resized.jpg'))
        resize([os.path.join(os.getcwd(), 'preview_resized.jpg')], Preview_mode=True)
        showinfo("Succes", "Preview generated!")
    except Exception as e:
        print(e)
        print("You probably didn't choose a file!")



def start_new_threads():
    global finished_counter
    global percent
    global thread_finished_counter
    global file_count
    finished_counter = 0
    percent = 0
    thread_finished_counter = 0
    try:
        files_fullpath = np.array(list_all_files())
        file_count = len(files_fullpath)
        chunks = np.array_split(files_fullpath, int(cpu_core_count_var.get()))
        for thr in range(0, int(cpu_core_count_var.get())):
            Thread(target=resize, args=[chunks[thr]]).start()
    except Exception as e:
        print("Probably Folder already exists!")
        print(e)


def resize(file_paths, Preview_mode=False):
    global finished_counter
    global percent
    global thread_finished_counter
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
            except Exception as e:
                print(e)
                print("Problem with image: " + str(file))
            finished_counter = finished_counter + 1
        if os.path.isfile(file) and file.split('.')[-1].lower() == 'png':
            try:
                im = PIL.Image.open(file).convert('RGB')
                f, e = os.path.splitext(file)
                im.save(f + '.jpg', 'JPEG', quality=int(quality_png_var.get()))
                im.close()
                os.remove(file)
            except Exception as e:
                print(e)
                print("Problem with image: " + str(file))
            finished_counter = finished_counter + 1
        if not Preview_mode:
            if percent + 1 < round(100 * finished_counter / file_count, 2):
                percent = round(100 * finished_counter / file_count, 2)
                finished_percent_var.set("Finished: " + str(percent) + "%")
    thread_finished_counter += 1
    if thread_finished_counter == int(cpu_core_count_var.get()):
        global path
        finished_percent_var.set("Finished: " + str(100) + "%")
        showinfo("Success", "Image compression finished")
        path = "No root folder selected"
        folder_label_var.set(path)


draw_gui()
