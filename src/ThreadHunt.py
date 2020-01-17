import wx
import time
import math
import random
import csv
from datetime import datetime
import util
from MainFrame import MainFrame
from WelcomeSplash import WelcomeSplash
from ClickableItems import ClickableItems
from Background import Background
from Foreground import Foreground

# pylint: disable=no-member

width, height = util.get_screen_dimensions()
root_coord = util.get_root_coord()
tile_size = util.get_tile_size()

global main_frame

if __name__ == "__main__":
    global main_frame
    util.read_high_scores_csv()
    app = wx.App()
    main_frame = MainFrame()
    main_frame.SetSize(width=width, height=height)
    main_frame.AddChild(Background(main_frame))
    main_frame.AddChild(WelcomeSplash(main_frame))
    main_frame.AddChild(ClickableItems(main_frame))
    main_frame.AddChild(Foreground(main_frame))
    app.MainLoop()
