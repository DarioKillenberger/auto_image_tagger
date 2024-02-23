import tkinter as tk
from tkinter import ttk, Frame

class ImgProcessGUI(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, minsize=60)
        
        # Image Container
        self.image_container = tk.Label(self, image="")
        self.image_container.grid(row=0, column=0, columnspan=6, padx=20, pady=20, sticky="NESW")
        
        # Image tag display label
        self.tag_label = tk.Label(self, text="", justify="left", background="azure3")
        self.tag_label.grid(row=1, column=0, columnspan=6, padx=20, pady=4, sticky="NESW")
        
         # Image processing progress label
        self.progress_label = tk.Label(self, text="",
                              justify="left")
        self.progress_label.grid(row=2, column=0, padx=4, pady=10, sticky="SW")
        
        # Approve writing to metadata for all images checkbox
        self.label = tk.Label(self, text="Always write to metadata",
                              justify="left")
        self.label.grid(row=2, column=1, padx=4, pady=10, sticky="NESW")
        self.approve_all_checkbox = ttk.Checkbutton(self)
        self.approve_all_checkbox.grid(row=2, column=2, padx=4, pady=10, sticky="NESW")
        
         # Approve writing to metadata Button
        self.approve_button = ttk.Button(self, text="Write to metadata")
        self.approve_button.grid(row=2, column=3, ipady=10, ipadx=10, padx=4, pady=10, sticky="NESW")
        
         # Skip Image Button
        self.skip_button = ttk.Button(self, text="Skip image")
        self.skip_button.grid(row=2, column=4, ipady=10, ipadx=10, padx=4, pady=10, sticky="NESW")
        
        # Abort Button
        self.cancel_button = ttk.Button(self, text="Abort")
        self.cancel_button.grid(row=2, column=5, ipady=10, ipadx=10, padx=(4,20), pady=10, sticky="NESW")
        
       
        
