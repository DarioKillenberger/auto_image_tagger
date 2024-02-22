import tkinter as tk
from tkinter import ttk, Frame

class ImgProcessGUI(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        n_rows = 3
        n_columns = 3
        for i in range(n_rows):
            self.grid_rowconfigure(i, weight=1)
        for i in range(n_columns):
            self.grid_columnconfigure(i, weight=1)
        
        # Image Container
        self.image_container = tk.Label(self, image="")
        self.image_container.grid(row=1, column=0, pady=20, padx=20, sticky="NESW")
        
        # Cancel Button
        self.cancel_button = ttk.Button(self, text="Cancel")
        self.cancel_button.grid(row=2, column=2, ipady=10, ipadx=10, padx=20, pady=10, sticky="SE")
        
