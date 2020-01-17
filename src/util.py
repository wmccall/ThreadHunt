import wx
import subprocess
import signal
import random
import time
import csv
from datetime import datetime


from Score import Score
from Level import Level
from Missed import Missed
from Game import Game

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

score_ids = ["ZerothDigit", "FirstDigit", "SecondDigit",
             "ThirdDigit", "FourthDigit", "FifthDigit", "SixthDigit", "SeventhDigit"]


level_ids = ["ZerothLevelDigit", "FirstLevelDigit"]
missed_id = "ZerothMissedDigit"

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


def get_score_ids():
    return score_ids


def get_level_ids():
    return level_ids


def get_missed_id():
    return missed_id


#
# SCREEN UTILS
#####################################

foreground_objects = []
width = 1600
height = 960
root_coord = 0
tile_size = 160


def get_screen_dimensions():
    global width, height
    return (width, height)


def get_root_coord():
    return root_coord


def get_tile_size():
    return tile_size


def destroy_foreground_objects():
    global foreground_objects

    for obj in foreground_objects:
        obj.Destroy()
        foreground_objects = []


def add_foreground_object(foreground_object):
    global foreground_objects

    foreground_objects.append(foreground_object)


def hide_high_scores():
    clean_high_score_elements()
    img = get_picture("Trophy90.png")
    wx.FindWindowById(str_to_int("HighScoreButton")).SetBitmap(img)


def show_high_scores(main_frame):

    img = get_picture("CrossOut90.png")
    wx.FindWindowById(str_to_int("HighScoreButton")).SetBitmap(img)

    png = get_picture("HighScoreBackground1200x640.png")
    wx.StaticBitmap(parent=main_frame, id=str_to_int("HighScore"), bitmap=png,
                    pos=((width-1200)/2, 160))
    index = 1
    for character in "HIGH SCORES":
        char = get_char_image(character)
        wx.StaticBitmap(parent=main_frame, id=str_to_int("HighScore"), bitmap=char,
                        pos=((width/2) + ((index - 6) * 35), 170))
        index += 1
    index = 1
    for character in "DEVELOPED BY: WMCCALL":
        char = get_char_image(character)
        wx.StaticBitmap(parent=main_frame, id=str_to_int("HighScore"), bitmap=char,
                        pos=((width/2) + ((index - 11) * 35), 750))
        index += 1

    flat_scores = []
    for element in high_scores:
        flat_scores.append(high_scores[element])

    sorted_scores = sorted(
        flat_scores, key=lambda cur_score: int(cur_score[0]))
    count = 0
    for element in reversed(sorted_scores):
        if count > 9:
            break
        index = 1
        for character in element[1] + " - " + str(element[0]):
            char = get_char_image(character)
            wx.StaticBitmap(parent=main_frame, id=str_to_int("HighScore"), bitmap=char,
                            pos=((width/2) + ((index - 16) * 35), 230 + (45 * count)))
            index += 1
        count += 1


def clean_temp_elements():
    element = wx.FindWindowById(str_to_int("TempElement"))
    while element is not None:
        element.Destroy()
        element = wx.FindWindowById(str_to_int("TempElement"))


def clean_high_score_elements():
    element = wx.FindWindowById(str_to_int("HighScore"))
    while element is not None:
        element.Destroy()
        element = wx.FindWindowById(str_to_int("HighScore"))


def clean_ducks_elements():
    element = wx.FindWindowById(str_to_int("DuckButton"))
    while element is not None:
        element.Destroy()
        element = wx.FindWindowById(str_to_int("DuckButton"))


def clean_whole_screen():
    for id in level_ids:
        wx.FindWindowById(str_to_int(id)).Destroy()
    for id in score_ids:
        wx.FindWindowById(str_to_int(id)).Destroy()
    wx.FindWindowById(str_to_int(missed_id)).Destroy()

    clean_temp_elements()
    clean_ducks_elements()

