import wx
import subprocess
import signal
import random

# pylint: disable=no-member

#
# COMMON FIELDS
#####################################

picture_location = "src/images/"
letter_location = picture_location + "characters/"
char_exten = "35x45.png"

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
           "M", "N", "O",  "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
extras = ["?", "!", "-", ":", " ", "/",
          "(", ")", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
extras_converted = ["Qu", "Ex", "Da", "Co", "Sp", "Sl", "Lp", "Rp", "Zero",
                    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
letter_images = [x + char_exten for x in letters+extras_converted]
letter_dict = dict(zip(letters+extras, letter_images))

id_strs = ["TempElement", "HighScore"]


#
#  USER UTILS
#####################################

def get_current_user():
    processes = subprocess.Popen(['whoami'], stdout=subprocess.PIPE)
    out, _ = processes.communicate()
    out_decoded = (out.decode('UTF-8')).strip()
    return out_decoded


#
#  PROCESS UTILS
#####################################

def get_pocesseses():
    processes = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE)
    out, _ = processes.communicate()
    out_decoded = out.decode('UTF-8')
    process_for_user = {}
    count = 0
    for row in out_decoded.split('\n'):
        if count != 0:
            split_row = ' '.join(row.split()).split()
            if len(split_row) >= 2:
                user = split_row[0]
                pid = split_row[1]
                if process_for_user.get(user) == None:
                    process_for_user[user] = []
                process_for_user[user].append(pid)
        count += 1
    return process_for_user


def get_current_user_processes():
    return get_pocesseses()[get_current_user()]


def get_all_processes():
    flat = []
    processes = get_pocesseses()
    for key in processes.keys():
        flat += processes[key]
    return flat


#
# KILL UTILS
#####################################

def kill_random_user_process(dry=False):
    user_process = get_current_user_processes()
    num_processes = len(user_process)
    random_process = random.randint(0, num_processes-1)
    which_process = subprocess.Popen(
        ['ps', '-p', user_process[random_process]], stdout=subprocess.PIPE)
    which_out, _ = which_process.communicate()
    if not dry:
        processes = subprocess.Popen(
            ['kill', user_process[random_process]], stdout=subprocess.PIPE)
        out, _ = processes.communicate()
        _ = (out.decode('UTF-8')).strip()
    process_name = ' '.join(which_out.decode(
        'UTF-8').split('\n')[1].split()).split()[3]
    return (user_process[random_process], process_name)


def kill_random_any_process(dry=False):
    process = get_all_processes()
    num_processes = len(process)
    random_process = random.randint(0, num_processes-1)
    which_process = subprocess.Popen(
        ['ps', '-p', process[random_process]], stdout=subprocess.PIPE)
    _, _ = which_process.communicate()
    if not dry:
        processes = subprocess.Popen(
            ['kill', process[random_process]], stdout=subprocess.PIPE)
        out, _ = processes.communicate()
        _ = (out.decode('UTF-8')).strip()


#
# IMAGE UTILS
#####################################

def get_char_image(char):
    image = letter_dict.get(char.upper())
    if image is None:
        image = letter_dict["-"]
    return get_bitmap(letter_location + image)


def get_picture(name):
    return get_bitmap(picture_location + name)


def get_bitmap(location):
    return wx.Image(location, wx.BITMAP_TYPE_PNG).ConvertToBitmap()


#
# ID UTILS
#####################################

def str_to_int(id_str):
    global id_strs
    try:
        location = id_strs.index(id_str)
        return location
    except:
        id_strs.append(id_str)
        return len(id_strs)-1
