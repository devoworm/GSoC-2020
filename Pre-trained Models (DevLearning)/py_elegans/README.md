# pyelegans 

<img src = "images/py_elegans_vis.png">

> Still under construction

# Generating synthetic images of embryos with a Pre-trained GAN

* Importing the model
```python
from pyelegans import Generator, embryo_generator_model
```

* Generating a picture
```python
generator = embryo_generator_model()
gen_image = generator.generate()  

```
* Viewing the generated image
```
plt.imshow(gen_image)
plt.show()
```

## Bulk generation using the GAN

* importing the libraries and the model
```python
from pyelegans import Generator, embryo_generator_model
import matplotlib.pyplot as plt
import cv2
import os
```

* setting the number of images and the foldername, and initiating the model
```python

num_images = 3
save_foldername = "gen_images"

if os.path.isdir(save_foldername) == False:
    os.mkdir(save_foldername)

generator = embryo_generator_model()
```
* generating images
```python
for i in range(num_images):
    filename = save_foldername + "/" + str(i) + ".jpg"
    gen_image = generator.generate()  ## 2d numpy array 
    cv2.imwrite(filename, gen_image)
```

---

# Predicting populations of cells within the C. elegans embryo

*  Importing the population model for inferences 
```python
from pyelegans import lineage_population_model
```

* Loading a model instance to be used to estimate lineage populations of embryos from videos/photos.
```python
model = lineage_population_model(mode = "cpu")
```

* Making a prediction from an image
```python
pred = model.predict(image_path = "sample.png")
```

* Making predictions from a video and saving the predictions into a CSV file
```python
results = model.predict_from_video(video_path = "sample_videos/20090309_F39B2_1_7_L1.mov", save_csv = True, csv_name = "foo.csv")
```

* Plotting the model's predictions
```python
plot = model.create_population_plot_from_video(video_path = "sample_data/sample_videos/20090309_F39B2_1_7_L1.mov", save_plot= True, plot_name= "images/plot.png", ignore_last_n_frames= 30 )
plot.show()
```
This would show a plot like:

<img src= "sample_preds/plot.png">
