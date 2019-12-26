import tkinter as tk
from PIL import Image, ImageTk

width = 1600
height = 960
root_coord = 0
tile_size = 160

class InanimateScreen(tk.Frame):
    def __init__(self, master=None):    
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill="both", expand=True)    

        sky_render = ImageTk.PhotoImage(Image.open("sky160.png"))
        xcoord = root_coord
        ycoord = root_coord
        while ycoord < height:
            while xcoord < width:
                img = tk.Label(self, image=sky_render, borderwidth=0, highlightthickness=0)
                img.image = sky_render
                img.place(x=xcoord, y=ycoord)
                xcoord += tile_size
            ycoord += tile_size
            xcoord = root_coord

        grass_render = ImageTk.PhotoImage(Image.open("grass160.png"))
        xcoord = root_coord
        while xcoord < width:
            img = tk.Label(self, image=grass_render, borderwidth=0, highlightthickness=0)
            img.image = grass_render
            img.place(x=xcoord, y=height-tile_size)
            xcoord += tile_size
        # self.label = tk.Label(self, text="Hello, World!")
        # self.label.pack(padx=20, pady=20)
        
if __name__ == "__main__":
    root = tk.Tk()

    main = InanimateScreen(root)
    # main.pack(fill="both", expand=True)

    root.wm_title("Thread Hunt")
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    root.mainloop()