import cv2
import numpy as np
import os
import json
# read file
with open('config.json', 'r') as myfile:
    data_json=myfile.read()
# parse file
obj = json.loads(data_json)

class ImageConfig():
    def __init__(self,url_dir_i):
        self.url_dir_i = url_dir_i
        
        # filter transforms
        # average
        self.average_size = int(obj["filter_transforms"]["kernel_average"]["size_square"])
        self.average_divide = float(obj["filter_transforms"]["kernel_average"]["divide"])
        #blur
        self.blur_size = int(obj["filter_transforms"]["kernel_blur"]["size_square"])
        #gauss
        self.gauss_size = int(obj["filter_transforms"]["kernel_gaussian"]["size_square"])
        #median
        self.median_size = int(obj["filter_transforms"]["kernel_median"]["size_square"])
        #S&P
        self.sp_sp = float(obj["filter_transforms"]["salt_and_pepper"]["sp"])
        self.sp_amount = float(obj["filter_transforms"]["salt_and_pepper"]["amount"])
        # Morphological Transforms
        self.morpho_size = int(obj["morphological_transforms"]["kernel_mor"]["size_square"])

    
    def loadImagesbyDir(self):
        self.img = cv2.imread(self.url_dir_i,1)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
    
    def viewThisSHIT(self):
        cv2.imshow('img',self.img)
        cv2.waitKey(0)
    
    def morphologicalTransforms(self):
        # gray morphological transformations
        self.gray_img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        kernel_mor = np.ones((self.morpho_size,self.morpho_size),np.uint8)
        self.erosion = cv2.erode(self.img,kernel_mor,iterations = 1)
        self.dilation = cv2.dilate(self.img,kernel_mor,iterations = 1)
        self.opening = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, kernel_mor)
        self.closing = cv2.morphologyEx(self.img, cv2.MORPH_CLOSE, kernel_mor)
    
    def filtersTransforms(self):
        # Averaging
        kernel = np.ones((self.average_size,self.average_size),np.float32)/self.average_divide
        self.average = cv2.filter2D(self.img,-1,kernel)
        # blur
        self.blur = cv2.blur(self.img,(self.blur_size,self.blur_size))
        # GaussianBlur
        self.gaussblur = cv2.GaussianBlur(self.img,(self.gauss_size,self.gauss_size),0)
        # MedianFilter
        self.median = cv2.medianBlur(self.img,self.median_size)
    
    def specialSaltAndPepper(self):
        # Salt and pepper
        row,col,ch = self.img.shape
        s_vs_p = self.sp_sp
        amount = self.sp_amount
        self.out = np.copy(self.img)
        # Salt mode
        num_salt = np.ceil(amount * self.img.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in self.img.shape]
        self.out[coords] = 1
        # Pepper mode
        num_pepper = np.ceil(amount* self.img.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in self.img.shape]
        self.out[coords] = 0

    def variability(self):
        self.morphologicalTransforms()
        self.filtersTransforms()
        self.specialSaltAndPepper()

    def saveAll(self, outpath, name):
        name = name.strip(".png")
        cv2.imwrite(os.path.join(outpath,name+"_original_.png"),self.img)

        cv2.imwrite(os.path.join(outpath,name+"_average_.png"),self.average)
        cv2.imwrite(os.path.join(outpath,name+"_blur_.png"),self.blur)
        cv2.imwrite(os.path.join(outpath,name+"_gaussian_.png"),self.gaussblur)
        cv2.imwrite(os.path.join(outpath,name+"_median_.png"),self.median)
        cv2.imwrite(os.path.join(outpath,name+"_sp_.png"),self.out)

        cv2.imwrite(os.path.join(outpath,name+"_erosion_.png"),self.erosion)
        cv2.imwrite(os.path.join(outpath,name+"_dilation_.png"),self.dilation)
        cv2.imwrite(os.path.join(outpath,name+"_opening_.png"),self.opening)
        cv2.imwrite(os.path.join(outpath,name+"_closing_.png"),self.closing)