#
# TIMER UTILS
#####################################


paused = False
total_timers = 0
timers = {}


def start_timers():
    global paused, timers
    paused = False
    for index in timers:
        timers[index][0].Start(timers[index][1])


def stop_timers():
    global paused, timers
    paused = True
    for index in timers:
        timers[index][0].Stop()


def add_timer(timer):
    global timers, total_timers
    total_timers += 1
    timers[total_timers] = timer
    return total_timers


def remove_timer(timer_number):
    global timers
    del(timers[timer_number])


def remove_all_timers():
    global timers
    try:
        for timer_num in timers:
            del(timers[timer_num])
    except:
        pass


def is_paused():
    return paused


#
# GAME UTILS
#####################################

level = 0
ducks_finished = 0
ducks_spawned = 0
ducks_missed = 0
score = 0
max_ducks_missed = 3

game_number = 0

dt_now = datetime.now()
dt_string = dt_now.strftime("%d/%m/%Y %H:%M")

high_scores = {}


def start_game(main_frame):
    main_frame.AddChild(Score(main_frame))
    main_frame.AddChild(Level(main_frame))
    main_frame.AddChild(Missed(main_frame))
    main_frame.AddChild(Game(main_frame))


def increment_level():
    global level

    level += 1

    str_level = str(level)[::-1]
    for index in range(0, 2):
        int_digit = 0
        try:
            int_digit = int(str_level[index])
        except:
            pass
        digit_image = get_char_image(str(int_digit))
        wx.FindWindowById(str_to_int(
            get_level_ids()[index])).SetBitmap(digit_image)


def get_level():
    return level


def increment_ducks_finished():
    global ducks_finished
    ducks_finished += 1


def increment_missed():
    global ducks_missed, missed_id

    ducks_missed += 1

    digit_image = get_char_image(str(ducks_missed))
    wx.FindWindowById(str_to_int(
        get_missed_id())).SetBitmap(digit_image)


def reset_game():
    global level, ducks_finished, ducks_spawned, ducks_missed, score, dt_now, dt_string
    level = 0
    ducks_finished = 0
    ducks_spawned = 0
    ducks_missed = 0
    score = 0
    dt_now = datetime.now()
    dt_string = dt_now.strftime("%d/%m/%Y %H:%M")


def increment_game():
    global game_number
    game_number += 1


def get_score():
    return score


def get_max_ducks_missed():
    return max_ducks_missed


def get_ducks_missed():
    return ducks_missed


def get_ducks_spawned():
    return ducks_spawned


def if_all_ducks_spawned_for_level(ducks_for_level):
    return ducks_finished == ducks_for_level


def reset_ducks():
    global ducks_finished, ducks_spawned

    ducks_finished = 0
    ducks_spawned = 0


def increment_ducks_spawned():
    global ducks_spawned
    ducks_spawned += 1


def add_and_update_score(points):
    global score

    score += points

    str_score = str(score)[::-1]
    score_ids = get_score_ids()
    for index in range(0, len(score_ids)):
        int_digit = 0
        try:
            int_digit = int(str_score[index])
        except:
            pass
        digit_image = get_char_image(str(int_digit))
        wx.FindWindowById(str_to_int(
            score_ids[index])).SetBitmap(digit_image)


def read_high_scores_csv():
    global high_scores, game_number
    with open('highscores.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        game_and_highscore = {}
        for row in csv_reader:
            game_and_highscore[row[0]] = [row[1], row[2]]
            line_count += 1
        game_number = len(game_and_highscore)
        high_scores = game_and_highscore


def update_high_score():
    global high_scores, game_number, score, dt_string
    high_scores[game_number] = [str(score), dt_string]


def update_high_scores_csv():
    global high_scores
    update_high_score()
    with open('highscores.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for index in high_scores:
            writer.writerow(
                [index, high_scores[index][0], high_scores[index][1]])
