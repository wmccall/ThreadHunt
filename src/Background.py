import wx
import Util
# pylint: disable=no-member


class Background(wx.Frame):
    width, height = Util.get_screen_dimensions()
    root_coord = Util.get_root_coord()
    tile_size = Util.get_tile_size()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        xcoord = self.root_coord
        ycoord = self.root_coord

        while ycoord < self.height:
            while xcoord < self.width:
                png = Util.get_picture("sky160.png")
                wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("BackgroundTile"), bitmap=png,
                                pos=(xcoord, ycoord))
                xcoord += self.tile_size
            ycoord += self.tile_size
            xcoord = self.root_coord
