import boto3
from PIL import Image
import os
import io
import uuid
import mimetypes
import glob
from subprocess import run

# You should change these variables
collection_id='AutoTaggedImages' # doesn't matter, name it what you like
tags_filename="./tags.txt"  # we store all tags assigned to an image in csv format for future reference

path_to_temp="./temp/" # a temp folder, please create
path_to_pictures="J:/Pictures/Camera/2024/Japan Trip/" # the folder where the pictures to process are stored. The code will add metadata tags to all JPG images found in this folder (including in sub-folders)

### 

def limit_img_size(img_filename, img_target_filename, target_filesize, tolerance=5):
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

def resize_image(photo,maxsize,overwrite=False):
    size=os.path.getsize(photo)
    if size>maxsize:
        # print("Have to resize image. It is "+str(size))
        if not overwrite:
            new_filename=path_to_temp+uuid.uuid4().hex+".jpg"
        else:
            new_filename=photo
        limit_img_size(photo,new_filename,maxsize)                
        size=os.path.getsize(new_filename)
        # print("Image resized. New size "+str(size))
        return new_filename
    else:
        return photo

def save_tags(wortliste):
    with open(tags_filename, "w") as f:
        for tags in wortliste:
            tag_row = ""
            for tag in tags:
                tag_row += tag
            tag_row += "\n"
            f.write(tag_row)

# def load_tags():
#     wordlist={}
#     with open(tags_filename) as file:
#         for line in file:
#             tag_line = line.split(",")
#             wordlist[tag_line[0]] = tag_line[1:]
#     return wordlist

def read_filelist(path):
    files = glob.glob(path + '/**/*.[jJ][pP][gG]', recursive=True)
    files = [file.replace('\\', '/') for file in files]
    return files

# call exiftool to add the tags to metadata
def write_tags(labels_final, labels_digikam_final, photo):
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

# Init
client=boto3.client('rekognition')
# translate = boto3.client(service_name='translate', region_name='eu-west-1', use_ssl=True)
mimetypes.init()
labels_final = []
labels_digikam_final = []
labelDatabase = []
approve_all = False

# process all pictures in the folder path_to_pictures
files=read_filelist(path_to_pictures)
print(len(files), " images were found. The script will go through all of them and tag them")

for index, photo in enumerate(files):
    print()
    print("processing image", index+1, "out of", len(files))
    print(photo)
    
    mimestart = mimetypes.guess_type(photo)[0]

    if mimestart != None:
        mimestart = mimestart.split('/')[0]

        if mimestart == 'image': # or mimestart == 'video' - but at the moment we don't analyse video 
            # print("File is an image.")

            photo_work=resize_image(photo,4500000) # we get an working photo of maxsize 4,5MB (AWS maximum is 5MB)

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
            
            # verify user wants to write the tags to the image
            if approve_all != True:
                print('Write labels to image metadata?')
                print('Options:\ny - Approve writing tags to this single image (will ask for confirmation each time)\nya - Approve writing tags to all images (will not ask for confirmation for future images)\nn - Do not write tags to this image\nc - quit script')
                print('Please enter an option: ', end="")
                x = input()
                match x:
                    case "y":
                        write_tags(labels_final, labels_digikam_final, photo)
                    case "ya":
                        write_tags(labels_final, labels_digikam_final, photo)
                        approve_all = True
                    case "n":
                        print("Tags were not written to metadata for this image")
                    case "c":
                        break
            else:
                write_tags(labels_final, labels_digikam_final, photo)
        else:
            print("No media type.")

        # build an array of the labels associated with each image
        labelArr = []
        labelArr.append(photo)
        
        for label in labels_final:
            labelArr.append(","+label)
            
        labelDatabase.append(labelArr)
        
save_tags(labelDatabase)
print("Save translations.")