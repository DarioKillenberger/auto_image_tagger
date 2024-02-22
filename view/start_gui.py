import tkinter as tk
from tkinter import ttk, Frame

class StartPageGUI(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        n_rows = 3
        n_columns = 3
        for i in range(n_rows):
            self.grid_rowconfigure(i, weight=1)
        for i in range(n_columns):
            self.grid_columnconfigure(i, weight=1)

        # Explanation label
        self.label = tk.Label(self, text="This program uses AWS Rekognition to automatically assign tags to images, and then write these into the image metadata using exiftool.\n\nPlease note that this permanently alters the image metadata, so use at your own risk!",
                              justify="left")
        self.label.grid(row=0, columnspan=4, column=0, padx=40, pady=10, sticky="W")
        
        # Choose Image Folder label
        self.folder_label = tk.Label(self, text="", justify="left")
        self.folder_label.grid(row=1, column=0, pady=10, sticky="W", padx=(200,0))

        # Choose Image Folder button
        self.choose_button = ttk.Button(self, text="Choose Image Folder") 
        self.choose_button.grid(row=1, column=0, ipady=10, ipadx=10, sticky="W", pady=10, padx=(40,0))  

        # Start Analysing Images button
        self.analyse_button = ttk.Button(self, text="Start Analysing Images")
        self.analyse_button.grid(row=2, column=3, ipady=10, ipadx=10, padx=20, pady=10, sticky="SE")
        
        # Settings Button
        self.settings_button = ttk.Button(self, text="Settings")
        self.settings_button.grid(row=2, column=2, ipady=10, ipadx=10, pady=10, sticky="SE")