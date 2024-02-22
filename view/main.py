from .root import Root
from .start_gui import StartPageGUI
from .img_process_gui import ImgProcessGUI

class View:
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}  # type: ignore
        self.curr_frame = ""
        
        self._add_frame(StartPageGUI, "startPage")
        self._add_frame(ImgProcessGUI, "imgProcessPage")
        # self._add_frame(HomeView, "home")

    def _add_frame(self, Frame, name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name: str) -> None:
        frame = self.frames[name]
        frame.tkraise()
        self.curr_frame = name
        
    def get_curr_frame(self):
        return self.curr_frame

    def start_mainloop(self) -> None:
        self.root.mainloop()