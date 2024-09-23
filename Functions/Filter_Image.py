import numpy as np
import pandas as pd
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



def quantize_image(image, num_levels):

    image_array = np.array(image)
    
    quantized_array = np.floor(image_array / (256 / num_levels)) * (256 / num_levels)
    
    return quantized_array.astype(np.uint8)



def create_scm(image, distances=[1], angles=[0]):

    image_array = np.array(image)
    max_value = np.max(image_array) + 1 
    
    scm = np.zeros((max_value, max_value), dtype=np.int32)

    for distance in distances:
        for angle in angles:
            for i in range(image_array.shape[0]):
                for j in range(image_array.shape[1]):
                    if angle == 0:  
                        if j + distance < image_array.shape[1]:
                            scm[image_array[i, j], image_array[i, j + distance]] += 1
                    elif angle == 90:  
                        if i + distance < image_array.shape[0]:
                            scm[image_array[i, j], image_array[i + distance, j]] += 1

    return scm

