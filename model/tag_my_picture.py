import boto3
from PIL import Image
import os
import io
import uuid
import glob
from subprocess import run

# You should change these variables
collection_id='AutoTaggedImages' # doesn't matter, name it what you like
tags_filename="../data/tags.txt"  # we store all tags assigned to an image in csv format for future reference

path_to_temp="./temp/" # a temp folder, please create
# path_to_pictures="J:/Pictures/Camera/2020" # the folder where the pictures to process are stored. The code will add metadata tags to all JPG images found in this folder (including in sub-folders)

class ImageTagger:
    
    def __init__(self):
        # Setting image size limits to support up to 350mb (useful for some very big panoramas)
        Image.MAX_IMAGE_PIXELS = 350000000
        self.labelDatabase = []
        self.directory_path = ""
        
    def set_directory(self, directory_path):
        self.directory_path = directory_path
        
    def get_directory(self):
        return self.directory_path

    def limit_img_size(self, img_filename, img_target_filename, target_filesize, tolerance=5):
        # code from: https://stackoverflow.com/questions/52940369/is-it-possible-to-resize-an-image-by-its-bytes-rather-than-width-and-height
        img = img_orig = Image.open(img_filename)
        # resize image to be maximum 10000 pixels, to comply with aws pixel limits
        img_orig.thumbnail((10000,10000), Image.LANCZOS)
        aspect = img.size[0] / img.size[1]

        while True:
            with io.BytesIO() as buffer:
                img.save(buffer, format="JPEG")
                data = buffer.getvalue()
            filesize = len(data)    
            size_deviation = filesize / target_filesize
            # print("size: {}; factor: {:.3f}".format(filesize, size_deviation))

            if size_deviation <= (100 + tolerance) / 100:
                # filesize fits
                with open(img_target_filename, "wb") as f:
                    f.write(data)
                break
            else:
                # filesize not good enough => adapt width and height
                # use sqrt of deviation since applied both in width and height
                new_width = img.size[0] / size_deviation**0.5    
                new_height = new_width / aspect
                # resize from img_orig to not lose quality
                img = img_orig.resize((int(new_width), int(new_height)))

    def resize_image(self, photo,maxsize,overwrite=False):
        size=os.path.getsize(photo)
        if size>maxsize:
            # print("Have to resize image. It is "+str(size))
            if not overwrite:
                new_filename=path_to_temp+uuid.uuid4().hex+".jpg"
            else:
                new_filename=photo
            self.limit_img_size(photo,new_filename,maxsize)                
            size=os.path.getsize(new_filename)
            # print("Image resized. New size "+str(size))
            return new_filename
        else:
            return photo

    def save_tags(self, wortliste):
        with open(tags_filename, "w") as f:
            for tags in wortliste:
                tag_row = ""
                for tag in tags:
                    tag_row += tag
                tag_row += "\n"
                f.write(tag_row)

    def read_filelist(self):
        files = glob.glob(self.directory_path + '/**/*.[jJ][pP][gG]', recursive=True)
        files = [file.replace('\\', '/') for file in files]
        print(len(files), " images were found. The script will go through all of them and tag them")
        return files

    # call exiftool to add the tags to metadata
    def write_tags(self, labels_final, labels_digikam_final, photo):
        cmdline=""
        for label in set(labels_final):
            # add commands to add all tags (parent and tag) to the IPTC 'Keywords' and XMP 'Subject' fields
            cmdline=cmdline+" -keywords-="+label+" -keywords+="+label+" -Subject="+label+" -Subject="+label
            
        for digiKam_label in set(labels_digikam_final):
            # add commands to add all tags (preserving parent/tag hierarchy) to the digiKam 'TagsList' XMP field
                cmdline=cmdline+" -XMP-digiKam:TagsList-="+digiKam_label+" -XMP-digiKam:TagsList+="+digiKam_label    

        if cmdline!="":
            # Note: I was having issues with spaces in filepaths using the previous method, hence updated to use subprocess to send the command
            run('exiftool -r -overwrite_original'+cmdline+' "'+photo+'"', check=True)

    def get_image_tags(self, photo):
        print("The image received by the model is", photo)
        # Init
        client=boto3.client('rekognition')
        labels_final = []
        labels_digikam_final = []
        photo_work=self.resize_image(photo,4500000) # we get an working photo of maxsize 4,5MB (AWS maximum is 5MB)

        # we ask Amazon Rekognition for the labels of the picture, with a maximum of 10 labels, and minimum confidence of 65
        with open(photo_work, 'rb') as image:
            response = client.detect_labels(Image={'Bytes': image.read()},  MaxLabels=10, MinConfidence=65)

        # There are labels and parents, we take them both for our exif keywords. Convert any tags which have spaces to be joined with underscore instead
        label_lst = []
        for label in response['Labels']:
            label_lst.append(label['Name'].replace(" ", "_"))
            
            for parents in label['Parents']:
                label_lst.append(parents['Name'].replace(" ", "_"))

        # For the digiKam TagsList, we would like to preserve parent/label hierarchy, and put them all under the autoGenerated tag
        digiKam_TagsList = []
        for label in response['Labels']:
            label_hierarchy = "autoGenerated/"
            for parents in label['Parents']:
                label_hierarchy += (parents['Name'].replace(" ", "_"))+"/"
            
            label_hierarchy += label['Name'].replace(" ", "_")
            digiKam_TagsList.append(label_hierarchy)
            
        # make the results a set to get every label only once
        labels_final=set(label_lst)
        labels_digikam_final=set(digiKam_TagsList)

        # print out labels for user information
        print("labels are: ", labels_final)
        print("hierarchical digikam labels are: ", labels_digikam_final)
        
        # build an array of the labels associated with each image
        labelArr = []
        labelArr.append(photo)
        
        for label in labels_final:
            labelArr.append(","+label)
            
        self.labelDatabase.append(labelArr)
        
        return {"individual_labels": labels_final, "digikam_labels": labels_digikam_final}
    
    def write_to_metadata(self, labels_final, labels_digikam_final, img_path): # TODO: OBSOLETE??
        self.write_tags(labels_final, labels_digikam_final, img_path)
        
    def save_tags_to_file(self):
        self.save_tags(self.labelDatabase)
        print("Save translations.")