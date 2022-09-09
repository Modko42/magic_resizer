import datetime
import random
import shutil
import string
import time
import tkinter
from tkinter import filedialog
from threading import *
from tkinter.messagebox import showinfo, showwarning
from pathlib import Path

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
global en_dict
global ch_dict
global active_dict
global start_time
global copy_finished_time
global compression_finished_time
file_count = 0
finished_counter = 0
percent = 0
thread_finished_counter = 0
original_folder_size = 0
path = ""

en_dict = {
    "current_quality": "Current quality",
    "current_quality_png": "Current quality(PNG)",
    "no_root_folder": "No root folder selected",
    "quality": "Quality: ",
    "quality_png": "Quality(PNG): ",
    "min_file_size": "Min file size: ",
    "max_file_size": "Max file size: ",
    "cpu_core_count": "CPU cores to use: ",
    "keep_originals": "Keep original pictures",
    "start_button": "Start",
    "preview_button": "Preview",
    "help_button": "Help",
    "open_button": "Choose root folder",
    "app_name": "Amalgam Image Resize Tool v1.0",
    "help_window": "Help window",
    "help_1": "The Amalgam Image Resize Tool has been created to process any .jpeg, .jpg, .bmp or .png image to smaller filesize, ready to upload into Sharepoint.",
    "help_2": "It does not resize or change image resolution.",
    "help_3": "Input images formats are:  .jpg, .jpeg, .png, .bmp.",
    "help_4": "Output format is .jpg (.png .bmp will be converted to .jpg).",
    "help_5": "Recursive sub-folder processing!",
    "help_6": "High quality & very fast processing!",
    "how_to_use": "How to use:\nUse the 'Choose Folder' button to select a folder containing images.\nAny sub folders containing images will also be processed. \n\nQuality setting % for .jpg & .bmp:\nPresent to 89%.  ANY original .jpeg or .bmp image at this quality setting will be reduced to over half it's filesize with zero loss of quality.\nQuality setting % for .png: \nPNG original images need a different setting.  Present to 95%.  ANY original .png image at this quality setting will be reduced to at least half it's original filesize.\n\nMin Size (MB):\nThis controls the minimum size of image files to process. For example: Source folder contains 1mb images files that we do not want to reduce in size any further. So, set Min Size to 1mb, any source image file smaller than 1mb will be ignored.\n\nMax Size (MB):\nThis controls the minimum size of image files to process. Ignore any source image files over specified filesize in mb.\n\nCPU Threads:\nThis is set at 8 cpu threads by default. If you have higher performance cpu with more core/thread's then enter higher value to increase performance.\n\nKeep Original Files:\nIf un-checked, the original source images will be over-written in place.\nIf checked a re-saved copy of the source folder will be created next to the source. (sub-folder structure will be kept)."
}
ch_dict = {
    "current_quality": "当前质量",
    "current_quality_png": "Current quality(PNG)",
    "no_root_folder": "未选择文件夹",
    "quality": "品质%.jpg.bmp ",
    "quality_png": "品质%.png ",
    "min_file_size": "最小尺寸（MB）",
    "max_file_size": "最大尺寸（MB）",
    "cpu_core_count": "CPU线程数",
    "keep_originals": "保留原始文件",
    "start_button": "开始",
    "preview_button": "预览",
    "help_button": "帮助",
    "open_button": "选择文件夹",
    "app_name": "Amalgam 图像调整工具 v1.0",
    "help_window": "帮助窗口",
    "help_1": "Amalgam图片大小调整工具支持jpeg、 jpg、bmp及png格式，可缩小文件大小，便于上传至Sharepoint。",
    "help_2": "图像分辨率不变。",
    "help_3": "导入的图片格式有: jpg、jpeg、png、 bmp。",
    "help_4": "导出格式为jpg(png及bmp将被转换为jpg)",
    "help_5": "可处理多层子文件夹",
    "help_6": "高画质&快速图片处理",
    "how_to_use": "如何使用\n使用“选择文件夹”按钮选择一个包含图像的文件夹。 任何包含图像的子文件夹也将被处理。\njpg和bmp格式画质设置%:\n默认89%。 在该设置下，任何jpeg或bmp图片将缩小至原始文件大小的一半以上，且画质零损失。\npng格式画质设置%:\nPng图片画质设置不同。默认95%。 在该设置下，任何png图片将被缩小至原始文件大小的至少一半。\n最小尺寸（MB）\n控制要处理的图像文件的最小尺寸。 示例:源文件夹包含1mb的图像文件，我们不想进一步减少其大小。 因此，将Min Size设置为1mb，任何小于1mb的源文件将被忽略。\n最大尺寸（MB）\n默认值50 mb。 控制要处理的图像文件的最大尺寸。 示例:忽略超过指定文件大小(以兆为单位)的任何源文件。\nCPU线程数默认8个CPU线程。 如果您有更高性能的CPU和更多的核/线程，那么输入更高的值来提高性能。\n保留原始文件:\n如果未勾选，原始图像将被覆盖 \n如果选中此项，将在源文件夹旁边创建源文件夹的副本。 (子文件夹结构将被保留)。\n"
}

