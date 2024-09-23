import numpy as np
from PIL import Image

def apply_mean_filter(image, filter_size):
    mean_filter = np.ones((filter_size, filter_size), np.float32) / (filter_size ** 2)
    
    image_array = np.array(image)
    padded_image = np.pad(image_array, ((filter_size//2, filter_size//2), (filter_size//2, filter_size//2)), mode='edge')
    filtered_image = np.zeros_like(image_array)

    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            region = padded_image[i:i + filter_size, j:j + filter_size]
            filtered_image[i, j] = np.sum(region * mean_filter)

    return filtered_image


