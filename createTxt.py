import os

class Mytxt():
    def __init__(self, out_path, name_img_current, name_on):
        self.out_path = out_path
        self.name_on = name_on
        name_url = name_img_current.strip(".png")
        self.name_list = [
            name_url+"_original_.png",name_url+"_average_.png",
            name_url+"_blur_.png",name_url+"_gaussian_.png",name_url+"_median_.png",
            name_url+"_sp_.png",name_url+"_erosion_.png",name_url+"_dilation_.png",
            name_url+"_opening_.png",name_url+"_closing_.png"
        ]
    
    def createTXT_zero(self):
        with open(self.path,"w") as f:
            for i in self.name_list:
                f.write(i + "\t"+ self.name_on +"\n")
    
    def appendTXT(self):
        with open(self.path,"a") as f:
            for i in self.name_list:
                f.write(i + "\t"+ self.name_on +"\n")
    
    def createAndDrop(self):
        with open(self.path,"r") as f:
            data = f.readlines()
        
        content = [row.split("\t")[0] for row in data]
        content_label = [row.split("\t")[1].strip("\n") for row in data]
        my_dict = dict(zip(content,content_label))

        for name_i in self.name_list:
            del my_dict[name_i]
        
        with open(self.path, "w") as f:
            for key in my_dict:
                f.write(key + "\t"+ my_dict[key] +"\n")
        
        self.appendTXT()
        
    def createRegister(self,exist):
        name_txt = "data_label.txt"
        self.path = os.path.join(self.out_path,name_txt)
        if exist:
            self.createAndDrop()
        else:
            if not os.path.isfile(self.path):
                self.createTXT_zero()
            else:
                self.appendTXT()      