active_dict = en_dict


def get_file_size_inMB(file):
    return os.stat(file).st_size / 1048576


def get_folder_size(root):
    size = 0
    for path, dirs, files in os.walk(root):
        for f in files:
            size += os.path.getsize(os.path.join(path, f)) / 1048576
    return round(size, 2)


def callback():
    print(active_dict["current_quality"] + str(quality_var.get()))
    print(active_dict["current_quality_png"] + str(quality_png_var.get()))
    print("Current min file size: " + str(min_file_size_var.get()))
    print("Current max file size: " + str(max_file_size_var.get()))
    print("CPU cores to use: " + str(cpu_core_count_var.get()))
    print("Keep originals: " + str(keep_originals.get()))
    print("Current language is english: " + str(selected_language_eng.get()))


def update_dict():
    global active_dict
    global en_dict
    global ch_dict
    if int(selected_language_eng.get()) == 1:
        active_dict = en_dict
    else:
        active_dict = ch_dict
    callback()


window = Tk()

folder_label_var = StringVar()
folder_label_var.set(active_dict['no_root_folder'])

quality_var = StringVar()
quality_png_var = StringVar()
min_file_size_var = StringVar()
max_file_size_var = StringVar()
status_var = StringVar()
cpu_core_count_var = StringVar()
keep_originals = StringVar()
selected_language_eng = IntVar()

quality_var.set(89)
quality_png_var.set(95)
min_file_size_var.set(2)
max_file_size_var.set(50)
status_var.set("")
try:
    if os.cpu_count() in range(1, 20, 1):
        cpu_core_count_var.set(round(os.cpu_count() * 0.8))
except:
    cpu_core_count_var.set(3)
keep_originals.set(1)
selected_language_eng.set(1)


def draw_gui():
    def update_labels():
        update_dict()
        quality_label.config(text=active_dict['quality'])
        quality_png_label.config(text=active_dict['quality_png'])
        min_file_size_label.config(text=active_dict['min_file_size'])
        max_file_size_label.config(text=active_dict['max_file_size'])
        cpu_core_count_label.config(text=active_dict['cpu_core_count'])
        keep_originals_label.config(text=active_dict['keep_originals'])
        start_button.config(text=active_dict['start_button'])
        preview_button.config(text=active_dict['preview_button'])
        open_button.config(text=active_dict['open_button'])
        help_button.config(text=active_dict['help_button'])
        folder_label_var.set(active_dict['no_root_folder'])
        window.title(active_dict['app_name'])

    window.title(active_dict['app_name'])
    window.geometry("450x300+200+200")
    window.resizable(False, False)
    open_button = tkinter.Button(window, text='Choose root folder', command=select_file)
    open_button.place(x=20, y=20)
    folder_label = tkinter.Label(window, textvariable=folder_label_var)
    folder_label.place(x=200, y=22)

    quality_label = tkinter.Label(window, text=active_dict['quality'])
    quality_label.place(x=20, y=60)
    quality_var.trace("w", lambda name, index, mode, quality_var=quality_var: callback())
    quality_field = tkinter.Entry(window, width=3, textvariable=quality_var)
    quality_field.place(x=150, y=60)

    quality_png_label = tkinter.Label(window, text="Quality(png): ")
    quality_png_label.place(x=20, y=90)
    quality_png_var.trace("w", lambda name, index, mode, quality_png_var=quality_png_var: callback())
    quality_png_field = tkinter.Entry(window, width=3, textvariable=quality_png_var)
    quality_png_field.place(x=150, y=90)

    min_file_size_label = tkinter.Label(window, text="Min size(MB): ")
    min_file_size_label.place(x=20, y=120)
    min_file_size_var.trace("w", lambda name, index, mode, min_file_size_var=min_file_size_var: callback())
    min_file_size_field = tkinter.Entry(window, width=3, textvariable=min_file_size_var)
    min_file_size_field.place(x=150, y=120)

    max_file_size_label = tkinter.Label(window, text="Max size(MB): ")
    max_file_size_label.place(x=20, y=150)
    max_file_size_var.trace("w", lambda name, index, mode, max_file_size_var=max_file_size_var: callback())
    max_file_size_field = tkinter.Entry(window, width=3, textvariable=max_file_size_var)
    max_file_size_field.place(x=150, y=150)

    cpu_core_count_label = tkinter.Label(window, text="CPU cores to use: ")
    cpu_core_count_label.place(x=20, y=180)
    cpu_core_count_var.trace("w", lambda name, index, mode, cpu_core_count_var=cpu_core_count_var: callback())
    cpu_core_count_field = tkinter.Entry(window, width=3, textvariable=cpu_core_count_var)
    cpu_core_count_field.place(x=150, y=180)

    keep_originals_label = tkinter.Checkbutton(window, text='Keep original pictures', command=clear_path,
                                               variable=keep_originals,
                                               onvalue=1, offvalue=0)
    keep_originals_label.place(x=20, y=207)

    start_button = tkinter.Button(window, text="Start", command=start_new_threads)
    start_button.place(x=20, y=250)

    preview_button = tkinter.Button(window, text="Preview", command=make_preview)
    preview_button.place(x=90, y=250)

    status_label = tkinter.Label(window, width=30, textvariable=status_var, justify=LEFT)
    status_label.place(x=200, y=60)

    radiobutton_en = tkinter.Radiobutton(window, text="EN", variable=selected_language_eng, value=1,
                                         command=update_labels)
    radiobutton_en.place(x=330, y=0)
    radiobutton_ch = tkinter.Radiobutton(window, text="中国人", variable=selected_language_eng, value=0,
                                         command=update_labels)
    radiobutton_ch.place(x=375, y=0)

    help_button = tkinter.Button(window, text="Help", command=open_help_page)
    help_button.place(x=375, y=250)

    #logo = tkinter.Label(image=ImageTk.PhotoImage(PIL.Image.open("logo.png")))
    #logo.place(x=0,y=0)

    window.mainloop()


