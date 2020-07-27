from pyelegans import lineage_population_model
from pyelegans import Generator, embryo_generator_model
import os 
import cv2 
import matplotlib.pyplot as plt
import pandas as pd 
from PIL import Image

model = lineage_population_model(mode = "cpu")

generator = embryo_generator_model()

generator.generate_n_images(n = 50, foldername= "generated_images", image_size= (256,256))

preds = []

for filename in os.listdir("generated_images"):

    pred = model.predict(image_path = "generated_images/" + filename)
    pred = list(pred.values())
    pred.append("generated_images/" + filename)
    preds.append(pred)

preds = pd.DataFrame(preds, columns = ["A", "E", "M", "P", "C", "D", "Z", "filename"])

preds = preds.sort_values(by = ["A"])

os.mkdir("plots")

count = 0
for i in preds.values:
    
    fig, ax = plt.subplots(1,2, figsize = (15,5))
    names = preds.columns[:-1]
    ax.flat[0].set_ylim([0, 255])
    ax.flat[0].bar(names, i[:-1], label= "populations")
    ax.flat[0].legend(fontsize = 15)
    ax.flat[1].imshow(cv2.imread(i[-1], 0))
    fig.savefig("plots/" + str(count) + ".jpg" )
    del fig
    count+= 1


names = [ "plots/" + str(i) + ".jpg" for i in range (0, 50, 1)]
images = []
for n in names:
    frame = Image.open(n)
    images.append(frame)

images[0].save('model_vs_GAN.gif',
               save_all=True,
               append_images=images[1:],
               duration=50,
               loop=0)

