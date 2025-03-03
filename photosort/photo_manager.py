import os
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener # type: ignore
import shutil

register_heif_opener()

def select_dir(path):
    if not os.path.exists(path):
        raise ValueError("Path does not exist")
    if not os.path.isdir(path):
        raise ValueError("Path is not a directory")
    return path

def create_dir(base_path, categories):
    base_path = select_dir(base_path)
    folders = {}
    for category in categories:
        folder_path = os.path.join(base_path, category)
        os.makedirs(folder_path, exist_ok=True)
        folders[category] = folder_path
    return folders

def get_images(dir_path):
    if not os.path.exists(dir_path):
        return []
    
    images = [f for f in os.listdir(dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', 'heic'))]
    return images
    
def move_image(src, dst):
    if os.path.exists(src):
        shutil.move(src, dst)
        
def delete_image(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