def open_help_page():
    help_window = Toplevel(window)
    help_window.title(active_dict['help_window'])
    help_window.geometry("300x300+700+200")
    help_window.resizable(False, False)
    text = tkinter.Text(help_window, height=40, width=40, wrap=WORD, bg='#323232')
    scrollbar = tkinter.Scrollbar(help_window, command=text.yview, orient=VERTICAL)

    scrollbar.pack(side=tkinter.RIGHT, fill='y')

    text.pack(side=tkinter.LEFT)
    text.config(yscrollcommand=scrollbar.set)
    text.insert(tkinter.END, active_dict['help_1'] + "\n" + active_dict['help_2'] + "\n"
                + active_dict['help_3'] + "\n" + active_dict['help_4'] + "\n" + active_dict['help_5'] + "\n" +
                active_dict['help_6'] + "\n\n" + active_dict['how_to_use'])
    text.config(state=DISABLED)


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
    global copy_finished_time
    if int(keep_originals.get()) == 1:
        status_var.set("Copying files")
        current_working_directory = Path(path).parent.resolve()
        new_directory_name = str(
            "resized_" + str(os.path.basename(path)) + "_" + str(datetime.datetime.now().strftime("%H_%M_%S")))
        new_directory_path = os.path.join(current_working_directory, new_directory_name)
        shutil.copytree(path, new_directory_path)
        copy_finished_time = time.time()
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
        showinfo("Success", "Preview generated!")
    except Exception as e:
        print(e)
        print("You probably didn't choose a file!")


def valid_folder_path(_path):
    try:
        if os.path.isdir(_path):
            return True
    except:
        return False


def start_new_threads():
    global path
    if not valid_folder_path(path):
        showwarning("Warning", "No folder selected")
        return

    global start_time
    global copy_finished_time
    start_time = time.time()
    copy_finished_time = start_time
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
                status_var.set("Compressing images " + str(percent) + "%")
    thread_finished_counter += 1
    if thread_finished_counter == int(cpu_core_count_var.get()):
        global compression_finished_time
        compression_finished_time = time.time()
        global path
        status_var.set("Compression finished!")
        showinfo("Success", "Image compression finished")
        path = "No root folder selected"
        folder_label_var.set(path)
        print("Total time  " + str(round(compression_finished_time - start_time, 2)) + " s")
        print("File copy   " + str(round(copy_finished_time - start_time, 2)) + " s")
        print("Compression " + str(round(compression_finished_time - copy_finished_time, 2)) + " s")


draw_gui()
