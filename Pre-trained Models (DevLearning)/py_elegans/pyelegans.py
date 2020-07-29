import torch
import torch.nn as nn
from torch.nn import functional as F
import torchvision
import torchvision.transforms as transforms
from torchvision.transforms import ToTensor
from torchvision.transforms import ToPILImage
import torchvision.models as models

import os
import cv2
from tqdm import tqdm
from PIL import Image
import joblib
import numpy as np
from collections import deque
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

class lineage_population_model():   
    def __init__(self, mode = "cpu"):
        self.mode = mode
        self.model = models.resnet18(pretrained = True)
        self.model.fc = nn.Linear(512, 7)  ## resize last layer

        self.scaler = joblib.load('scaler/scaler.gz')

        if self.mode == "cpu":
            self.model.load_state_dict(torch.load("models/estimate_lineage_population.pt", map_location= "cpu"))  
        else:
            self.model.load_state_dict(torch.load("models/estimate_lineage_population.pt"))  

        self.model.eval()

        self.transforms = transforms.Compose([
                                            transforms.ToPILImage(),
                                            transforms.Resize((256,256), interpolation = Image.NEAREST),
                                            transforms.ToTensor(),
                                            transforms.Normalize((0.5,), (0.5,))
                                            ])

    def predict(self, image_path):

        """
        input{
            image path <str>
        }

        output{
            dictionary containing the cell population values <dict>
        }

        Loads an image from image_path and converts it to grayscale, 
        then passes it though the model and returns a dictionary 
        with the scaled output (see self.scaler)

        """

        image = cv2.imread(image_path, 0)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        tensor = self.transforms(image).unsqueeze(0)
        
        pred = self.model(tensor).detach().cpu().numpy().reshape(1,-1)

        pred_scaled = (self.scaler.inverse_transform(pred).flatten()).astype(np.uint8)

        pred_dict = {
            "A": pred_scaled[0],
            "E": pred_scaled[1],
            "M": pred_scaled[2],
            "P": pred_scaled[3],
            "C": pred_scaled[4],
            "D": pred_scaled[5],
            "Z": pred_scaled[6]
        }

        return pred_dict

    def predict_from_video(self, video_path, csv_name  = "foo.csv", save_csv = False, ignore_first_n_frames = 0, ignore_last_n_frames = 0):

        """
        inputs{
            video path <str> = path to video file 
            csv_name <str> = filename to be used to save the predictions 
            save_csv <bool> = set to True if you want to save the predictions into a CSV files
            ignore_first_n_frames <int> = number of frames to drop in the start of the video 
            ignore_last_n_frames <int> = number of frames to drop in the end of the video 
        }


        output{
            DataFrame containing all the preds with the corresponding column name <pandas.DataFrame>
        }
        
        Splits a video from video_path into frames and passes the 
        frames through the model for predictions. Saves all the predictions
        into a pandas.DataFrame which can be optionally saved as a CSV file.

        The model was trained to make predictions upto the 
        stage where the population of "A" lineage is 250

        """
        A_population_upper_limit = 250

        vidObj = cv2.VideoCapture(video_path)   
        success = 1
        images = deque()
        count = 0

        preds = deque()

        while success: 
            success, image = vidObj.read() 
            
            try:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                images.append(image)
                
            except:
                print("skipped possible corrupt frame number : ", count)
            count += 1 

        for i in tqdm(range(len(images)), desc='Predicting from video file:  :'):
            tensor = self.transforms(images[i]).unsqueeze(0)
            pred = self.model(tensor).detach().cpu().numpy().reshape(1,-1)
            pred_scaled = (self.scaler.inverse_transform(pred).flatten()).astype(np.uint8)
            preds.append(pred_scaled)

       
        df = pd.DataFrame(preds, columns = ["A", "E", "M", "P", "C", "D", "Z"]) 

        if ignore_first_n_frames != 0:
            df= df.tail(df.shape[0] - ignore_first_n_frames)


        if ignore_last_n_frames != 0:
            df= df.head(df.shape[0] - ignore_last_n_frames)

        a_values = df["A"].values

        for limit in range(len(a_values)):  ## show preds upto 250 A cells 
            if a_values[limit]>=250:
                break
        
        df = df.head(limit)

        if save_csv == True:

            df.to_csv(csv_name, index = False)

        return  df


        
    def create_population_plot_from_video(self, video_path, save_plot = False, plot_name = "plot.png", ignore_first_n_frames = 0, ignore_last_n_frames = 0 ):

        """
        inputs{
            video_path <str> = path to video file 
            save_plot <bool> = set to True to save the plot as an image file 
            plot_name <str> = filename of the plot image to be saved 
            ignore_first_n_frames <int> = number of frames to drop in the start of the video 
            ignore_last_n_frames <int> = number of frames to drop in the end of the video 
        }

        outputs{
            plot object which can be customized further <matplotlib.pyplot>
        }

        plots all the predictions from a video into a matplotlib.pyplot 
        
        """
        df = self.predict_from_video(video_path, ignore_first_n_frames = ignore_first_n_frames, ignore_last_n_frames = ignore_last_n_frames )  
        
        labels = ["A", "E", "M", "P", "C", "D", "Z"]

        for label in labels:
            plt.plot(df[label].values, label = label)

        plt.xlabel("frames")
        plt.ylabel("population")

        if save_plot == True:
            plt.legend()
            
            plt.savefig(plot_name)

        return plt



"""
GAN to generate images of embryos 
"""


class Generator(nn.Module):
    def __init__(self, ngpu, ngf, nz, nc):
        super().__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d( nz, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d( ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d( ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32

            nn.ConvTranspose2d( ngf, ngf, 4, 2, 1, bias=False),  ## added custom stuff here
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 64 x 64

            nn.ConvTranspose2d( ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. (nc) x 128 x 128
        )

    def forward(self, input):
        return self.main(input)


class embryo_generator_model():   
    def __init__(self, mode = "cpu"):

        self.ngf = 128 ## generated image size 
        self.nz = 128
        self.nc = 1

        
        self.mode = mode
        if self.mode=="cpu":
            self.ngpu = 0
            self.generator= Generator(self.ngpu, self.ngf, self.nz, self.nc)
            self.generator.load_state_dict(torch.load("models/embryo_generator.pt", map_location= "cpu"))

        else:
            self.ngpu = 1
            self.generator= Generator(self.ngpu, self.ngf, self.nz, self.nc)
            self.generator.load_state_dict(torch.load("models/embryo_generator.pt"))


    def generate(self, image_size = (700,500)):
        with torch.no_grad():
            noise = torch.randn([1,128,1,1])
            if self.mode != "cpu":
                noise = noise.cuda()
            im = self.generator(noise)[0][0].cpu().detach().numpy()
        im = cv2.resize(im, image_size)
        im = 255 - cv2.convertScaleAbs(im, alpha=(255.0))   ## temporary fix against inverted images 

        return im


    def generate_n_images(self, n = 3, foldername = "generated_images", image_size = (700,500)):

        if os.path.isdir(foldername) == False:
            os.mkdir(foldername)

        
        for i in tqdm(range(n), desc = "generating images :"):
            filename = foldername + "/" + str(i) + ".jpg"
            gen_image = self.generate()  ## 2d numpy array 
            cv2.imwrite(filename, gen_image)

        print ("Saved ", n, " images in", foldername)