import wx
import time
import random

width = 1600
height = 960
root_coord = 0
tile_size = 160

picture_location = "pictures/"
number_location = picture_location + "numbers/"

score = 0
score_ids = ["ZerothDigit", "FirstDigit", "SecondDigit",
             "ThirdDigit", "FourthDigit", "FifthDigit"]
score_images = ["Zero35x45.png", "One35x45.png", "Two35x45.png", "Three35x45.png", "Four35x45.png",
                "Five35x45.png", "Six35x45.png", "Seven35x45.png", "Eight35x45.png", "Nine35x45.png"]

foreground_objects = []

id_strs = []
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
            picture_location + "Info9.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.info_button = wx.BitmapButton(parent=parent_frame, id=str_to_int("InfoButton"), bitmap=info_png,
                                           pos=(10, 10), style=wx.NO_BORDER)
        self.info_button.Bind(wx.EVT_LEFT_DOWN, self.info_clicked)
        self.info_button.Bind(wx.EVT_ENTER_WINDOW, self.info_hover)

        settings_png = wx.Image(
            picture_location + "Settings9.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.settings_button = wx.BitmapButton(parent=parent_frame, id=str_to_int("SettingsButton"), bitmap=settings_png,
                                               pos=(130, 10), style=wx.NO_BORDER)
        self.settings_button.Bind(wx.EVT_LEFT_DOWN, self.settings_clicked)
        self.settings_button.Bind(wx.EVT_ENTER_WINDOW, self.settings_hover)

    def start_clicked(self, event):
        self.start_button.Hide()
        wx.FindWindowById(str_to_int("WelcomeSplash")).Hide()
        start_game()

    def start_hover(self, event):
        self.start_button.SetWindowStyleFlag(wx.NO_BORDER)

    def info_clicked(self, event):
        print("info_clicked")

    def info_hover(self, event):
        self.info_button.SetWindowStyleFlag(wx.NO_BORDER)

    def settings_clicked(self, event):
        print("settings_clicked")

    def settings_hover(self, event):
        self.settings_button.SetWindowStyleFlag(wx.NO_BORDER)


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
    global score_ids, foreground_objects

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for score_id in score_ids:
            digit = wx.Image(
                number_location + "Zero35x45.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            digit_bitmap = wx.StaticBitmap(parent=parent_frame, id=str_to_int(score_id), bitmap=digit,
                                           pos=(width - 10 - (index * 35), 10))
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
        if self.y_location == -200:
            self.timer.Stop()
            self.duck_button.Destroy()
            print("Flew High")
            return

        if self.x_location < 300 and self.dir_int < 6:
            print("l ", end="")
            change = random.randint(1, 3)
            self.dir_int += change
            self.move_queue = random.randint(1, 2)
        elif self.x_location > width - 300 and self.dir_int > 2:
            print("r ", end="")
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

        print(f'dir_int: {self.dir_int}, ', end="")
        current_dir = self.directions[self.dir_int]
        self.x_location += self.speeds[self.dir_int][0] * current_dir[0]
        self.y_location -= self.speeds[self.dir_int][1] * current_dir[1]
        print(
            f'x: {self.x_location}, y: {self.y_location}, dir: {self.directions[self.dir_int]}, queue: {self.move_queue}')
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
        self.duck_button.Destroy()
        self.timer.Stop()
        add_and_update_score(1000)

    def duck_hover(self, event):
        self.duck_button.SetWindowStyleFlag(wx.NO_BORDER)


def add_and_update_score(points):
    global score, score_ids, score_images

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
            number_location + score_images[int_digit], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.FindWindowById(str_to_int(
            score_ids[index])).SetBitmap(digit_image)


def start_game():
    global main_frame
    main_frame.AddChild(Score(main_frame))

    main_frame.AddChild(Duck(main_frame))


if __name__ == "__main__":
    global main_frame
    app = wx.App()
    main_frame = MainFrame()
    main_frame.SetDimensions(0, 0, width, height)
    main_frame.AddChild(Background(main_frame))
    main_frame.AddChild(WelcomeSplash(main_frame))
    main_frame.AddChild(ClickableItems(main_frame))
    main_frame.AddChild(Foreground(main_frame))
    app.MainLoop()
