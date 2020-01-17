import wx
import util
# pylint: disable=no-member


class Level(wx.Frame):
    width, _ = util.get_screen_dimensions()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for character in "LEVEL: ":
            char = util.get_char_image(character)
            wx.StaticBitmap(parent=parent_frame, id=util.str_to_int("TempElement"), bitmap=char,
                            pos=((self.width/2) + ((index - 15) * 35), 10))
            index += 1
        for level_id in reversed(util.get_level_ids()):
            digit = util.get_char_image("0")
            wx.StaticBitmap(parent=parent_frame, id=util.str_to_int(level_id), bitmap=digit,
                            pos=((self.width/2) + ((index - 15) * 35), 10))
            index += 1
        util.increment_level()
