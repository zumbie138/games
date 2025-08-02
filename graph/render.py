from PIL import Image, ImageTk
import os

class RenderImage():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        IMAGE_PATH = os.path.join(BASE_DIR, 'images', 'demon_exodus_initial_screen.png')