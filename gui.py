import tkinter as tk
from tkinter import ttk, filedialog

class ImageTagger(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Automatic Image Tagger")
        self.geometry("800x400")
        
        n_rows = 4
        n_columns = 3
        for i in range(n_rows):
            self.grid_rowconfigure(i, weight =1)
        for i in range(n_columns):
            self.grid_columnconfigure(i, weight =1)
        

        # Explanation label
        label = tk.Label(self, text="This program uses AWS Rekognition to automatically assign tags to images, and then write these into the image metadata using exiftool.\n\nPlease note that this permanently alters the image metadata, so use at your own risk!", justify="left")
        label.grid(row=1, columnspan=3, column=1, padx=40, pady=10)

        # Choose Image Folder button
        choose_button = ttk.Button(self, text="Choose Image Folder", command=self.choose_folder)
        choose_button.grid(row=2, column=1, ipady=10, ipadx=10, sticky="W", padx=40, pady=10)

        # Start Analysing Images button
        analyse_button = ttk.Button(self, text="Start Analysing Images", command=self.analyse_images)
        analyse_button.grid(row=3, column=3, ipady=10, ipadx=10, padx=20, pady=10, sticky="SE")
        
        # Settings Button
        settings_button = ttk.Button(self, text="Settings", command=self.settings)
        settings_button.grid(row=3, column=2, ipady=10, ipadx=10, pady=10, sticky="SE")

    def choose_folder(self):
        folder_selected = filedialog.askdirectory()
        return folder_selected

    def analyse_images(self):
        print("Analyse images")
        # Placeholder for actual image analysis logic
        
    def settings(self):
        print("Analyse images")
        # Placeholder for actual image analysis logic

# Create an instance of our app and run it
app = ImageTagger()
app.mainloop()
