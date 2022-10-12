# Intelligent_Placer
by bolshakova anna, group 5030102/90401
# Intelligent_Placer.
# Постановка задачи

Требуется создать “Intelligent Placer”:

**Подается фотография, на который отчетливо видно:**
   - несколько предметов из заготовленного перечня предметов (всего 10 шт., фото предметом в репозитории), расположенных на светло-деревянной горизонтальной поверхности (фотография которой также находится в репозитории, для последующего учитывания текстуры фона (?)). 
   - многоугольник, нарисованный черным маркером/ ручкой на белом листе бумаги
   
**Необходимо** : узнать, можно ли расположить одновременно все эти предметы на плоскости так, чтобы они влезли в этот многоугольник, при этом не пересекаясь (предполагается, что программа сможет создавать бинарные маски-контуры предметов, которые при размещении в многоугольники не будут накладываться друг на друга) 


“Intelligent Placer” должен быть оформлен в виде python-библиотеки `intelligent_placer_lib`, которая поставляется каталогом `intelligent_placer_lib` с файлом `intelligent_placer.py`, содержащим функцию - точку входа 
`def check_image(<path_to_png_jpg_image_on_local_computer>[, <poligon_coordinates>]) `
которая возвращает True если предметы могут влезть в многоугольник, иначе False. То есть так, чтобы работал код:


```
from intelligent_placer_lib import intelligent_placer 
def test_intelligent_placer(): 
assert intelligent_placer.check_image(“/path/to/my/image.png”) 
```
# Вход и выход
**Входные данные:**   строка - путь к фотографии - *фото допустимого формата (см. требования)*
  
**Выходные данные:**  `True` - существует спооб расположит все предметы так, чтобы они не пересекались. Иначе - `False` (если нет многоугольника, если нет предметов, если нельзя расположить все предметы, если фотография не соотвествует требованиям и т.д.)
   
  

# Требования
### Фотометрические требования:
  1. допустимые форматы -  png / jpg / jpeg
  1. камера как можно более параллельна плоскости листа, чтобы минимизировать искажение перспективы
  1. освещение непосредственно над плоскостью съемки
  1. четкие фото, тень от объектов минимальна
  1. на входных фотографиях предметы отличимы от поверхности. (предметы темнее поверхности, на которой находятся)
  1. на эталонных фотографиях предметы находятся на белом листе А4. 
### Требования по расположению объектов:
  1. объекты не пересекаются (видно некотую область с текстурой поверхности между ними) 
  1. объекты не выходят за границы кадра 
  1. объекты сложной формы фотографируются с единственного ракурса
  1. лист располагается слева, предметы справа
  1. На фото 1 объект присутсвует 1 раз
### Требования в области:
  1. многоугольник, имеющий от 3 до 15 вершин
  1. нарисован черным маркером / ручкой

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
  
   [поверхность](https://github.com/bolshakova-anna/Intelligent_Placer/blob/develop/data/background.jpg)

# Примеры с пояснениями и примерами расположения, если такие имеются
  1. [1 помещаемый объект -> true](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/1)
  1. [2 объекта, помещается 1 -> false](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/2)
  1. [2 объекта, помещается 2 -> true](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/3)
  1. [2 объкта, оба одновременно не помещаются -> false](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/4)
  1. [1 непомещаемый объект -> false](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/5)
  1. [несколько помещаемых объектов -> true](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/6)
  1. [еще несколько помещаемых объектов -> true](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/7)
  1. [ни один из обхектов не поместился -> false](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/8)
  1. [нет многоугольника -> false](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/9)
  1. [пример со всеми 10 предметами, все помещаются -> true](https://github.com/bolshakova-anna/Intelligent_Placer/tree/develop/data/examples/10)

# План

1. Этап предобработки. 
   - Понижение разрешения фотографии для ускорения работы программы (текущее 3024x3024, стоит понизить          примерно в 3-5 раз)
   - Перевод изображение в ч/б
   - Поиск границ листа:
     - применение локальной или обычной бинаризации изображения (в зависимости от результатов, конкретный      метод  для бинаризации может меняться)
     - использование морфологических операций, выбор наибольшей по площади компоненты связности - листа с      многоугольником
   - Создание бинарной маски многоугольника в найденном листе : 
     - поиск границ многоугольника - применение canny 
     - создание маски, применение морфологических операций , заполнение полученной границы значением 1.
   - Создание бинарных масок предметов
     - отделение предметов от поверхности - поиск похожей текстуры и удаление ее с фото
     - отделение границ предметов друг от друга - применение гаусса, бинаризация, морфологические операции
     - создание и сортировка списка масок изображений - получение списка компонент связности, первый элемент - компонента наибольшей площади, последний - наименьшей. в самой маске значение 1 соответствует объекту.
2. Размещение. Задача заключается в разработке метода перебора комбинаций 
   - Если суммарная площадь объектов больше площади многоугольника, выход с результатом False
   - Разработать алгоритм, который с помощью угла поворота масок объектов, сдвига их внутри области            многоугольника, будет оптимально находить возможное размещение, либо сообщать о невозможности.
     - Текущая идея: 
      1. начиная с объекта наиб. площади
      1. перемещаясь по границе многоугольника
      1. для каждого положения с некоторым шагом поворачивать объект, при необходимости (при выходе за границы многоугольника) - смещая его внутрь. Вычитаем его из маски многоугольника и получаем вместо многоугольника список компонент связности. Теперь каждую из них можно рассматривать как новый “многоугольник”, в котором можно попробовать разместить оставшиеся предметы.


  
