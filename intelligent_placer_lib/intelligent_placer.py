from skimage.color import rgb2gray
import cv2
from matplotlib import pyplot as plt
import intelligent_placer_lib.placer as pl


def check_image(path_to_png_jpg_image_on_local_computer) -> bool:
    '''
    точка входа
    def check_image(<path_to_png_jpg_image_on_local_computer>[, <poligon_coordinates>])
    которая возвращает True если предметы могут влезть в многоугольник, иначе False. То есть так, чтобы работал код:

    '''
    image_as_gray = rgb2gray(cv2.imread(path_to_png_jpg_image_on_local_computer))
    mask = pl.get_mask_of_total_image(image_as_gray)
    labels = pl.get_component_and_areas(mask)
    polygon_region, object_regions = pl.get_polygon_and_objects(labels)

    minr, minc, maxr, maxc =  polygon_region.bbox
    if minc > image_as_gray.shape[1]/2:
        return False, mask
    
    res, img = pl.not_very_intelligent_but_placer(object_regions, polygon_region)
    return res, img

