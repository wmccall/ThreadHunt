import wx
import util
# pylint: disable=no-member


class WelcomeSplash(wx.Frame):
    tick = 1
    pos = [160, 165, 170, 180, 180, 175, 170, 160]
    width, height = util.get_screen_dimensions()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        png = util.get_picture("ThreadHunt800x320.png")
        self.splash = wx.StaticBitmap(parent=parent_frame, id=util.str_to_int("WelcomeSplash"), bitmap=png,
                                      pos=((self.width-800)/2, self.pos[0]))

        self.timer.Start(250)

    def update(self, timer):
        self.splash.Move(x=(self.width-800)/2, y=self.pos[self.tick])
        self.splash.Update()
        self.tick = (self.tick+1) % len(self.pos)
