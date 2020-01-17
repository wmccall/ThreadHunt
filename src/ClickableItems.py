import wx
import util


from Score import Score
from Level import Level
from Missed import Missed
from Game import Game
# pylint: disable=no-member


class ClickableItems(wx.Frame):
    width, _ = util.get_screen_dimensions()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.parent_frame = parent_frame

        start_png = util.get_picture("Start320x120.png")
        self.start_button = wx.BitmapButton(parent=parent_frame, id=util.str_to_int("StartButton"), bitmap=start_png,
                                            pos=((self.width-320)/2, 540), style=wx.NO_BORDER)
        self.start_button.Bind(wx.EVT_LEFT_DOWN, self.start_clicked)
        self.start_button.Bind(wx.EVT_ENTER_WINDOW, self.start_hover)

        info_png = util.get_picture("Trophy90.png")
        self.info_button = wx.BitmapButton(parent=parent_frame, id=util.str_to_int("HighScoreButton"), bitmap=info_png,
                                           pos=(10, 10), style=wx.NO_BORDER)
        self.info_button.Bind(wx.EVT_LEFT_DOWN, self.info_clicked)
        self.info_button.Bind(wx.EVT_ENTER_WINDOW, self.info_hover)

    def start_clicked(self, event):
        if not util.is_paused():
            self.start_button.Hide()
            wx.FindWindowById(util.str_to_int("WelcomeSplash")).Hide()
            self.start_game(self.parent_frame)

    def start_hover(self, event):
        self.start_button.SetWindowStyleFlag(wx.NO_BORDER)

    def info_clicked(self, event):
        if util.is_paused():
            util.start_timers()
            util.hide_high_scores()
        else:
            util.stop_timers()
            util.show_high_scores(self.parent_frame)

    def info_hover(self, event):
        self.info_button.SetWindowStyleFlag(wx.NO_BORDER)

    def start_game(self, main_frame):
        main_frame.AddChild(Score(main_frame))
        main_frame.AddChild(Level(main_frame))
        main_frame.AddChild(Missed(main_frame))
        main_frame.AddChild(Game(main_frame))
