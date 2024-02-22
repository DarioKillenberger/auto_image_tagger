from model.tag_my_picture import ImageTagger
from view.main import View

from .start_screen import StartScreenController
from .img_process import ImgProcessController

class Controller:
    def __init__(self, model: ImageTagger, view: View) -> None:
        self.view = view
        self.model = model
        self.start_screen_controller = StartScreenController(model, view)
        self.img_process_controller = ImgProcessController(model, view)

    def start(self) -> None:
        self.view.start_mainloop()