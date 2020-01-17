import wx
import Util
# pylint: disable=no-member


class Foreground(wx.Frame):
    width, height = Util.get_screen_dimensions()
    root_coord = Util.get_root_coord()
    tile_size = Util.get_tile_size()

    def __init__(self, parent_frame):
        super().__init__(parent=None, title='', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        xcoord = self.root_coord
        while xcoord < self.width:
            png = Util.get_picture("grass160.png")
            tile = wx.StaticBitmap(parent=parent_frame, id=Util.str_to_int("ForegroundTile"), bitmap=png,
                                   pos=(xcoord, self.height-self.tile_size-35))
            Util.add_foreground_object(tile)
            xcoord += self.tile_size
