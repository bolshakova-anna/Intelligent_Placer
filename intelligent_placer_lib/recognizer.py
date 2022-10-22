import os
import numpy as np
from scipy import ndimage as ndi
import cv2
from skimage.color import rgb2gray, label2rgb
from skimage.feature import canny
from skimage.measure import regionprops
from skimage.measure import label as sk_measure_label
from skimage.metrics import structural_similarity
from skimage.filters import gaussian, threshold_otsu
from skimage.morphology import binary_closing, binary_opening

min_area = 40000
    
def correct_mask_borders_after_canny(canny_result, border_width=3):
    canny_result[:border_width,:] = 0
    canny_result[:,:border_width] = 0
    canny_result[-border_width:,:] = 0
    canny_result[:,-border_width:] = 0    

def get_mask(image_as_gray):
    canny_sigma = 3.001
    canny_low_threshold = 0.00
    canny_high_threshold = 0.285
    binary_closing_footprint_width = 10
    binary_closing_footprint = np.ones((binary_closing_footprint_width, binary_closing_footprint_width))

    my_edge_map = binary_closing(
        canny(
            image_as_gray,
            sigma=canny_sigma,
            low_threshold=canny_low_threshold,
            high_threshold=canny_high_threshold,
        ),
        footprint=binary_closing_footprint
    )
    correct_mask_borders_after_canny(my_edge_map)
    my_edge_segmentation = ndi.binary_fill_holes(my_edge_map)
    return my_edge_segmentation

def get_component_and_areas(mask):
    labels = sk_measure_label(mask) # разбиение маски на компоненты связности
    props = regionprops(labels) # нахождение свойств каждой области (положение центра, площадь, bbox, интервал интенсивностей и т.д.)
    areas = [prop.area for prop in props] 
    return labels, areas

## нахождение многоугольника как самого левого компонента связности (из постановки)
def get_polygon_region(labels):
    _ = 5000
    for region in regionprops(labels):
            minr, minc, maxr, maxc = region.bbox
            if minc < _ and region.area > min_area:
                _ = minc
                polygon_region = region
    return polygon_region

def get_objects_regions(labels, polygon_region):
    object_regions = list
    regions = regionprops(labels)
    for region in regions:
            if region.area < min_area or region == polygon_region:
                regions.remove(region)    
    return regions
