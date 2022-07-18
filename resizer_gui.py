import tkinter
from tkinter import filedialog

from PIL import Image
import os
import tkinter as tk

from tkinter import *


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

window = tk.Tk()

folder_label_var = StringVar()
folder_label_var.set("Default")

quality_var = StringVar()
quality_png_var = StringVar()
min_file_size_var = StringVar()
max_file_size_var = StringVar()

quality_var.set(85)
quality_png_var.set(95)
min_file_size_var.set(2)
max_file_size_var.set(50)


def draw_gui():
    window.title("TheBestResizerEver")
    window.geometry("450x300")
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

    start_button = tkinter.Button(window,text="Start",command=resize)
    start_button.place(x=20,y=180)

    window.mainloop()


def select_file():
    global path
    path = filedialog.askdirectory(
        title='Open a file',
        initialdir='/')
    folder_label_var.set(".." + path[-30:])




original_folder_size = get_folder_size(path)


def list_all_files():
    print(path)
    filepaths = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            file_size = get_file_size_inMB(subdir + '/' + file)
            if float(min_file_size_var.get()) < file_size < float(max_file_size_var.get()):
                filepaths.append(subdir + '/' + file)

    print("Files found: " + str(len(filepaths)))
    return filepaths

files_fullpath = []


def resize():
    files_fullpath = list_all_files()
    print(files_fullpath)
    percent = 0
    i = 0
    for file in files_fullpath:
        if percent + 1 < round(100 * i / len(files_fullpath), 2):
            percent = round(100 * i / len(files_fullpath), 2)
            print(str(percent) + " % done")
        if os.path.isfile(file) and file.split('.')[-1].lower() == 'jpg':
            try:
                im = Image.open(file)
                f, e = os.path.splitext(file)
                im.save(f + '.jpg', 'JPEG', quality=int(quality_var.get()))
            except Exception as e:
                print(e)
                print("Problem with image: " + str(file))
            i = i + 1
        if os.path.isfile(file) and file.split('.')[-1].lower() == 'bmp':
            try:
                im = Image.open(file)
                f, e = os.path.splitext(file)
                im.save(f + '.jpg', 'JPEG', quality=int(quality_var.get()))
                im.close()
                os.remove(file)
            except:
                print("Problem with image: " + str(file))
            i = i + 1
        if os.path.isfile(file) and file.split('.')[-1].lower() == 'png':
            try:
                im = Image.open(file).convert('RGB')
                f, e = os.path.splitext(file)
                im.save(f + '.jpg', 'JPEG', quality=int(quality_png_var.get()))
                im.close()
                os.remove(file)
            except:
                print("Problem with image: " + str(file))
            i = i + 1


draw_gui()

resized_folder_size = get_folder_size(path)
print("Original total size: " + str(original_folder_size) + " MB")
print("Resized  total size: " + str(resized_folder_size) + " MB")
