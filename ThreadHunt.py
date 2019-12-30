import wx
import time

width = 1600
height = 960
root_coord = 0
tile_size = 160


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Thread Hunt', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Show()


class WelcomeSplash(wx.Frame):
    tick = 1
    pos = [160, 165, 170, 180, 180, 175, 170, 160]

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        png = wx.Image(
            "ThreadHunt800x320.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.splash = wx.StaticBitmap(parent=parent_frame, id=1, bitmap=png,
                                      pos=((width-800)/2, self.pos[0]))

        self.timer.Start(250)

    def update(self, timer):
        self.splash.MoveXY((width-800)/2, self.pos[self.tick])
        self.splash.Update()
        self.tick = (self.tick+1) % len(self.pos)


class ClickableItems(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.parent_frame = parent_frame

        start_png = wx.Image(
            "Start320x120.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.start_button = wx.BitmapButton(parent=parent_frame, id=2, bitmap=start_png,
                                            pos=((width-320)/2, 540), style=wx.NO_BORDER)
        self.start_button.Bind(wx.EVT_LEFT_DOWN, self.start_clicked)
        self.start_button.Bind(wx.EVT_ENTER_WINDOW, self.start_hover)

        info_png = wx.Image(
            "Info9.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.info_button = wx.BitmapButton(parent=parent_frame, id=2, bitmap=info_png,
                                           pos=(10, 10), style=wx.NO_BORDER)
        self.info_button.Bind(wx.EVT_LEFT_DOWN, self.info_clicked)
        self.info_button.Bind(wx.EVT_ENTER_WINDOW, self.info_hover)

        settings_png = wx.Image(
            "Settings9.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.settings_button = wx.BitmapButton(parent=parent_frame, id=2, bitmap=settings_png,
                                               pos=(130, 10), style=wx.NO_BORDER)
        self.settings_button.Bind(wx.EVT_LEFT_DOWN, self.settings_clicked)
        self.settings_button.Bind(wx.EVT_ENTER_WINDOW, self.settings_hover)

    def start_clicked(self, event):
        self.start_button.Destroy()

    def start_hover(self, event):
        self.start_button.SetWindowStyleFlag(wx.NO_BORDER)

    def info_clicked(self, event):
        self.info_button.Destroy()

    def info_hover(self, event):
        self.info_button.SetWindowStyleFlag(wx.NO_BORDER)

    def settings_clicked(self, event):
        self.settings_button.Destroy()

    def settings_hover(self, event):
        self.settings_button.SetWindowStyleFlag(wx.NO_BORDER)


class Background(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        xcoord = root_coord
        ycoord = root_coord

        while ycoord < height:
            while xcoord < width:
                png = wx.Image(
                    "sky160.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                wx.StaticBitmap(parent=parent_frame, id=-1, bitmap=png,
                                pos=(xcoord, ycoord))
                xcoord += tile_size
            ycoord += tile_size
            xcoord = root_coord


class Foreground(wx.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        xcoord = root_coord
        while xcoord < width:
            png = wx.Image(
                "grass160.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(parent=parent_frame, id=-1, bitmap=png,
                            pos=(xcoord, height-tile_size-35))
            xcoord += tile_size


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.SetDimensions(0, 0, width, height)
    frame.AddChild(Background(frame))
    frame.AddChild(WelcomeSplash(frame))
    frame.AddChild(ClickableItems(frame))
    frame.AddChild(Foreground(frame))
    app.MainLoop()
