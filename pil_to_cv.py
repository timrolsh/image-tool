from PIL import Image
import numpy as np
import cv2

def pil_to_cv(image: Image):
    """
    Convert a PIL Image to an OpenCV image format.

    Args:
    image (PIL.Image): The PIL Image object to convert.

    Returns:
    ndarray: Image array compatible with OpenCV.
    """
    # Convert the PIL image to RGB if it's not in RGB mode already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert the PIL image to a numpy array
    cv_image = np.array(image)
    
    # OpenCV uses BGR format by default, so convert RGB to BGR
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    return cv_image