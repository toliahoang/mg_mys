import PIL.Image
# import Image
# import ImageTk
from tkinter import *
from PIL import ImageTk
import os


class ExampleApp(Frame):
    def __init__(self,master, path):
        Frame.__init__(self,master=None)
        self.path = path
        self.x = self.y = 0
        self.im = PIL.Image.open(self.path)
        width, height = self.im.size
        self.canvas = Canvas(self,  cursor="cross", width=width, height=height)

        self.sbarv=Scrollbar(self,orient=VERTICAL)
        self.sbarh=Scrollbar(self,orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)
        self.sbarv.grid(row=0,column=1,stick=N+S)
        self.sbarh.grid(row=1,column=0,sticky=E+W)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

        self.start_x = None
        self.start_y = None

        self.wazil,self.lard=self.im.size
        self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

    def on_button_press(self, event):
        # save mouse drag start position
        width, height = self.im.size
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')
        x0,y0,x1,y1 = self.canvas.bbox(self.rect)
        print(f"{x0},{y0}, {x1}, {y1}")
        print(f"delta_form {x0},{y0},{x1-x0},{y1-y0}")
        with open(os.path.split(self.path)[0] +'/'+'coord.txt','w') as fh:
            fh.write(f"{width},{height}\n")
            fh.write(f"{x0},{y0},{x1-x0},{y1-y0}")

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if event.x > 0.9*w:
            self.canvas.xview_scroll(1, 'units')
        elif event.x < 0.1*w:
            self.canvas.xview_scroll(-1, 'units')
        if event.y > 0.9*h:
            self.canvas.yview_scroll(1, 'units')
        elif event.y < 0.1*h:
            self.canvas.yview_scroll(-1, 'units')

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def get_coordinate(self):
        pass

    def on_button_release(self, event):
        pass


def draw_reg_get_coord(path):
    root=Tk()
    try:
        open(path,'r').close()
    except IOError:
        raise IOError("problem with input file")
    img = PIL.Image.open(path)
    w,h = img.size
    print(f"w-h: {w},{h}")
    root.geometry(f"{w}x{h}")
    root.grid_columnconfigure(0, weight=1)

    app = ExampleApp(root, path)
    app.pack()
    root.mainloop()


# if __name__ == "__main__":
#     root=Tk()
#     try:
#         open(path,'r').close()
#     except IOError:
#         raise IOError("problem with input file")
#     img = PIL.Image.open(path)
#     w,h = img.size
#     print(f"w-h: {w},{h}")
#     root.geometry(f"{w}x{h}")
#     root.grid_columnconfigure(0, weight=1)
#
#     app = ExampleApp(root, path)
#     app.pack()
#     root.mainloop()
