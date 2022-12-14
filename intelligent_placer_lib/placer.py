import numpy as np
from scipy import ndimage as ndi
import cv2 as cv
import matplotlib.pyplot as plt 
from skimage.feature import canny
from skimage.measure import regionprops
from skimage.measure import label as sk_measure_label
from skimage.morphology import binary_closing #, binary_opening
from skimage.morphology import remove_small_objects
from skimage.morphology import erosion, square
from skimage.transform import rescale
from skimage.transform import rotate
from skimage.transform import warp , SimilarityTransform


# https://datacarpentry.org/image-processing/aio/index.html
MIN_AREA = 40000*0.9


def correct_mask_borders(canny_result, border_width=3):
    '''
    коррекция краев бинарной маски
    используется внутри get_mask_of_total_image
    '''
    canny_result[:border_width,:] = 0
    canny_result[:,:border_width] = 0
    canny_result[-border_width:,:] = 0
    canny_result[:,-border_width:] = 0    


def get_mask_of_total_image(image_as_gray: np.ndarray)->np.ndarray:
    '''
    Получение маски изображения посредством детектора Кэнни и морфологических операций.
    Исключение дефектов из маски на данном этапе не происходит.
    Parameters
    ----------
    image : ndarray
        Ч/б изображение
    Returns
    -------
    np.ndarray
        Бинарная маска, где True - пиксели, распознанные как объекты

    '''
    canny_sigma = 3.001
    canny_low_threshold = 0.00
    canny_high_threshold = 0.285
    binary_closing_footprint_width = 10
    binary_closing_footprint = np.ones((binary_closing_footprint_width, binary_closing_footprint_width))

    total_bin_mask = binary_closing(
        canny(
            image_as_gray,
            sigma=canny_sigma,
            low_threshold=canny_low_threshold,
            high_threshold=canny_high_threshold,
        ),
        footprint=binary_closing_footprint
    )
    correct_mask_borders(total_bin_mask)
    total_bin_mask = ndi.binary_fill_holes(total_bin_mask)
    return total_bin_mask


def get_component_and_areas(mask):
    '''
    Исключение дефектов обработки маски. Выделение из маски списка компонент связности 
    - некоторых областей, которые потом будут опознаваться 
    Parameters
    ----------
    image : ndarray
        бинарная маска изображения
    Returns
    -------
    лист label'ов, соответвующий объектам

    '''
    mask = remove_small_objects(mask,MIN_AREA)
    labels = sk_measure_label(mask) 
    return labels

def get_polygon_and_objects(labels):
    '''
    Нахождение многоугольника как самого левого компонента связности (из постановки)
    Оставшиеся компоненты связности возвращаются как объекты
    
    Parameters
    ----------
    labels
        список компонен связности входного изображения
    Returns
    -------
    polygon_region : regionprops() , соотвествующий многоугольнику
    '''
    # предполагается, что разрешение изображения точно меньше 'max_image_pixel_len' 
    max_image_pixel_len = 5000  
    objects_regions = regionprops(labels)
    for region in objects_regions:
            minr, minc, maxr, maxc = region.bbox
            if minc < max_image_pixel_len:
                max_image_pixel_len = minc
                polygon_region = region

    objects_regions.remove(polygon_region)
    return polygon_region, objects_regions



def is_total_object_area_smaller_than_polygon_area(polygon_region, objects_regions) -> bool :
    '''
    Проверка вместимости всех объектов по площади в многоугольник
    '''
    sum_area = 0
    for region in objects_regions:
            sum_area += region.area
    if sum_area > polygon_region.area:
        return False
    return True

def is_all_objects_major_lenghs_fit_polygon(polygon_region, objects_regions) -> bool :
    '''
    Проверка вместимости всех объектов по длине в многоугольник
    '''
    max_axis_major_length = polygon_region.axis_major_length
    for object_cur in objects_regions:
        if object_cur.axis_major_length > max_axis_major_length:
            return False
    return True
    
def shift_object(object_image, vector)->bool:
    '''
    Сдвиг изображения в направлении вектора.
    Изменения размера изображения не происходит. Пустота заполняется черным фоном.
    '''
    transform = SimilarityTransform(translation=(-vector[0],vector[1])) # использована геом. трансформация (быстрее) :
    shifted = warp(object_image, transform)#, mode='wrap', preserve_range=True)

    return shifted


