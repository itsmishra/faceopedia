 
from tkinter import *
from PIL import Image,ImageTk
class Preview():
    def __init__(self,location):
        img = Image.open(location)
        img.show()


