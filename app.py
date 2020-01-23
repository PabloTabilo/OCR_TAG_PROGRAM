import os
import utils_cv2 as cv
import createTxt as ct

# si no tiene el directorio para guardar las imagens post transformacion
# , se lo creo
out_path = "salidaOCR/"
if not os.path.exists(out_path):
    os.makedirs(out_path)
# si no tiene el directorio para guardar txt, se lo creo
textpaths = "txt_dir/"
if not os.path.exists(textpaths):
    os.makedirs(textpaths)

# funcion que recorre toda la data y saca los nombres de la imagen
# sin embargo solo de la original
def checkMytxt(path_current="txt_dir/data_label.txt"):
    try:
        with open(path_current, 'r') as f:
            data = f.readlines()
        content = [row.split("\t")[0].replace("_original_","") for row in data if "_original_" in row]
        content_label = [row.split("\t")[1].strip("\n") for row in data if "_original_" in row]
    except :
        content = ""
        content_label = ""
    return content,content_label

def main(imagepaths,current_image_path,name):
    # listo el directorio donde esta todas las imagenes
    list_dir = [x for x in os.listdir(imagepaths) if ".png" in x]
    # nombre del set de registros por etiqueta
    name_txt = "data_label.txt"
    path_current = os.path.join(textpaths, name_txt)
    # checkeo si existe el directorio
    if os.path.isfile(path_current):
        # si existe, entonces, cargo la info que tiene el txt
        list_on_txt,_ = checkMytxt(path_current)
        # luego comparo las dos listas, y solo me dejo los archivos que 
        # no se han cargado al txt
        dict_all_vals = dict(zip(list_on_txt,_))
    
    try:
        print(dict_all_vals[current_image_path])
        print("new name: " + str(name))
        existe_img = True
    except:
        existe_img = False

    # Cargo el obj de imagen
    img_obj = cv.ImageConfig(os.path.join(imagepaths,current_image_path))
    # cargo la imagen con cv2 en numpy
    img_obj.loadImagesbyDir()
    # Creo la variabilidad y guardo todo
    img_obj.variability()
    img_obj.saveAll(out_path,current_image_path)
    # ahora agrego todo al txt,
    # le doy la ruta donde se guarda, la ruta de la imagen actual
    # y el nombre que el usuario introdujo
    txt_obj = ct.Mytxt(textpaths,current_image_path,name)
    # aqui creo el registro "i"
    txt_obj.createRegister(existe_img)