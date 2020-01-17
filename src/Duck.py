import wx
import random
import util

from Foreground import Foreground
from Kill import Kill
# pylint: disable=no-member


class Duck(wx.Frame):
    dir_int = 2
    directions = [[-1, 0], [-1, 1], [-1, 1], [0, 1],
                  [0, 1], [1, 1], [1, 1], [1, 0]]
    speeds = [[5, 0], [3, 2], [3, 2], [0, 4],
              [0, 4], [2, 3], [2, 3], [5, 0]]
    image = "DuckLU130.png"

    move_queue = 5

    width, height = util.get_screen_dimensions()

    x_location = random.randint(600, width-600)
    y_location = height

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.parent_frame = parent_frame

        self.timer = wx.Timer(self)
        self.timer_number = util.add_timer([self.timer, 10])
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        duck_png = util.get_picture(self.image)
        self.duck_button = wx.BitmapButton(parent=parent_frame, id=util.str_to_int("DuckButton"), bitmap=duck_png,
                                           pos=(10, self.y_location), style=wx.NO_BORDER)
        self.duck_button.Bind(wx.EVT_LEFT_DOWN, self.duck_clicked)
        self.duck_button.Bind(wx.EVT_ENTER_WINDOW, self.duck_hover)

        util.destroy_foreground_objects()
        parent_frame.AddChild(Foreground(parent_frame))

        self.timer.Start(10)

    def update(self, timer):
        if util.get_ducks_missed() == util.get_max_ducks_missed():
            self.timer.Stop()
            util.remove_timer(self.timer_number)
            return
        if self.y_location <= -131:
            self.timer.Stop()
            util.remove_timer(self.timer_number)
            self.duck_button.Destroy()
            util.increment_ducks_finished()
            util.increment_missed()
            return

        if self.x_location < 300 and self.dir_int < 6:
            change = random.randint(1, 3)
            self.dir_int += change
            self.move_queue = random.randint(1, 2)
        elif self.x_location > self.width - 300 and self.dir_int > 2:
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
        duck_img = util.get_picture(self.image)
        self.duck_button.SetBitmap(duck_img)
        self.duck_button.Move(x=self.x_location, y=self.y_location)
        self.duck_button.Update()
        self.move_queue -= 1

    def duck_clicked(self, event):
        if not util.is_paused():
            self.duck_button.Destroy()
            self.timer.Stop()
            process_id, process_name = util.kill_random_user_process(
                dry=False)
            util.add_and_update_score(int(process_id))
            self.parent_frame.AddChild(
                Kill(self.parent_frame, (self.x_location, self.y_location), process_name))
            util.update_high_scores_csv()
            util.increment_ducks_finished()

    def duck_hover(self, event):
        self.duck_button.SetWindowStyleFlag(wx.NO_BORDER)
