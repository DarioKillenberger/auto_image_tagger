# auto_image_tagger
Automatically tag objects in images using aws rekognition, and then write this to metadata using exiftool.

The image tags are written to the IPTC 'Keywords' field, the XMP 'Subject' field, as well as the digiKam 'Tags List' field, where the tags are formatted in hierarchical order (for the other tag fields, each level in the hierarchy is simply treated as it's own keyword)

Please note that this is my first time using Tkinter and also my first time using Python in a while, so the code is naturally not perfect - not to mention I'm still in university, so please don't be too harsh on my code xD, it's likely far from perfect.

That being said, if you have any improvements or tips for me, feel free to email me at dario13ad@posteo.de.

## Known Problems/Planned improvements
- Currenly, only JPG files are processed, due to metadata format differences for other file formats
- The AWS Rekognize api is called for each image, even when it is immediately skipped by the user. This is not very cost effective
- There is currently no loading indicator while waiting to receive image tags from api
- Currently, there is no way to edit the tags generated for an image. The image tags field should be user editable so they can make corrections before writing to image.
- There should be a setting to choose which metadata fields the tags should be written to
- Temp  files are currently written to the program directory. Look into storing these in AppData/Local/Temp or something like that, and also make program clear the folder on closing
- Abort/closing program currently does not quit any already started operations (eg if the tags have already been requested from the api, this will finish and the tags field will be populated even while hidden from the user!?)

# Credits
Backend logic is based on code from tag-my-picture by Andreas Streim: https://github.com/streiman/tag-my-picture

MVC code structure based on template by Nazmul Ahsan: https://github.com/AhsanShihab/tkinter-multiframe-mvc/tree/master


## Instructions for use

1. This program relies on the AWS Rekognition API. In order to access this, you need to create an AWS account and set up the AWS CLI and SDK on your computer. In order to do this, please follow the steps outlined in https://docs.aws.amazon.com/rekognition/latest/dg/getting-started.html. Note that while there is a free trial period, costs *may* apply (eg if the limits are exceeded, or an existing AWS account is used). 
2. Once the AWS api has been set up and you have provided the credentials to a user account with permissions to access Rekognition, you can start the application
3. Once in the application, choose the folder containing the images you would like to add metadata to. Note: All JPG images in that folder (or subfolders) will have tags generateD, even if you choose to skip writing tags to some images. It is therefore recommended to ensure the chosen folder only contains images you would like to add tags to, in order to avoid unneccesary calls to the aws api.
4. After selecting the folder, click 'Start Analysing Images'. The first image will be compressed and sent to AWS Rekognition to generate its tags. Once the tags are generated, they will be displayed underneath the image.
5. You now have 3 buttons and 1 checkbox to select:
    - The 'Write to metadata' button will write the currently displayed tags into the image metadata, and then load the next image and associated tags.
    - The 'Skip image' button will skip not write the tags metadata into the current image, and will instead load the next image and associated tags right away.
    - The 'Abort' button will wait for any currently in progress operations to complete (eg if tags have already been requested for an image, these will finish loading), and then cancel all future operations and return to the start screen
    - When the 'Always write to metadata' checkbox is checked, the program will not wait for user confirmation before writing tags to metadata, and will instead automatically process and write metadata for all images in the folder. On the other hand, if the checkbox is unchecked, the program will pause after retrieving the tags for each image, and request user input to either write those tags to metadata or skip.
6. The counter in the bottom left shows the current progress. At this stage, there is no confirmation notification once all images have been processed, so once the counter reaches the end and the tags have been written to metadata, the program has processed all images in the folder and is finished.