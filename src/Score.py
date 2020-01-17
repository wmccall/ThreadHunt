import wx
import util
# pylint: disable=no-member


class Score(wx.Frame):
    width, _ = util.get_screen_dimensions()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for score_id in util.get_score_ids():
            digit = util.get_char_image("0")
            wx.StaticBitmap(parent=parent_frame, id=util.str_to_int(score_id), bitmap=digit,
                            pos=(self.width - 10 - (index * 35), 10))
            index += 1
