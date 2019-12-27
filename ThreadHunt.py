import wx
# from PIL import Image, ImageTk

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
    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        png = wx.Image(
            "ThreadHunt800x320.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(parent=parent_frame, id=-1, bitmap=png,
                        pos=((width-800)/2, 160))


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
    frame.AddChild(Foreground(frame))
    app.MainLoop()
