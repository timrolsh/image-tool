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


def cv_to_pil(image: np.ndarray):
    """
    Convert an OpenCV image to a PIL Image object.

    Args:
    image (ndarray): Image array compatible with OpenCV.

    Returns:
    PIL.Image: The converted PIL Image object.
    """

    # Assuming img_trim is your BGR image from OpenCV where black regions should be transparent
    # First, create an alpha channel based on the condition that all BGR values are 0 (black)
    # Creates a mask where black is 0 (transparent)
    alpha_channel = 255 * np.all(image == [0, 0, 0], axis=-1).astype(np.uint8)

    # Invert the mask since we want black to be transparent
    alpha_channel = np.invert(alpha_channel)

    # Stack the BGR image with the new alpha channel
    rgba_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rgba_image = np.dstack((rgba_image, alpha_channel))

    # Convert to PIL Image
    transparent_image = Image.fromarray(rgba_image)

    return transparent_image
