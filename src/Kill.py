import wx
import Util
# pylint: disable=no-member


class Kill(wx.Frame):
    def __init__(self, parent_frame, pos, program):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        prog_upper = program.upper()

        index = 0
        for killed_char in "KILLED":
            letter_img = Util.get_char_image(killed_char)
            wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("TempElement"), bitmap=letter_img,
                            pos=((pos[0] + (index * 35), pos[1])))
            index += 1

        index = 0
        for prog_char in prog_upper:
            letter_img = Util.get_char_image(prog_char)
            wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("TempElement"), bitmap=letter_img,
                            pos=((pos[0] + (index * 35), pos[1]+45)))
            index += 1
