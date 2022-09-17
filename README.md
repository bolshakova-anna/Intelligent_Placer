# Intelligent_Placer. Описание

Требуется создать “Intelligent Placer”: по поданной на вход фотографии нескольких предметов на светлой горизонтальной поверхности и многоугольнику понимать, можно ли расположить одновременно все эти предметы на плоскости так, чтобы они влезли в этот многоугольник. Предметы и горизонтальная поверхность, которые могут оказаться на фотографии, заранее известны. Также заранее известно направление вертикальной оси Z у этих предметов. Многоугольник задаетя фигурой, нарисованной темным маркером на белом листе бумаги, сфотографированной вместе с предметами. 

“Intelligent Placer” должен быть оформлен в виде python-библиотеки `intelligent_placer_lib`, которая поставляется каталогом `intelligent_placer_lib` с файлом `intelligent_placer.py`, содержащим функцию - точку входа 
`def check_image(<path_to_png_jpg_image_on_local_computer>[, <poligon_coordinates>]) `
которая возвращает True если предметы могут влезть в многоугольник, иначе False. То есть так, чтобы работал код:

```
from intelligent_placer_lib import intelligent_placer 
def test_intelligent_placer(): 
assert intelligent_placer.check_image(“/path/to/my/image.png”) 
```

# Требования
### Фотометрические требования:
  1. допустимые форматы -  png / jpg / jpeg
  1. камера как можно более параллельна плоскости листа
  1. освещение непосредственно над плоскостью съемки
  1. четкие фото, тень минимальна
### Требования по расположению объектов:
  1. объекты не пересекаются
  1. объекты сложной формы сфотографированы с единственного ракурса
  1. лист располагается слева, предметы справа
  1. На фото 1 объект присутсвует 1 раз
### Требования в области:
  1. многоугольник, имеющий от 3 до 15 вершин
  1. нарисован черным маркером или ручкой

# Изображения объектов
  1. [адаптер](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/adapter.jpg)
  1. [карта](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/card.jpeg)
  1. [перо](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/wacompen.jpeg)
  1. [ножницы](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/snip.jpg)
  1. [гильза](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/sleeve.jpg)
  1. [маркер](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/pen.jpg)
  1. [заколка](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/hairpin.jpeg)
  1. [когтерезка](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/cutter.jpg)
  1. [монета](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/coin.jpg)
  1. [кейс](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/objects/case.jpg)

# Примеры с комментарием
  1. []()
  1. []()
  1. []()
  1. []()
  1. []()
  1. []()
  1. []()
  1. []()
  1. []()
  1. []()
  1. []()
