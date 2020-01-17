import wx
import Util
# pylint: disable=no-member


class GameOver(wx.Frame):
    width, height = Util.get_screen_dimensions()
    root_coord = Util.get_root_coord()
    tile_size = Util.get_tile_size()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        index = 1
        for character in "GAME OVER":
            char = Util.get_char_image(character)
            wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("TempElement"), bitmap=char,
                            pos=((self.width/2) + ((index - 5) * 35), self.height/4))
            index += 1

        index = 1
        for character in "SCORE: ":
            char = Util.get_char_image(character)
            wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("TempElement"), bitmap=char,
                            pos=((self.width/2) + ((index - 5) * 35), (self.height/4)+45))
            index += 1

        for character in str(Util.get_score()):
            char = Util.get_char_image(character)
            wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("TempElement"), bitmap=char,
                            pos=((self.width/2) + ((index - 5) * 35), (self.height/4)+45))
            index += 1

        home_png = Util.get_picture("Home320x120.png")
        self.home_button = wx.BitmapButton(parent=parent_frame, id=Util.str_to_int("HomeButton"), bitmap=home_png,
                                           pos=((self.width-320)/2, (self.height/2)+90), style=wx.NO_BORDER)
        self.home_button.Bind(wx.EVT_LEFT_DOWN, self.home_clicked)
        self.home_button.Bind(wx.EVT_ENTER_WINDOW, self.home_hover)

    def home_clicked(self, event):
        if not Util.is_paused():
            wx.FindWindowById(Util.str_to_int("StartButton")).Show()
            wx.FindWindowById(Util.str_to_int("WelcomeSplash")).Show()
            self.home_button.Destroy()
            Util.clean_temp_elements()

    def home_hover(self, event):
        self.home_button.SetWindowStyleFlag(wx.NO_BORDER)
