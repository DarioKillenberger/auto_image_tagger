from tkinter import filedialog
from model.tag_my_picture import ImageTagger
from view.main import View

class StartScreenController():  
    
    def __init__(self, model: ImageTagger, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["startPage"]
        self.img_folder = ""
        
        self.frame.choose_button.config(command=self.choose_folder)
        self.frame.settings_button.config(command=self.settings)
        self.frame.bind("<Configure>", lambda e: self.window_resize())
        print("ran start screen controller")
        self.view.switch("startPage")
        
        # Note: The 'Start Analysing Images' button is handled by the img_process controller, as it starts that controller's logic
        
    def choose_folder(self):
        folder_selected = filedialog.askdirectory()
        self.model.set_directory(folder_selected)
        self.frame.folder_label.config(text=folder_selected)
        
    def settings(self):
        print("Settings...")
        # Placeholder for actual image analysis logic
        
    def window_resize(self):
        print("called resize")
        self.frame.label.config(wraplength=self.frame.winfo_width()-80)