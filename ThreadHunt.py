import wx
import time
import math
import random
import csv
from datetime import datetime
import kill_process

# pylint: disable=no-member

level = 0
ducks_finished = 0
ducks_spawned = 0
ducks_missed = 0
score = 0
max_ducks_missed = 3

high_scores = {}
game_number = 0

dt_now = datetime.now()
dt_string = dt_now.strftime("%d/%m/%Y %H:%M")

paused = False

total_timers = 0
timers = {}

width = 1600
height = 960
root_coord = 0
tile_size = 160

picture_location = "pictures/"
letter_location = picture_location + "letters/"
char_exten = "35x45.png"


score_ids = ["ZerothDigit", "FirstDigit", "SecondDigit",
             "ThirdDigit", "FourthDigit", "FifthDigit"]

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
           "M", "N", "O",  "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
extras = ["?", "!", "-", ":", " ", "/", "(", ")", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
extras_converted = ["Qu", "Ex", "Da", "Co", "Sp", "Sl", "Lp", "Rp", "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
letter_images = [x + char_exten for x in letters+extras_converted]
letter_dict = dict(zip(letters+extras, letter_images))

level_ids = ["ZerothLevelDigit", "FirstLevelDigit"]
missed_id = "ZerothMissedDigit"

foreground_objects = []

id_strs = ["TempElement", "HighScore"]
global main_frame


def str_to_int(id_str):
    global id_strs
    try:
        location = id_strs.index(id_str)
        return location
    except:
        id_strs.append(id_str)
        return len(id_strs)-1


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Thread Hunt', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Show()


class WelcomeSplash(wx.Frame):
    tick = 1
    pos = [160, 165, 170, 180, 180, 175, 170, 160]

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        png = wx.Image(
            picture_location + "ThreadHunt800x320.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.splash = wx.StaticBitmap(parent=parent_frame, id=str_to_int("WelcomeSplash"), bitmap=png,
                                      pos=((width-800)/2, self.pos[0]))

        self.timer.Start(250)

    def update(self, timer):
        self.splash.MoveXY((width-800)/2, self.pos[self.tick])
        self.splash.Update()
        self.tick = (self.tick+1) % len(self.pos)


class ClickableItems(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.parent_frame = parent_frame

        start_png = wx.Image(
            picture_location + "Start320x120.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.start_button = wx.BitmapButton(parent=parent_frame, id=str_to_int("StartButton"), bitmap=start_png,
                                            pos=((width-320)/2, 540), style=wx.NO_BORDER)
        self.start_button.Bind(wx.EVT_LEFT_DOWN, self.start_clicked)
        self.start_button.Bind(wx.EVT_ENTER_WINDOW, self.start_hover)

        info_png = wx.Image(
            picture_location + "Trophy90.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.info_button = wx.BitmapButton(parent=parent_frame, id=str_to_int("HighScoreButton"), bitmap=info_png,
                                           pos=(10, 10), style=wx.NO_BORDER)
        self.info_button.Bind(wx.EVT_LEFT_DOWN, self.info_clicked)
        self.info_button.Bind(wx.EVT_ENTER_WINDOW, self.info_hover)

    def start_clicked(self, event):
        self.start_button.Hide()
        wx.FindWindowById(str_to_int("WelcomeSplash")).Hide()
        start_game()

    def start_hover(self, event):
        self.start_button.SetWindowStyleFlag(wx.NO_BORDER)

    def info_clicked(self, event):
        global paused, timers
        if paused:
            paused = False
            for index in timers:
                timers[index][0].Start(timers[index][1])
            hide_high_scores()
        else:
            paused = True
            for index in timers:
                timers[index][0].Stop()
            show_high_scores()
        print("info_clicked")

    def info_hover(self, event):
        self.info_button.SetWindowStyleFlag(wx.NO_BORDER)


class Background(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        xcoord = root_coord
        ycoord = root_coord

        while ycoord < height:
            while xcoord < width:
                png = wx.Image(
                    picture_location + "sky160.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                wx.StaticBitmap(parent=parent_frame, id=str_to_int("BackgroundTile"), bitmap=png,
                                pos=(xcoord, ycoord))
                xcoord += tile_size
            ycoord += tile_size
            xcoord = root_coord


class Foreground(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        xcoord = root_coord
        while xcoord < width:
            png = wx.Image(
                picture_location + "grass160.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            tile = wx.StaticBitmap(parent=parent_frame, id=str_to_int("ForegroundTile"), bitmap=png,
                                   pos=(xcoord, height-tile_size-35))
            foreground_objects.append(tile)
            xcoord += tile_size


class Score(wx.Frame):
    global score_ids

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for score_id in score_ids:
            digit = wx.Image(
                letter_location + "Zero35x45.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int(score_id), bitmap=digit,
                            pos=(width - 10 - (index * 35), 10))
            index += 1


class GameOver(wx.Frame):
    global level_ids, score

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for character in "GAME OVER":
            char = wx.Image(
                letter_location + letter_dict[character], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=char,
                            pos=((width/2) + ((index - 5) * 35), height/4))
            index += 1

        index = 1
        for character in "SCORE: ":
            char = wx.Image(
                letter_location + letter_dict[character], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=char,
                            pos=((width/2) + ((index - 5) * 35), (height/4)+45))
            index += 1

        for character in str(score):
            char = wx.Image(
                letter_location + letter_dict[character], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=char,
                            pos=((width/2) + ((index - 5) * 35), (height/4)+45))
            index += 1

        home_png = wx.Image(
            picture_location + "Home320x120.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.home_button = wx.BitmapButton(parent=parent_frame, id=str_to_int("HomeButton"), bitmap=home_png,
                                           pos=((width-320)/2, (height/2)+90), style=wx.NO_BORDER)
        self.home_button.Bind(wx.EVT_LEFT_DOWN, self.home_clicked)
        self.home_button.Bind(wx.EVT_ENTER_WINDOW, self.home_hover)

    def home_clicked(self, event):
        wx.FindWindowById(str_to_int("StartButton")).Show()
        wx.FindWindowById(str_to_int("WelcomeSplash")).Show()
        self.home_button.Destroy()
        clean_temp_elements()

    def home_hover(self, event):
        self.home_button.SetWindowStyleFlag(wx.NO_BORDER)


class Level(wx.Frame):
    global level_ids

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for character in "LEVEL: ":
            char = wx.Image(
                letter_location + letter_dict[character], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=char,
                            pos=((width/2) + ((index - 15) * 35), 10))
            index += 1
        for level_id in reversed(level_ids):
            digit = wx.Image(
                letter_location + "Zero35x45.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int(level_id), bitmap=digit,
                            pos=((width/2) + ((index - 15) * 35), 10))
            index += 1
        increment_level()


class Missed(wx.Frame):
    global missed_id

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for character in "MISSED: ":
            char = wx.Image(
                letter_location + letter_dict[character], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=char,
                            pos=((width/2) + ((index - 1) * 35), 10))
            index += 1

        digit = wx.Image(
            letter_location + "Zero35x45.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(parent=parent_frame, id=str_to_int(missed_id), bitmap=digit,
                        pos=((width/2) + ((index - 1) * 35), 10))
        index += 1

        char = wx.Image(
            letter_location + letter_dict["/"], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=char,
                        pos=((width/2) + ((index - 1) * 35), 10))
        index += 1

        char = wx.Image(
            letter_location + letter_dict[str(max_ducks_missed)], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=char,
                        pos=((width/2) + ((index - 1) * 35), 10))
        index += 1


class Kill(wx.Frame):
    global main_frame

    def __init__(self, parent_frame, pos, program):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        print(pos, program)

        killed = "KILLED"
        prog_upper = program.upper()

        index = 0
        for killed_char in killed:
            letter_img = wx.Image(
                letter_location + letter_dict[killed_char], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=letter_img,
                            pos=((pos[0] + (index * 35), pos[1])))
            index += 1

        index = 0
        for prog_char in prog_upper:

            letter_img = wx.Image(
                letter_location + letter_dict[prog_char], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=str_to_int("TempElement"), bitmap=letter_img,
                            pos=((pos[0] + (index * 35), pos[1]+45)))
            index += 1


class Duck(wx.Frame):
    global main_frame
    dir_int = 2
    directions = [[-1, 0], [-1, 1], [-1, 1], [0, 1],
                  [0, 1], [1, 1], [1, 1], [1, 0]]
    speeds = [[5, 0], [3, 2], [3, 2], [0, 4],
              [0, 4], [2, 3], [2, 3], [5, 0]]
    image = "DuckLU130.png"

    move_queue = 5

    x_location = random.randint(600, width-600)
    y_location = height

    def __init__(self, parent_frame):
        global foreground_objects
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.timer = wx.Timer(self)
        self.timer_number = add_timer([self.timer, 10])
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        duck_png = wx.Image(
            picture_location + self.image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.duck_button = wx.BitmapButton(parent=parent_frame, id=str_to_int("DuckButton"), bitmap=duck_png,
                                           pos=(10, self.y_location), style=wx.NO_BORDER)
        self.duck_button.Bind(wx.EVT_LEFT_DOWN, self.duck_clicked)
        self.duck_button.Bind(wx.EVT_ENTER_WINDOW, self.duck_hover)

        for obj in foreground_objects:
            obj.Destroy()
        foreground_objects = []
        main_frame.AddChild(Foreground(main_frame))

        self.timer.Start(10)

    def update(self, timer):
        global ducks_finished, ducks_missed
        if ducks_missed == max_ducks_missed:
            self.timer.Stop()
            remove_timer(self.timer_number)
            return
        if self.y_location <= -131:
            self.timer.Stop()
            remove_timer(self.timer_number)
            self.duck_button.Destroy()
            print("Flew High")
            ducks_finished += 1
            increment_missed()
            return

        if self.x_location < 300 and self.dir_int < 6:
            change = random.randint(1, 3)
            self.dir_int += change
            self.move_queue = random.randint(1, 2)
        elif self.x_location > width - 300 and self.dir_int > 2:
            change = random.randint(-3, -1)
            self.dir_int += change
            self.move_queue = random.randint(1, 2)

        if self.move_queue == 0:
            change = random.randint(-1, 1)
            self.dir_int += change
            self.move_queue = random.randint(5, 17)

        if self.dir_int < 0:
            self.dir_int = 0
        elif self.dir_int > len(self.directions)-1:
            self.dir_int = len(self.directions)-1

        current_dir = self.directions[self.dir_int]
        self.x_location += self.speeds[self.dir_int][0] * current_dir[0]
        self.y_location -= self.speeds[self.dir_int][1] * current_dir[1]
        # print(
        # f'x: {self.x_location}, y: {self.y_location}, dir: {self.directions[self.dir_int]}, queue: {self.move_queue}')
        if current_dir[1] == 1:
            if current_dir[0] == -1:
                self.image = "DuckLU130.png"
            elif current_dir[0] == 1:
                self.image = "DuckRU130.png"
            else:
                self.image = "DuckU130.png"
        else:
            if current_dir[0] == -1:
                self.image = "DuckL130.png"
            else:
                self.image = "DuckR130.png"
        duck_img = wx.Image(
            picture_location + self.image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.duck_button.SetBitmap(duck_img)
        self.duck_button.MoveXY(self.x_location, self.y_location)
        self.duck_button.Update()
        self.move_queue -= 1

    def duck_clicked(self, event):
        global ducks_finished, paused
        if not paused:
            self.duck_button.Destroy()
            self.timer.Stop()
            process_id, process_name = kill_process.kill_random_user_process(
                dry=False)
            add_and_update_score(int(process_id))
            main_frame.AddChild(
                Kill(main_frame, (self.x_location, self.y_location), process_name))
            update_high_scores_csv()
            ducks_finished += 1

    def duck_hover(self, event):
        self.duck_button.SetWindowStyleFlag(wx.NO_BORDER)


def add_and_update_score(points):
    global score, score_ids, letter_dict

    score += points
    print(score)

    str_score = str(score)[::-1]
    for index in range(0, 6):
        int_digit = 0
        try:
            int_digit = int(str_score[index])
        except:
            pass
        digit_image = wx.Image(
            letter_location + letter_dict[str(int_digit)], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.FindWindowById(str_to_int(
            score_ids[index])).SetBitmap(digit_image)


def increment_level():
    global level, level_ids, letter_dict

    level += 1

    str_level = str(level)[::-1]
    for index in range(0, 2):
        int_digit = 0
        try:
            int_digit = int(str_level[index])
        except:
            pass
        digit_image = wx.Image(
            letter_location + letter_dict[str(int_digit)], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.FindWindowById(str_to_int(
            level_ids[index])).SetBitmap(digit_image)


def increment_missed():
    global ducks_missed, missed_id, letter_dict

    ducks_missed += 1

    digit_image = wx.Image(
        letter_location + letter_dict[str(ducks_missed)], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    wx.FindWindowById(str_to_int(
        missed_id)).SetBitmap(digit_image)


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
    for timer_num in timers:
        del(timers[timer_num])


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

def show_high_scores():
    global main_frame

    img = wx.Image(
            picture_location + "CrossOut90.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    wx.FindWindowById(str_to_int("HighScoreButton")).SetBitmap(img)

    png = wx.Image(
        picture_location + "HighScoreBackground1200x640.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    wx.StaticBitmap(parent=main_frame, id=str_to_int("HighScore"), bitmap=png,
                                    pos=((width-1200)/2, 160))
    index = 1
    for character in "HIGH SCORES":
        char = wx.Image(
            letter_location + letter_dict[character], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(parent=main_frame, id=str_to_int("HighScore"), bitmap=char,
                        pos=((width/2) + ((index - 6) * 35), 170))
        index += 1
    index = 1
    for character in "DEVELOPED BY: WMCCALL":
        char = wx.Image(
            letter_location + letter_dict[character], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(parent=main_frame, id=str_to_int("HighScore"), bitmap=char,
                        pos=((width/2) + ((index - 11) * 35), 750))
        index += 1

    flat_scores = []
    for element in high_scores:
        flat_scores.append(high_scores[element])
    flat_scores.sort()
    count = 0
    for element in reversed(flat_scores):
        if count > 9:
            break
        index = 1
        for character in element[1] + " - " + str(element[0]):
            char = wx.Image(
                letter_location + letter_dict[character], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=main_frame, id=str_to_int("HighScore"), bitmap=char,
                            pos=((width/2) + ((index - 16) * 35), 230 + (45 * count)))
            index += 1
        count += 1

def hide_high_scores():
    clean_high_score_elements()
    img = wx.Image(
            picture_location + "Trophy90.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    wx.FindWindowById(str_to_int("HighScoreButton")).SetBitmap(img)


class Game(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.timer = wx.Timer(self)
        self.timer_number = add_timer([self.timer, 3000])
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(3000)

    def update(self, timer):
        global main_frame, level, ducks_finished, ducks_missed, ducks_spawned, max_ducks_missed
        ducks_for_level = math.ceil(level/2)

        print(f'level: {level}, ducks_finished: {ducks_finished}, ducks_missed: {ducks_missed}, ducks_spawned: {ducks_spawned}, max_ducks_missed: {max_ducks_missed}')

        if ducks_missed == max_ducks_missed:
            self.timer.Stop()
            print("Stopping game")
            remove_timer(self.timer_number)
            update_high_scores_csv()
            remove_all_timers()
            clean_whole_screen()
            main_frame.AddChild(GameOver(main_frame))
            reset_game()
            increment_game()
        elif ducks_spawned < ducks_for_level:
            main_frame.AddChild(Duck(main_frame))
            ducks_spawned += 1
        elif ducks_finished == ducks_for_level:
            ducks_finished = 0
            ducks_spawned = 0
            increment_level()


def start_game():
    global main_frame
    main_frame.AddChild(Score(main_frame))
    main_frame.AddChild(Level(main_frame))
    main_frame.AddChild(Missed(main_frame))
    main_frame.AddChild(Game(main_frame))


def read_high_scores_csv():
    global high_scores, game_number
    with open('highscores.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        game_and_highscore = {}
        for row in csv_reader:
            game_and_highscore[row[0]] = [row[1], row[2]]
            line_count += 1
        print(f'Highscores: {len(game_and_highscore)}\n{game_and_highscore}')
        game_number = len(game_and_highscore)
        high_scores = game_and_highscore


def update_high_score():
    global high_scores, game_number, score, dt_string
    high_scores[game_number] = [score, dt_string]


def update_high_scores_csv():
    global high_scores
    update_high_score()
    with open('highscores.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for index in high_scores:
            writer.writerow([index, high_scores[index][0], high_scores[index][1]])


def reset_game():
    global level, ducks_finished, ducks_spawned, ducks_missed, score, dt_now, dt_string
    level = 0
    ducks_finished = 0
    ducks_spawned = 0
    ducks_missed = 0
    score = 0
    dt_now = datetime.now()
    dt_string =dt_now.strftime("%d/%m/%Y %H:%M")


def increment_game():
    global game_number
    game_number += 1


if __name__ == "__main__":
    global main_frame
    read_high_scores_csv()
    app = wx.App()
    main_frame = MainFrame()
    main_frame.SetDimensions(0, 0, width, height)
    main_frame.AddChild(Background(main_frame))
    main_frame.AddChild(WelcomeSplash(main_frame))
    main_frame.AddChild(ClickableItems(main_frame))
    main_frame.AddChild(Foreground(main_frame))
    app.MainLoop()
