import torch
import torch.nn as nn
from torch.nn import functional as F
import torchvision
import torchvision.transforms as transforms
from torchvision.transforms import ToTensor
from torchvision.transforms import ToPILImage
import torchvision.models as models

import cv2
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
        input = video path <str>
        output = DataFrame <pandas.DataFrame>
        optionally saves csv file

        """

        vidObj = cv2.VideoCapture(video_path)   
        success = 1
        count = 0

        preds = deque()

        while success: 
            success, image = vidObj.read() 
            
            try:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                tensor = self.transforms(image).unsqueeze(0)
                pred = self.model(tensor).detach().cpu().numpy().reshape(1,-1)
                pred_scaled = (self.scaler.inverse_transform(pred).flatten()).astype(np.uint8)
                preds.append(pred_scaled)
                
            except:
                print("skipped possible corrupt frame number : ", count)
            count += 1
                
        df = pd.DataFrame(preds, columns = ["A", "E", "M", "P", "C", "D", "Z"]) 


        if ignore_first_n_frames != 0:
            df= df.tail(df.shape[0] - ignore_first_n_frames)


        if ignore_last_n_frames != 0:
            df= df.head(df.shape[0] - ignore_last_n_frames)


        if save_csv == True:

            df.to_csv(csv_name, index = False)

        return  df
        
    def create_population_plot_from_video(self, video_path, save_plot = False, plot_name = "plot.png", ignore_first_n_frames = 0, ignore_last_n_frames = 0 ):
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
        

        
        
