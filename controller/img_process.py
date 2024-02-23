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
        self.user_selection = ""
        
        self.curr_tags = ""
        self.img_folder = ""
        self.images = ""
        self.curr_image = ""
        self.curr_index = 0
    
        self.frame.cancel_button.config(command=self.cancel)
        # self.frame.analyse_button.config(command=self.startImageProcessing)
        # self.frame.settings_button.config(command=self.settings)
        self.frame.bind("<Configure>", lambda e: self.window_resize())
        self.start_frame.analyse_button.bind("<Button-1>", lambda e: self.process_image())
        self.frame.approve_button.bind("<Button-1>", lambda e: self.write_to_metadata())
        self.frame.skip_button.bind("<Button-1>", lambda e: self.next_image())
        # self.start_frame.analyse_button.config(command=self.settings)

        
    def cancel(self):
        # code for the main function
        self.curr_image = ""
        self.curr_tags = ""
        self.update_tag_label()
        self.view.switch("startPage")
    
    def window_resize(self):
        self.set_resized_img() # note: likely not very efficient!!!
        self.frame.tag_label.config(wraplength=self.frame.winfo_width()-80)

        
    def set_resized_img(self):
        if self.curr_image != "":
            self.curr_tags = ""
            resized_img = ImageOps.contain(Image.open(self.curr_image), (self.frame.winfo_width(), self.frame.winfo_height()))
            resized_img = ImageTk.PhotoImage(resized_img)

            self.frame.image_container.config(image = resized_img)
            self.frame.image=resized_img #need to keep the reference of image to avoid garbage collection !?!?!?
            self.frame.tag_label.config(wraplength=self.frame.winfo_width()-80)
            self.frame.update()
        
    def process_image(self):
        if self.model.get_directory() == "":
            print("please select an image folder first!!") # Make this a hidden label which becomes visible, just above the process screen button
        else:
            print("process_images method has indeed been called!!!!!!!!!!!")
            self.view.switch("imgProcessPage")
            self.images = self.model.read_filelist()
            self.frame.progress_label.config(text="Image " + str(self.curr_index+1) + "/" + str(len(self.images)))
            self.curr_image = self.images[self.curr_index]
            self.set_resized_img()
            
            self.curr_tags = self.generate_tags(self.images[self.curr_index])
            self.update_tag_label()
            
    def update_tag_label(self):
        if self.curr_tags == "":
            self.frame.tag_label.config(text="")
        else:
            self.frame.tag_label.config(text=self.curr_tags["individual_labels"])
            
    # TODO: Make the tags label a textbox, where user can edit the tags. To do this, strip the squiggly brackets and quotes from the tags list, then update the 
    # local copy (in the controller) of the tagslist everytime the user makes an edit. When writing metadata to file, take the user edited code (do some basic
    # error checking before writing ie. no spaces within tags!?)
            
            
    def generate_tags(self, img_path):
        return self.model.get_image_tags(img_path)
    
    def write_to_metadata(self):
        if self.curr_image != "" and self.curr_tags != "":
            self.model.write_tags(self.curr_tags["individual_labels"], self.curr_tags["digikam_labels"], self.curr_image)
            self.next_image()
                
    def next_image(self):
        if self.curr_index < len(self.images)-1:
            self.curr_index += 1
            self.curr_tags = ""
            self.update_tag_label()
            self.process_image()
        else:
            print("Completed. All images processed")
    
        
        
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