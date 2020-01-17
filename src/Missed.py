import wx
import Util
# pylint: disable=no-member


class Missed(wx.Frame):
    width, height = Util.get_screen_dimensions()
    root_coord = Util.get_root_coord()
    tile_size = Util.get_tile_size()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for character in "MISSED: ":
            char = Util.get_char_image(character)
            wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("TempElement"), bitmap=char,
                            pos=((self.width/2) + ((index - 1) * 35), 10))
            index += 1

        digit = Util.get_char_image("0")
        wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int(Util.get_missed_id()), bitmap=digit,
                        pos=((self.width/2) + ((index - 1) * 35), 10))
        index += 1

        char = Util.get_char_image("/")
        wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("TempElement"), bitmap=char,
                        pos=((self.width/2) + ((index - 1) * 35), 10))
        index += 1

        char = Util.get_char_image(str(Util.get_max_ducks_missed()))
        wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("TempElement"), bitmap=char,
                        pos=((self.width/2) + ((index - 1) * 35), 10))
        index += 1
