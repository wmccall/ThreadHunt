import wx
import math
import Util

from Duck import Duck
from GameOver import GameOver
# pylint: disable=no-member


class Game(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.parent_frame = parent_frame
        self.timer = wx.Timer(self)
        self.timer_number = Util.add_timer([self.timer, 3000])
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(3000)

    def update(self, timer):
        ducks_for_level = math.ceil(Util.get_level()/2)

        if Util.get_ducks_missed() == Util.get_max_ducks_missed():
            self.timer.Stop()
            Util.remove_timer(self.timer_number)
            Util.update_high_scores_csv()
            Util.remove_all_timers()
            Util.clean_whole_screen()
            self.parent_frame.AddChild(GameOver(self.parent_frame))
            Util.reset_game()
            Util.increment_game()
        elif Util.get_ducks_spawned() < ducks_for_level:
            self.parent_frame.AddChild(Duck(self.parent_frame))
            Util.increment_ducks_spawned()
        elif Util.if_all_ducks_spawned_for_level(ducks_for_level):
            Util.reset_ducks()
            Util.increment_level()
