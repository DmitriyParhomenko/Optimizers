import os
import uuid
from PIL import Image


SEARCH_DIR = '../unedited_images/' 
DEST_DIR = '../edited_images/'

def setup_directories(search, destination):
    """Set up search and destination directories."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    search_path = os.path.join(current_dir, search)
    dest_path = os.path.join(current_dir, destination)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    return search_path, dest_path

def save_image(image, path, filename):
    """Convert to RGB and save the image."""
    image = image.convert('RGB')
    image.save(os.path.join(path, filename))

def calculate_new_dimensions(old_width, old_height, new_width):
    new_height = int(old_height * (new_width / old_width))
    return new_width, new_height



def process_images(search, destination, process_function, file_suffix=''):
    search_path, dest_path = setup_directories(search, destination)

    for file in os.listdir(search_path):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            try:
                img_path = os.path.join(search_path, file)
                with Image.open(img_path) as img:
                    processed_imgs = process_function(img)
                    if processed_imgs:
                        # Check if the function returned a tuple of images
                        if isinstance(processed_imgs, tuple):
                            # Save each image separately
                            for i, processed_img in enumerate(processed_imgs, start=1):
                                save_image(processed_img, dest_path, f'{file}_{i}_{file}')
                        else:
                            # Single image
                            save_image(processed_imgs, dest_path, f'{file_suffix}_{file}')
            except IOError as e:
                print(f"An error occurred with {file}: {e}")


def change_image_format(search, destination, format="jpg"):
    search_path, dest_path = setup_directories(search, destination)
    for file in os.listdir(search_path):
        if file.lower().endswith(('.jpg', '.png', '.jpeg', 'webp')):
            try:
                img_path = os.path.join(search_path, file)
                with Image.open(img_path) as img:
                    # Convert the image to the desired format (RGB for jpg)
                    converted_img = img.convert('RGB')

                    # Extract the filename without extension
                    file_without_ext = os.path.splitext(file)[0]
                    
                    # Save the image with the new format
                    new_img_path = os.path.join(dest_path, f'{file_without_ext}.{format}')
                    converted_img.save(new_img_path)

            except IOError as e:
                print(f"An error occurred with {file}: {e}")
                

def resize_image(img):
    new_width = DEFAULT_BNA_WIDTH
    if(new_width > img.width):
        print('New width must be smaller than current width')
        # return None
    return img.resize(calculate_new_dimensions(*img.size, new_width))


def split_image_vertically(img):
    width, height = img.size
    half_width = width // 2
    left = img.crop((0, 0, half_width, height))
    right = img.crop((half_width, 0, width, height))
    return left, right

def split_image_horizontally(img):
    width, height = img.size
    half_height = height // 2
    top = img.crop((0, 0, width, half_height))
    bottom = img.crop((0, half_height, width, height))
    return top, bottom

def custom_crop_height(img, crop_height=1120):
    width, height = img.size
    top = (height - crop_height) // 2
    bottom = top + crop_height
    return img.crop((0, top, width, bottom))

def add_white_space_height(img, new_height_percent=200.0): 
    width, height = img.size
    # new_height = int(height * (new_height_percent / 100.0))
    new_height = int(height * (new_height_percent / 100.0))
    new_img = Image.new(img.mode, (width, new_height), (255, 255, 255))
    # new_img.paste(img, (0, (new_height - height) // 2))
    new_img.paste(img, (0, (new_height - height) // 2 ))
    return new_img



DR_PHELPS_WHITE_SPACE = 200.0
DR_PHELPS_CROP_HEIGHT = 160
DEFAULT_BNA_WIDTH = 800
DEFAULT_CONTENT_IMAGE_WIDTH = 325

# Example usage
# change_image_format(SEARCH_DIR, DEST_DIR)

process_images(SEARCH_DIR, DEST_DIR, resize_image, 'resized')
# process_images(SEARCH_DIR, DEST_DIR, split_image_vertically, 'split_vertical')

# process_images(SEARCH_DIR, DEST_DIR, resize_image_height, 'resized')
# process_images(SEARCH_DIR, DEST_DIR, split_image_horizontally, 'split_horizontal')
# process_images(SEARCH_DIR, DEST_DIR, custom_crop_height, 'cropped_height')
# process_images(SEARCH_DIR, DEST_DIR, add_white_space_height, 'white_space') # defaults to 200.00 for Dr. Phelps

 