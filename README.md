# OCR TAG PROGRAM
Facilita el etiquetado de OCR.

## Requerimientos
Tener python3, se recomienda crear un ambiente aislado.
Las siguiente librerías son necesarias para correr el programa:
* `pip install opencv-python`
* `pip install pyqt5`
* `pip install numpy`

## Descripción y detalles
Programa que administra el etiquetado para OCR.

Algunos algoritmo de entrenamiento te solicitan que te entregues los datos en el formato:

always image_name | always ocr name
------------- | -------------
name1.extension(por eje. "png") | nombre_imagen1
name2.extension(por eje. "png") | nombre_imagen2\n
name3.extension(por eje. "png") | nombre_imagen3\n
. | .

## Algunos Ejemplos
### Aplicación principal
![](https://github.com/PabloTabilo/OCR_TAG_PROGRAM/blob/master/examples/app_principal.png)

### image augmentation
+ Se busca ampliar la varianza de posibilidades para el futuro entrenamiento de la red neuronal.
    + Se tiene distintas funciones implementadas con open-cv tanto de filtros como morfológicas.
        + Transformaciones morfológicas
            + Erosion
            + Dilatation
            + Opening
            + Closing
        + Filters
            + Average
            + Blur
            + gauss
            + Median
            + Salt & pepper
+ A futuro seguir mejorando los filtros e implementar algunos más.

![](https://github.com/PabloTabilo/OCR_TAG_PROGRAM/blob/master/examples/imageAugmentation.png)

### Data label
Para esta parte tenemos la etiqueta de ocr con el formato obligatorio para entrenar una red.

![](https://github.com/PabloTabilo/OCR_TAG_PROGRAM/blob/master/examples/datalabelinfo.png)

