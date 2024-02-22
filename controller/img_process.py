from tkinter import filedialog
from model.tag_my_picture import ImageTagger
from view.main import View
from PIL import Image, ImageTk, ImageOps

class ImgProcessController():  
    
    def __init__(self, model: ImageTagger, view: View) -> None:
        self.model = model # should brackets be here to initalize as object?
        self.view = view
        self.frame = self.view.frames["imgProcessPage"]
        self.start_frame = self.view.frames["startPage"]
        self.img_folder = ""
        self.user_selection = ""
        self.curr_image = ""
        
        self.frame.cancel_button.config(command=self.cancel)
        # self.frame.analyse_button.config(command=self.startImageProcessing)
        # self.frame.settings_button.config(command=self.settings)
        self.frame.bind("<Configure>", lambda e: self.window_resize())
        self.start_frame.analyse_button.bind("<Button-1>", lambda e: self.process_images())
        # self.start_frame.analyse_button.config(command=self.settings)
        print("ran image process controller")

        
    def cancel(self):
        # code for the main function
         self.view.switch("startPage")
    
    def window_resize(self):
        self.set_resized_img() # note: likely not very efficient!!!

        
    def set_resized_img(self):
        resized_img = ImageOps.contain(self.curr_image, (self.frame.winfo_width(), self.frame.winfo_height()))
        resized_img = ImageTk.PhotoImage(resized_img)

        self.frame.image_container.config(image = resized_img)
        self.frame.image=resized_img #need to keep the reference of image to avoid garbage collection !?!?!?
        
    def process_images(self):
        print("process_images method has indeed been called!!!!!!!!!!!")
        files = self.model.read_filelist()
        self.curr_image = Image.open(files[0])
        
        self.set_resized_img()
          
        
        
    #     for index, photo in enumerate(files):
    #         print()
    #         print("processing image", index+1, "out of", len(files))
    #         print(photo)
    
        # verify user wants to write the tags to the image
        # if approve_all != True:
        #     print('Write labels to image metadata?')
        #     print('Options:\ny - Approve writing tags to this single image (will ask for confirmation each time)\nya - Approve writing tags to all images (will not ask for confirmation for future images)\nn - Do not write tags to this image\nc - quit script')
        #     print('Please enter an option: ', end="")
        #     x = input()
        #     match x:
        #         case "y":
        #             self.write_tags(labels_final, labels_digikam_final, photo)
        #         case "ya":
        #             self.write_tags(labels_final, labels_digikam_final, photo)
        #             approve_all = True
        #         case "n":
        #             print("Tags were not written to metadata for this image")
        #         case "c":
        #             break
        # else:
        #     self.write_tags(labels_final, labels_digikam_final, photo)