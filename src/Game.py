import wx
import math
import util

from Duck import Duck
from GameOver import GameOver
# pylint: disable=no-member


class Game(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.parent_frame = parent_frame
        self.timer = wx.Timer(self)
        self.timer_number = util.add_timer([self.timer, 3000])
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(3000)

    def update(self, timer):
        ducks_for_level = math.ceil(util.get_level()/2)

        if util.get_ducks_missed() == util.get_max_ducks_missed():
            self.timer.Stop()
            util.remove_timer(self.timer_number)
            util.update_high_scores_csv()
            util.remove_all_timers()
            util.clean_whole_screen()
            self.parent_frame.AddChild(GameOver(self.parent_frame))
            util.reset_game()
            util.increment_game()
        elif util.get_ducks_spawned() < ducks_for_level:
            self.parent_frame.AddChild(Duck(self.parent_frame))
            util.increment_ducks_spawned()
        elif util.if_all_ducks_spawned_for_level(ducks_for_level):
            util.reset_ducks()
            util.increment_level()
