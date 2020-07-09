# [Pre-Trained models for Developmental Neuroscience](https://summerofcode.withgoogle.com/projects/#6078813261266944)

[![Binder](https://camo.githubusercontent.com/bfeb5472ee3df9b7c63ea3b260dc0c679be90b97/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f72656e6465722d6e627669657765722d6f72616e67652e7376673f636f6c6f72423d66333736323626636f6c6f72413d346434643464)](https://nbviewer.jupyter.org/github/devoworm/GSoC-2020/tree/master/Pre-trained%20Models%20(DevLearning))

Pre-trained deep neural networks like ResNet are being used in various industries where they help make our lives easier. But these kinds of models are not yet being used for microscopic images on a large scale. With the right model architecture and training approaches, it is possible to get pre-trained models which would help in the research efforts of many. These models, combined with a GUI would act as a community tool which would help speed up the classification/segmentation of thousands of microscopic images and gain inferences from them.

## [Deep segmentation model to extract nuclei from a C.elegans embryo](https://nbviewer.jupyter.org/github/devoworm/GSoC-2020/tree/master/Pre-trained%20Models%20%28DevLearning%29/notebooks/embryo_segmentation/)
* This model was trained on the [WormImage dataset](https://www.wormimage.org/) with manually labelled masks. You can download the segmentation datset [from this link](https://github.com/devoworm/GSoC-2020/raw/master/Pre-trained%20Models%20(DevLearning)/notebooks/embryo_segmentation/data/image_data.tar.xz)  
* The architeture is built on a [resNet18 backbone](https://www.researchgate.net/figure/ResNet-18-Architecture_tbl1_322476121).
* Augmentations were made within a custom instance of the `torch.utils.data.Dataset()` with the help of [albumentations](https://github.com/albumentations-team/albumentations). We had to make sure that the input image and the mask went through the exact same augmentative transforms in the pre-processing stage. 
* Interestingly enough, the model's output is less noisy than the augmented mask as seen below 

<image src= "notebooks/embryo_segmentation/images/seg_result.png" >

## [Extracting metadata from embryo time-lapses using the ResNet18](https://nbviewer.jupyter.org/github/devoworm/GSoC-2020/blob/master/Pre-trained%20Models%20%28DevLearning%29/notebooks/embryo_analysis/video_analysis/estimate_cell_family_population.ipynb)

<image src= "images/resnet18_pipeline.jpg" width = "80%" >

* We trained a ResNet18 architecture to determine the population of cells of various lineages within the C. elegans embryo. All videos were sourced from the [EPIC dataset](http://epic.gs.washington.edu/). 
*  The prediction for each frame of the model is a 1 dimensional tensor which contains the populations of the lineages `['A', 'E', 'M', 'P', 'C', 'D', 'Z']` in that order
* The model was trained on a reformatted version of the raw metadata, feel free to contact any of the members in this project for the reformatted data that was used for training. 

<image src= "images/resnet18_preds.png" >


## [Worm movement tracking and metadata extraction](https://nbviewer.jupyter.org/github/devoworm/GSoC-2020/tree/master/Pre-trained%20Models%20%28DevLearning%29/notebooks/worm_tracking/)
* This was built mostly using [openCV](https://opencv.org/) with tools like thresholding and contour finding algorithms. It tracks and segments worms from video feeds specifically from the [Open Worm Movement Database](http://movement.openworm.org/)

<image src= "images/tracking.gif" width = "50%">

* The cropped images of the worms were then used for time series analysis with the distance between the head and the tail as the parameter. The head and tail of the worm were also extracted using openCV. 

<image src= "https://mayukhdeb.github.io/blog/post/images/may_24/skeleton.png" width = "50%">

 ## [Deep learning on cell position metadata of a C. elegans embryo](https://nbviewer.jupyter.org/github/devoworm/GSoC-2020/blob/master/Pre-trained%20Models%20%28DevLearning%29/notebooks/embryo_analysis/deep_learning_on_metadata.ipynb)
 * Training was done on the [EPIC dataset](http://epic.gs.washington.edu/)
 * The model can predict the lineage name of a cell (or the cell name itself, depending on the time value) given it's position, size and time value. One can get a better understanding of the lineage tree of cells from the diagram given below:
 
 <image src= "notebooks/embryo_analysis/images/lineage_diagram.jpg" width = "30%">
  
 * The model can be re-trained on any embryo instance available on the dataset.
 
 ## [Time series prediction on worm metadata](https://nbviewer.jupyter.org/github/devoworm/GSoC-2020/blob/master/Pre-trained%20Models%20%28DevLearning%29/notebooks/worm_tracking/LSTM_time_series_prediction.ipynb)
* Predicting the "curvature" of a worm's body from time series data containing the distance between the head and the tail of the worm's body. 
* Note that the distance between the head and the tail is inversely proportional to the curvature. 
<image src= "images/LSTM_pred.png" >
 
 ## [Principal component analysis on worm embryo metadata](https://nbviewer.jupyter.org/github/devoworm/GSoC-2020/blob/master/Pre-trained%20Models%20%28DevLearning%29/notebooks/embryo_analysis/principal_component_analysis.ipynb)
 PCA helped us visualise how cells descending from common ancestors are closer to each other in the lower dimensional space with the two principal components as the `x` and `y` axis.  
 
 <image src= "notebooks/embryo_analysis/images/PCA.png" width = "80%">

 
 

#### Blog posts:
* [community bonding week 1](https://mayukhdeb.github.io/blog/post/gsoc-2020-may-17/)
* [community bonding week 2](https://mayukhdeb.github.io/blog/post/gsoc-2020-may-24/)
* [community bonding week 3](https://mayukhdeb.github.io/blog/post/gsoc-2020-may-31/)
* [coding period week 1](https://mayukhdeb.github.io/blog/post/gsoc-2020-june-7/)
* [coding period week 2](https://mayukhdeb.github.io/blog/post/gsoc-2020-june-14/)
* [coding period week 3](https://mayukhdeb.github.io/blog/post/gsoc-2020-june-21/)
* [coding period week 5](https://mayukhdeb.github.io/blog/post/gsoc-2020-july-5/)