def rotate_object(object_image, angle):
    '''
    Поворот изображения (объекта) на угол angle в градусах
    Parameters
    ----------
    labels
        список компонен связности входного изображения
    polygon_region 
         regionprops() , соотвествующий многоугольнику
    Returns
    -------
    polygon_region : лист regionprops() , соотвествующий листу объектов
    '''
    rotated = rotate(object_image, angle, resize = True)
    return rotated

def add_pad(object, pad_shape)->np.ndarray:
    '''
    Добавление подложки размера pad_shape для object таким образом,
    что object расположен слева-снизу
    '''
    pad = np.full(pad_shape, False,dtype=bool)
    pad[pad.shape[0]-object.shape[0]:pad.shape[0],
    0:object.shape[1]] += object
    return pad


def can_place(object, total_img)->bool:
    '''
    Проверка на то, поместился ли полностью объект
    '''
    res = np.logical_and(object,~total_img)
    count = (res == True).sum()
    if count >= 10:
        return False
    return True
        


def place_iteration(total_placement_img, object_img, step, step_angle):
    '''
    Реализация алгоритма - итерации перебора размещения. Не самая оптимальная версия
        скорее всего все придет к блоксхеме-2 (картинка в директории) из статьи:
        A heuristic for nesting problems of irregular shapes, Wen-Chen Lee
    '''
    for angle in range(0,360,step_angle):
        rotated_object = rotate(object_img,angle) # текущая конфигурация поворота
        pad_object = add_pad(rotated_object,total_placement_img.shape) #добавление подложки
        #протаскиваем по изображению
        breaker = False
        for h in range(0,total_placement_img.shape[0],step):
            for w in range(0,total_placement_img.shape[1],step):
                
                pad_object_shifted = shift_object(pad_object,(h,w))
                

                 #если верхний или левый край содержат края изображения, считаем что вышли за границы
                if ( (True in pad_object_shifted[:1,:]) or
                    np.max(pad_object_shifted) == False or
                    (True in pad_object_shifted[:,-1:])):
                    breaker = True
                    break

                if can_place(pad_object_shifted,total_placement_img):                    
                    plt.figure()
                    fig,ax=plt.subplots(1,3)
                    ax[0].imshow(pad_object_shifted)
                    ax[1].imshow(total_placement_img)
                    ax[2].imshow(np.logical_xor(pad_object_shifted,total_placement_img))
                    plt.show()
                    total_placement_img = np.logical_xor(pad_object_shifted,total_placement_img)
                    return True , total_placement_img
            if breaker:
                break
                
    return False, total_placement_img

def not_very_intelligent_but_placer(objects_regions, polygon_region):
    '''
    Проверка размещения листа объектов в области.

    Parameters
    ----------
    objects_regions
        список компонен связности располагаемых объектов 
    polygon_region 
         regionprops() , соотвествующий многоугольнику
    Returns
    -------
    bool 
        - True, если можно расположить
        - False, если нельзя расположить
    np.ndarray 
        найденная возможная конфигурация размещения

    '''
        
    # cортировка объектов по убыванию площади
    objects_regions = sorted(
            objects_regions,
            key=lambda r: r.area,
            reverse=True,
    )
    total_placement = polygon_region.image
    # проверка - объекты по суммарной площади влезают
                    # все объекты по длине влезают 
    if not(is_total_object_area_smaller_than_polygon_area(polygon_region,objects_regions) and 
           is_all_objects_major_lenghs_fit_polygon(polygon_region,objects_regions)):
        return False, total_placement
    
    step_shift = 5
    step_angle = 10
    rescale_coeff = 0.25

    total_placement = rescale(total_placement,rescale_coeff,anti_aliasing=False).astype(bool)

    for object_cur in objects_regions:
        object_cur_img = rescale(object_cur.image,rescale_coeff,anti_aliasing=False).astype(bool)
        correct_mask_borders(object_cur_img,1)
        object_cur_img = erosion(object_cur_img, square(5))
        
        if np.count_nonzero(object_cur_img == True) >= np.count_nonzero(total_placement == True):
            return False, total_placement

        answer, total_placement = place_iteration(total_placement,
                                                 object_cur_img,
                                                 step_shift, step_angle)
        if answer == False:
            return False, total_placement    
    return True, total_placement

