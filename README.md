# OCR TAG PROGRAM
Finalidad: Facilitar y agilizar el etiquetado de OCR para la creación de una RED que tenga data nueva.

## Requerimientos
Tener python 3 instalado, se recomienda crear un ambiente aislado (lo podemos hacer con [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)).
Las siguiente librerías son necesarias para correr el programa:
* `pip install opencv-python`
* `pip install PyQt5`
* `pip install numpy`

## Descripción y detalles
Programa que administra el etiquetado para OCR.
Algunos algoritmo de entrenamiento te solicitan que te entregues los datos en el formato:

always image_name | always ocr name
------------- | -------------
name1.extension(por eje. "png") | nombre_imagen1
name2.extension(por eje. "png") | nombre_imagen2\n
name3.extension(por eje. "png") | nombre_imagen3\n
... | ...

Para iniciar la aplicacion se escribe lo siguiente en consola, tiene que ser en el directorio del proyecto:
`python OCRgui.py`

### Ejemplos de uso (con pantallazo)
#### Aplicación principal
![](https://github.com/PabloTabilo/OCR_TAG_PROGRAM/blob/master/examples/app_principal.png)

### Image augmentation
+ Se busca ampliar la varianza de los datos con el fin de representar un desafío para el futuro entrenamiento de la red neuronal, ya que, esto permite lograr que la red capture las features relevantes dentro de la imagen.
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

#### Data label
Para esta parte tenemos la etiqueta de ocr con el formato obligatorio para entrenar una red.

![](https://github.com/PabloTabilo/OCR_TAG_PROGRAM/blob/master/examples/datalabelinfo.png)

#### Salida de la información
El programa, en el mismo directorio donde se aloja, crea dos carpetas llamadas "salidaOCR", "txt_dir".
La carpeta "salidaOCR" contiene las imagenes con su transformación, y la carpeta "txt_dir" contiene un archivo de texto que mantiene el orden que se explica en la sección de "Descripción y detalles".

## Opcional
También, dentro del repositorio, viene incluido un archivo "config.json" con el cual como usuario puedes configurar los parámetros (como el tamaño de los kernel's) que se ocupan para el image augmentation.

# Autor
Pablo Ignacio Tabilo Chirino
