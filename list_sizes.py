import os
import pandas as pd



def get_file_size_inMB(file):
    return round(os.stat(file).st_size / 1048576, 1)


def get_file_extension(file):
    return file.split('.')[-1].lower()

files_with_extandsize = []

def list_all_files(path):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            fullpath = os.path.join(subdir, file)
            files_with_extandsize.append([get_file_extension(fullpath), get_file_size_inMB(fullpath)])

path = input("Dir: ")

list_all_files(path)

df = pd.DataFrame(files_with_extandsize,columns=['extension','size'])

print(df.groupby('extension').agg(['sum','count']))