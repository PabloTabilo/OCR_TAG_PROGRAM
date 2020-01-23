from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QPixmap
import os

# tengo que entregar la entrada de los archivos imgs
# Si quiero puedo agregar

import app

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "OCR label Version 0.1"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 600
        self.InitWindow()
        self.save_file = False
    
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)

        self.hbox = QHBoxLayout()

        self.vbox = QVBoxLayout()

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
    
    def alertMessages(self):
        res = QMessageBox.question(self,'','Are you sure you want to continue without save?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            return True
        else:
            return False

    def save_ocr(self):
        self.save_file = True
        self.allGood = True
        try:
            print("Tenemos el archivo seleccionado")
            print(self.listwidget.currentItem().text())
            self.allGood = True
        except:
            print("No has seleccionado ningun item")
            self.save_file = False
            self.allGood = False
        try:
            print("Tenemos el texto del usuario!")
            print(self.textUser)
            self.allGood = True
        except:
            print("No has escrito nada")
            self.save_file = False
            self.allGood = False
        try:
            print("Tenemos el directorio")
            print(str(self.ddir))
            self.allGood = True
        except:
            print("No has seleccionado ningun directorio")
            self.save_file = False
            self.allGood = False
        
        if self.allGood:
            app.main(str(self.ddir),self.listwidget.currentItem().text(),self.textUser)
    
    def continueNext(self,cur):
        try:
            self.getImage(self.files[cur+1])
            self.listwidget.setCurrentRow(cur+1)
        except:
            self.getImage(self.files[cur])
            self.listwidget.setCurrentRow(cur)
    
    def next_click(self):
        cur = self.listwidget.currentRow()
        self.identify(self.imageName)
        if self.save_file == True:
            self.continueNext(cur)
        else:
            if self.alertMessages():
                self.continueNext(cur)
            else:
                self.getImage(self.files[cur])
                self.listwidget.setCurrentRow(cur)
        
        self.save_file = False
    
    def continueBefore(self,cur):
        try:
            self.getImage(self.files[cur-1])
            self.listwidget.setCurrentRow(cur-1)
        except:
            self.getImage(self.files[cur])
            self.listwidget.setCurrentRow(cur)
    
    def before_click(self):
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
    
    def itemsList(self,files):
        self.listwidget = QListWidget()
        self.listwidget.setMinimumWidth(200)
        for i in range(len(files)):
            self.listwidget.insertItem(i, str(files[i]))
        self.listwidget.clicked.connect(self.clicked)
        self.hbox.addWidget(self.listwidget)
    
    def clicked(self, qmodelindex):
        item = self.listwidget.currentItem()
        self.getImage(item.text())
    
    def getDir(self):
        self.ddir = QFileDialog.getExistingDirectory(self, "Get Dir PAth")
        try:
            self.files = [name for name in os.listdir(str(self.ddir)) if ".png" in name]
            self.itemsList(self.files)
        except:
            self.dir = ""
 
    def getImage(self,image_name):
        self.imageName = image_name
        imagePath = os.path.join(self.ddir,image_name)
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(QPixmap(imagePath).scaled(600, 400, QtCore.Qt.KeepAspectRatio))
        self.identify(image_name)
    
    def identify(self,image_name):
        # nombres de las imgs guardadas con OCR
        name_saved, ocr_saved = app.checkMytxt()
        self.dict_saved = dict(zip(name_saved,ocr_saved))
        try:
            actual_name = self.dict_saved[image_name]
            self.lineedit.setText(actual_name)
            self.save_file = True
        except :
            self.lineedit.setText("")
            self.save_file = False
    
    def setLabelInput(self):
        self.lineedit = QLineEdit(self)
        self.lineedit.setFont(QtGui.QFont("Sanserif",15))
        self.lineedit.textChanged.connect(self.onPressed)
    
    def onPressed(self):
        self.textUser = self.lineedit.text()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())