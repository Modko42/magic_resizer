from PIL import Image
import os


def get_file_size_inMB(file):
    return str(os.stat(file).st_size / 1000000)


def get_folder_size(root):
    size = 0
    for path, dirs, files in os.walk(root):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp) / 1048576
    return round(size, 2)


path = ""

path = input("Specify the root dir\nLike C:/dir/pics/\nRoot dir: ")
custom_quality = int(input("Quality: "))
min_file_size = input("Min file size to convert(in MB): ")
max_file_size = input("Max file size to convert(in MB): ")

original_folder_size = get_folder_size(path)

files_fullpath = []
counter = 0
for subdir, dirs, files in os.walk(path):
    for file in files:
        file_size = get_file_size_inMB(subdir + '/' + file)
        if min_file_size < file_size < max_file_size:
            files_fullpath.append(subdir + '/' + file)

print("Files found: " + str(len(files_fullpath)))


def resize():
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
                im.save(f + '.jpg', 'JPEG', quality=custom_quality)
            except:
                print("Problem with image: " + str(file))
            i = i + 1
        if os.path.isfile(file) and file.split('.')[-1].lower() == 'bmp':
            try:
                im = Image.open(file)
                f, e = os.path.splitext(file)
                im.save(f + '.jpg', 'JPEG', quality=custom_quality)
                im.close()
                os.remove(file)
            except:
                print("Problem with image: " + str(file))
            i = i + 1


resize()

resized_folder_size = get_folder_size(path)
print("Original total size: " + str(original_folder_size) + " MB")
print("Resized  total size: " + str(resized_folder_size) + " MB")
