from tkinter import BooleanVar
from model.tag_my_picture import ImageTagger
from view.main import View
from PIL import Image, ImageTk, ImageOps
import threading

class ImgProcessController():  
    
    def __init__(self, model: ImageTagger, view: View) -> None:
        self.model = model # should brackets be here to initalize as object?
        self.view = view
        self.frame = self.view.frames["imgProcessPage"]
        self.start_frame = self.view.frames["startPage"]
        
        self.write_all = BooleanVar()
        self.always_get_tags = BooleanVar()
        
        self.get_tags_temp = BooleanVar()
        self.write_tags_temp = BooleanVar()
        
        self.curr_tags = ""
        self.img_folder = ""
        self.images = ""
        self.curr_image = ""
        self.curr_index = 0
    
        self.frame.cancel_button.config(command=self.cancel)
        self.frame.bind("<Configure>", lambda e: self.window_resize())
        self.start_frame.analyse_button.bind("<Button-1>", lambda e: threading.Thread(target=self.control_process_loop).start())
        
        self.frame.write_all_checkbox.config(variable = self.write_all)
        self.frame.get_all_tags_checkbox.config(variable = self.always_get_tags)
        self.frame.get_tags_button.bind("<Button-1>", lambda e: self.handle_tags_button())
        self.frame.write_metadata_button.bind("<Button-1>", lambda e: self.handle_metadata_button())
        self.frame.skip_button.bind("<Button-1>", lambda e: self.skip_image())
      

    def cancel(self):
        # code for the main function
        self.curr_image = ""
        self.curr_tags = ""
        self.write_all.set(False)
        self.update_tag_label()
        self.view.switch("startPage")
    
    def window_resize(self):
        self.set_resized_img() # note: likely not very efficient!!!
        self.frame.tag_label.config(wraplength=self.frame.winfo_width()-80)

    def set_resized_img(self):
        if self.curr_image != "":
            # self.curr_tags = ""
            resized_img = ImageOps.contain(Image.open(self.curr_image), (self.frame.winfo_width(), self.frame.winfo_height()))
            resized_img = ImageTk.PhotoImage(resized_img)

            self.frame.image_container.config(image = resized_img)
            self.frame.image=resized_img #need to keep the reference of image to avoid garbage collection !?!?!?
            self.frame.tag_label.config(wraplength=self.frame.winfo_width()-80)
            self.frame.update()
        
    def handle_tags_button(self):
        self.get_tags_temp = True
        self.control_process_loop()
    
    def handle_metadata_button(self):
        self.write_tags_temp = True
        self.control_process_loop()
    
    # Threading helper function
    def run_in_thread(self, func):
        thread = threading.Thread(target=func)
        thread.start()
        thread.join()
        
    
    # Main control loop. Determines what gets run based on the checkboxes/buttons pressed
    def control_process_loop(self):
        self.process_image()
        
        if self.write_all.get() == True and self.always_get_tags.get() == True:
            for index, image in enumerate(self.images):
                if self.write_all.get() != True or self.always_get_tags.get() != True:
                    break
                else:
                    print("control process loop approved ran")
                    self.curr_index = index
                    
                    self.run_in_thread(self.get_image_tags)
                    self.run_in_thread(self.write_to_metadata)
                    self.next_image()
        
        elif (self.always_get_tags.get() == True or self.get_tags_temp == True) and (self.write_all.get() == True or self.write_tags_temp == True):
            self.get_image_tags()
            self.write_to_metadata()
            self.write_tags_temp = False
            self.get_tags_temp == False
            self.next_image()
            
        else:
            if (self.always_get_tags.get() == True or self.get_tags_temp == True) and self.curr_tags == "":
                self.get_image_tags()
                self.get_tags_temp = False
            
            if (self.write_all.get() == True or self.write_tags_temp == True) and self.curr_tags != "":
                self.write_to_metadata()
                self.write_tags_temp = False
                self.next_image()
            elif self.write_tags_temp == True:
                self.start_frame.create_popup("Error", "Please generate tags first 1")
                self.write_tags_temp = False
    
    # Switches to next image and calls the control_process_loop again
    def next_image(self):
        if self.curr_index < len(self.images)-1:
            self.curr_index += 1
            self.curr_tags = ""
            self.update_tag_label()
            threading.Thread(target=self.process_image).start()
            
        else:
            print("Completed. All images processed")
            self.start_frame.create_popup("Completed", "All images have been processed")
            
    
    # Read and resize the image for viewing in the application
    def process_image(self):
        if self.model.get_directory() == "":
            self.start_frame.create_popup("Error", "Please select an image folder first")
        else:
            print("process_images method has indeed been called!!!!!!!!!!!")
            self.view.switch("imgProcessPage")
            self.images = self.model.read_filelist() #TODO: Don't read this each time???
            self.frame.progress_label.config(text="Image " + str(self.curr_index+1) + "/" + str(len(self.images)))
            self.curr_image = self.images[self.curr_index]
            self.set_resized_img()
            
    # Update the image label tag in the UI to show the currently generated tags
    def update_tag_label(self):
        if self.curr_tags == "":
            self.frame.tag_label.config(text="")
        else:
            self.frame.tag_label.config(text=self.curr_tags["individual_labels"])
            
    # TODO: Make the tags label a textbox, where user can edit the tags. To do this, strip the squiggly brackets and quotes from the tags list, then update the 
    # local copy (in the controller) of the tagslist everytime the user makes an edit. When writing metadata to file, take the user edited code (do some basic
    # error checking before writing ie. no spaces within tags!?)
            
    # Gets image tags and calls the update_tag_label method to display them
    def get_image_tags(self):
        if self.curr_tags == "":
            self.curr_tags = self.generate_tags(self.curr_image)
            self.update_tag_label()
    
    # Calls the model to write get the tags from the Amazon Rekognition API
    def generate_tags(self, img_path):
        return self.model.get_image_tags(img_path)
    
    # Calls the model to write the tags to the image metadata
    def write_to_metadata(self):
        if self.curr_image != "" and self.curr_tags != "":
            print("The information being passed in the write_to_metadata method is: ", self.curr_tags["individual_labels"], self.curr_tags["digikam_labels"], self.curr_image)
            self.model.write_tags(self.curr_tags["individual_labels"], self.curr_tags["digikam_labels"], self.curr_image)
        elif self.curr_tags == "":
            self.start_frame.create_popup("Error", "Please generate tags first") 
            
    def skip_image(self):
        self.model.set_runState(False)
        self.next_image()
        
        
    #     for index, photo in enumerate(files):
    #         print()
    #         print("processing image", index+1, "out of", len(files))
    #         print(photo)
    
        # verify user wants to write the tags to the image
        # if write_all != True:
        #     print('Write labels to image metadata?')
        #     print('Options:\ny - Approve writing tags to this single image (will ask for confirmation each time)\nya - Approve writing tags to all images (will not ask for confirmation for future images)\nn - Do not write tags to this image\nc - quit script')
        #     print('Please enter an option: ', end="")
        #     x = input()
        #     match x:
        #         case "y":
        #             self.write_tags(labels_final, labels_digikam_final, photo)
        #         case "ya":
        #             self.write_tags(labels_final, labels_digikam_final, photo)
        #             write_all = True
        #         case "n":
        #             print("Tags were not written to metadata for this image")
        #         case "c":
        #             break
        # else:
        #     self.write_tags(labels_final, labels_digikam_final, photo)