from pyelegans import Generator, embryo_generator_model
import matplotlib.pyplot as plt
import cv2
import os

num_images = 3
save_foldername = "gen_images"

if os.path.isdir(save_foldername) == False:
    os.mkdir(save_foldername)
    

generator = embryo_generator_model()

for i in range(num_images):
    filename = save_foldername + "/" + str(i) + ".jpg"
    gen_image = generator.generate()  ## 2d numpy array 
    cv2.imwrite(filename, gen_image)