from tkinter import Tk


class Root(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Automatic Image Tagger")
        self.geometry("800x400")
        
        n_rows = 1
        n_columns = 1
        for i in range(n_rows):
            self.grid_rowconfigure(i, weight=1)
        for i in range(n_columns):
            self.grid_columnconfigure(i, weight=1)