# TODO: refactor, split to components, use interface.
# Currently only ran with console. Alpha Variant

# IMPORT
# ============================
import os
import shutil

# VARIABLES
# ============================
root_dir = os.getcwd()
copy_to_dir = 'E:\Music'
count = 0

# FUNCTIONS
# ============================
def main():
    global count
    for band in os.listdir(root_dir):
        directory = os.path.join(root_dir, band)
        if os.path.isdir(directory):
            count += 1

            print("\n--------------------------------------")
            print("%s) Working on BAND %s\n--------------------------------------"%(count, band))

            print("Clean up started!\n--------------------------------------")
            iterrate(directory, cleanup)
            print("Copy started!\n--------------------------------------")
            iterrate(directory, copy)

    print("\n--------------------------------------")
    print("Proccess ended!\n--------------------------------------")

def iterrate(directory, next_function):
    for album in os.listdir(directory):
        sub_directory = os.path.join(directory, album)
        if os.path.isdir(sub_directory):
            print("Working on ALBUM %s\n--------------------------------------"%(album))
            next_function(sub_directory)

def cleanup(directory):
    for folder in os.listdir(directory):
        sub_directory = os.path.join(directory, folder)
        if os.path.isdir(sub_directory):
            if auto_delete(folder):
                answer = 'y'
                print("Auto >> DELETING >>>>  %s  <<<<   "%(folder))
            elif auto_skip(folder):
                answer = 'n'
                print("Auto >> SKIPPING >>>>  %s  <<<<   "%(folder))
            else:
                answer = input("Has folder >>>>  %s  <<<<, DELETE? Enter for skip, 'y' for yes: "%(folder))

            if answer.lower() == 'y':
                delete(sub_directory)

def copy(directory):
    copy_dir = directory.replace(root_dir, copy_to_dir)
    if(os.path.exists(copy_dir)):
        if(get_dir_size(directory) == get_dir_size(copy_dir)):
            return
        delete(copy_dir, True)

    shutil.copytree(directory, copy_dir)

def get_dir_size(path='.', total=0):
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def auto_delete(folder):
    autodelete = ["Covers", "Cover", "Artwork", "Scans"]
    for text in autodelete:
        if(folder.lower().startswith(text.lower())):
            return True

    return False

def auto_skip(folder):
    autoskip = ["Disc 1", "Disc 2", "Disc 3", "CD1", "CD2", "CD3", "CD 1", "CD 2", "CD 3"]
    for text in autoskip:
        if(folder.lower().startswith(text.lower())):
            return True

    return False

def delete(file_path, silent=False):
    if(silent == False): print('Deleting %s'%(file_path))

    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s'%(file_path, e))

    if(silent == False): print('--------------------------------------')


# START
# ============================
main()