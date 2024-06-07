# test_image_processor.py
import pytest
import sys
sys.path.append('.')

from src.image_processor import calculate_new_dimensions
from src.image_processor import resize_image

def test_calculate_new_dimensions():
    # call the function to be tested 
    result = calculate_new_dimensions(400,200,200) 
    assert result == (200,100)

def test_resize_image():
    test_image_path = 'resize_test.jpg' 

    # Calculate expected new height
    new_dimensions = calculate_new_dimensions(500, 346, 200)

    # Resize the image
    resized_size = resize_image(test_image_path, 200)

    # Check if the width of the resized image is as expected
    assert resized_size == new_dimensions, "Resized image width does not match expected width"