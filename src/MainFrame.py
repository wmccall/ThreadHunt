import wx
# pylint: disable=no-member


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Thread Hunt', style=wx.DEFAULT_FRAME_STYLE &
                         ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Show()
