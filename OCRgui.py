from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QPixmap
import os
import app

class Window(QWidget):
    def __init__(self):
        super().__init__()
        # Set configuraciones de ventana
        self.title = "OCR label Version 0.1"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 600
        # Indica si un archivo "i" esta guardado
        self.save_file = False
        self.textoCambio = False
        self.dir_anterior = ""

        self.InitWindow()
    
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)

        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()

        # boton para abrir directorios
        self.btn1 = QPushButton("Open Dir with images")
        self.btn1.clicked.connect(self.getDir)
        self.vbox.addWidget(self.btn1)

        self.label = QLabel("Not Image select")
        self.vbox.addWidget(self.label)

        self.setLabelInput()
        self.vbox.addWidget(self.lineedit)

        self.label2 = QLabel(self)
        self.label2.setFont(QtGui.QFont("Sanserif",15))
        self.vbox.addWidget(self.label2)

        # vbox
        button_save = QPushButton('SAVE',self)
        button_save.clicked.connect(self.save_ocr)
        self.vbox.addWidget(button_save)

        button_before = QPushButton('BEFORE',self)
        button_before.clicked.connect(self.before_click)
        self.vbox.addWidget(button_before)

        button_next = QPushButton('NEXT',self)
        button_next.clicked.connect(self.next_click)
        self.vbox.addWidget(button_next)

        # add vbox to horizontal
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(800,600)
        self.show()
    
    # Funcion de mensajes de alerta simple
    # solo nos entrega una si/no para guardar
    def alertMessages(self):
        res = QMessageBox.question(self,'','Estas seguro que quieres seguir sin crear OCR tag?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            return True
        else:
            return False
    
    def modifyText(self):
        res = QMessageBox.question(self,'','Se modificó el texto, no quieres guardar?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            return True
        else:
            return False
    
    def onlySpaces(self):
        res = QMessageBox.question(self,'','Has dejado muchos espacios, más de 3, es correcto?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            return True
        else:
            return False

    
    def alertNotSaveEmpty(self):
        QMessageBox.about(self, "No se puede salvar!", "Estas entregando un tag OCR vacío, no podemos salvar.")
    
    def alertNotDir(self):
        QMessageBox.about(self, "No se puede realizar la acción!", "No podemos realizar la acción, no tienes ningún directorio seleccionado.")
    
    def alertNotImage(self):
        QMessageBox.about(self, "No se puede realizar la acción!", "No podemos realizar la acción, no tienes ninguna imagen seleccionada.")

    def alertNotUserText(self):
        QMessageBox.about(self, "No se puede realizar la acción!", "Estas entregando un tag OCR vacío, no tienes nada.")

    def alertAllSave(self):
        QMessageBox.about(self, "Todo Guardado", "Todo a sido guardado de manera exitosa!!")
    
    def checkImageSelect(self):
        try:
            print("1ero instancia rescatada con text")
            print(self.listwidget.currentItem().text())
            print("2do propiedad de la clase")
            print(self.imageName)
            print("Tenemos la imagen seleccionada")
            self.allGood = True
        except:
            print("No has seleccionado ninguna imagen")
            self.save_file = False
            self.allGood = False
            self.alertNotImage()
        
        if self.allGood:
            return True
        else:
            return False
    
    def checkUserText(self):
        try:
            print(self.textUser)
            print("Tenemos el texto del usuario!")
            self.allGood = True
        except:
            print("El usuario no ha escrito nada")
            self.save_file = False
            self.allGood = False
            self.alertNotUserText()
        
        if self.allGood:
            return True
        else:
            return False
    
    def checkDir(self):
        try:
            print(str(self.ddir))
            print("Tenemos el directorio")
            self.allGood = True
        except:
            print("No has seleccionado ningun directorio")
            self.save_file = False
            self.allGood = False
            self.alertNotDir()
        
        if self.allGood:
            return True
        else:
            return False
    
    def checked(self):
        if self.checkDir() and self.checkImageSelect() and self.checkUserText():
            return True
        else:
            return False
    
    # Funcion que guarda el OCR solo si tiene todos los datos
    # especificados 
    def save_ocr(self):
        self.save_file = True
        self.allGood = True
        
        if self.checked():
            if self.textUser != "":
                app.main(str(self.ddir),self.listwidget.currentItem().text(),self.textUser)
                self.alertAllSave()
            else:
                print("Pero el user borro todo!")
                self.allGood = False
                self.save_file = False
                self.alertNotSaveEmpty()
    
    # funcion que toma el siguiente file dentro de la lista
    def continueNext(self,cur):
        try:
            self.getImage(self.files[cur+1])
            self.listwidget.setCurrentRow(cur+1)
        except:
            self.getImage(self.files[cur])
            self.listwidget.setCurrentRow(cur)
    
    # funcion para el boton next permite darnos el siguiente item
    # sin embargo, se necesitan cumplir ciertas reglas
    # tales como que tenga información el OCR, sino, te dará una advertencia
    # que el usuario decide si seguir o no 
    def next_click(self):
        if self.checked():
            cur = self.listwidget.currentRow()
            self.identify(self.imageName)
            if self.textUser != "":
                self.save_file = True
                self.continueNext(cur)
            else:
                if self.alertMessages():
                    self.continueNext(cur)
                else:
                    self.getImage(self.files[cur])
                    self.listwidget.setCurrentRow(cur)
            
            self.save_file = False
        else:
            print("No se puede realizar la acción")
    
    # funcion que toma el anterior file dentro de la lista
    def continueBefore(self,cur):
        try:
            self.getImage(self.files[cur-1])
            self.listwidget.setCurrentRow(cur-1)
        except:
            self.getImage(self.files[cur])
            self.listwidget.setCurrentRow(cur)
    
    # funcion para el boton before permite darnos el item anterior
    # sin embargo, se necesitan cumplir ciertas reglas
    # tales como que tenga información el OCR, sino, te dará una advertencia
    # que el usuario decide si seguir o no 
    def before_click(self):
        if self.checked():
            cur = self.listwidget.currentRow()
            self.identify(self.imageName)
            if self.save_file == True:
                self.continueBefore(cur)
            else:
                if self.alertMessages():
                    self.continueBefore(cur)
                else:
                    self.getImage(self.files[cur])
                    self.listwidget.setCurrentRow(cur)
            self.save_file = False
        else:
            print("Imposible realizar la acción")
    
    # Checkea si existe la lista
    # si existe entonces, elimina la actual y coloca la nueva
    def checkItemList(self):
        try:
            print(self.listwidget)
            print("Existe")
            # later
            self.listwidget.setParent(None)
        except :
            self.listwidget = None
    
    # funcion que crea el widget list para incluir todas las
    # imagenes
    def itemsList(self):
        self.checkItemList()
        self.listwidget = QListWidget()
        self.listwidget.setMinimumWidth(200)
        for i in range(len(self.files)):
            self.listwidget.insertItem(i, str(self.files[i]))
        self.listwidget.clicked.connect(self.clicked)# cuando clickeo alguna foto envio la info
        self.hbox.addWidget(self.listwidget)
    
    # funcion que sirve para asignar el nombre de la foto y permite
    # que la foto este en screen del usuario
    def clicked(self):
        item = self.listwidget.currentItem() # tomo el item actual
        print("Item actual: " + str(item.text))
        self.getImage(item.text()) # le paso el texto para cargar la img
    
    # funcion: abre el directorio y te entrega una lista de todos los archivos
    # .png, .jpg, .jpeg, .JPG, .PNG
    def getDir(self):
        self.ddir = QFileDialog.getExistingDirectory(self, "Get Dir Path")
        try:
            files_actuals = [name for name in os.listdir(str(self.ddir)) if ".png" in name or
             ".jpg" in name or ".jpeg" in name or ".JPG" in name or ".PNG" in name]
            if len(files_actuals)>0:
                self.dir_anterior = self.ddir
                self.files = files_actuals
                self.itemsList() # con esto listo los archivos en una lista
        except:
            # Si el usuario cancela el directorio, entonces, como tengo guardado el
            # directorio que ya abrió, solo se lo asigno
            self.ddir = ""
            if len(self.dir_anterior)>1:
                self.ddir = self.dir_anterior
                self.itemsList()
    
    # Funcion que con el nombre de la imagen y la colocamos en el pixmap
    # para mostrarla en la app
    def getImage(self,image_name):
        self.imageName = image_name
        imagePath = os.path.join(self.ddir,image_name)
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(QPixmap(imagePath).scaled(600, 400, QtCore.Qt.KeepAspectRatio))
        self.identify(image_name)
    
    # Funcion que me entrega el valor de OCR asignado a la imagen
    # si es que tiene
    # Finalmente el nombre lo escribe sobre el line edit
    def identify(self,image_name):
        # nombres de las imgs guardadas con OCR
        name_saved, ocr_saved = app.checkMytxt()
        self.dict_saved = dict(zip(name_saved,ocr_saved))
        try:
            actual_name = self.dict_saved[image_name]
            self.lineedit.setText(actual_name)
            self.save_file = True
            print(actual_name)
            print("Actual name asignado!")
            if actual_name == "":
                self.save_file = False
        except:
            self.lineedit.setText("")
            self.save_file = False
    
    # Funcion que registra el cambio del texto
    def setLabelInput(self):
        self.lineedit = QLineEdit(self)
        self.lineedit.setFont(QtGui.QFont("Sanserif",15))
        self.lineedit.textChanged.connect(self.onPressed)
    
    # Escribe el texto en el lineedit
    def onPressed(self):
        self.textUser = self.lineedit.text()
        self.textoCambio = True

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())