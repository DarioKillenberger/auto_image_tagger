from model.tag_my_picture import ImageTagger
from view.main import View
from controller.main import Controller

def main():
    # code for the main function
    print()
    

if __name__ == "__main__":
    model = ImageTagger()
    view = View()
    controller = Controller(model, view)
    controller.start()