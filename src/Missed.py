import wx
import util
# pylint: disable=no-member


class Missed(wx.Frame):
    width, height = util.get_screen_dimensions()
    root_coord = util.get_root_coord()
    tile_size = util.get_tile_size()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for character in "MISSED: ":
            char = util.get_char_image(character)
            wx.StaticBitmap(parent=parent_frame, id=util.str_to_int("TempElement"), bitmap=char,
                            pos=((self.width/2) + ((index - 1) * 35), 10))
            index += 1

        digit = util.get_char_image("0")
        wx.StaticBitmap(parent=parent_frame, id=util.str_to_int(util.get_missed_id()), bitmap=digit,
                        pos=((self.width/2) + ((index - 1) * 35), 10))
        index += 1

        char = util.get_char_image("/")
        wx.StaticBitmap(parent=parent_frame, id=util.str_to_int("TempElement"), bitmap=char,
                        pos=((self.width/2) + ((index - 1) * 35), 10))
        index += 1

        char = util.get_char_image(str(util.get_max_ducks_missed()))
        wx.StaticBitmap(parent=parent_frame, id=util.str_to_int("TempElement"), bitmap=char,
                        pos=((self.width/2) + ((index - 1) * 35), 10))
        index += 1
