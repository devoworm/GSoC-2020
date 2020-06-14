# Pre-Trained models for Developmental Neuroscience

[![Binder](https://camo.githubusercontent.com/bfeb5472ee3df9b7c63ea3b260dc0c679be90b97/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f72656e6465722d6e627669657765722d6f72616e67652e7376673f636f6c6f72423d66333736323626636f6c6f72413d346434643464)](https://nbviewer.jupyter.org/github/devoworm/GSoC-2020/tree/master/Pre-trained%20Models%20(DevLearning))

Pre-trained deep neural networks like ResNet are being used in various industries where they help make our lives easier. But these kinds of models are not yet being used for microscopic images on a large scale. With the right model architecture and training approaches, it is possible to get pre-trained models which would help in the research efforts of many. These models, combined with a GUI would act as a community tool which would help speed up the classification/segmentation of thousands of microscopic images and gain inferences from them.

## Deep segmentation model to extract nuclei from a C.elegans embryo
* This model was trained on the [WormImage dataset](https://www.wormimage.org/) with manually labelled masks. 
* The architeture is built on a [resNet18 backbone](https://www.researchgate.net/figure/ResNet-18-Architecture_tbl1_322476121).
* Augmentations were made within a custom instance of the `torch.utils.data.Dataset()` with the help of [albumentations](https://github.com/albumentations-team/albumentations). We had to make sure that the input image and the mask went through the exact same augmentative transforms in the pre-processing stage. 
* Interestingly enough, the model's output is less noisy than the augmented mask as seen below 

<image src= "notebooks/embryo_segmentation/images/seg_result.png" >

#### Blog posts:
* [community bonding week 1](https://mayukhdeb.github.io/blog/post/gsoc-2020-may-17/)
* [community bonding week 2](https://mayukhdeb.github.io/blog/post/gsoc-2020-may-24/)
* [community bonding week 3](https://mayukhdeb.github.io/blog/post/gsoc-2020-may-31/)
* [coding period week 1](https://mayukhdeb.github.io/blog/post/gsoc-2020-june-7/)
* [coding period week 2](https://mayukhdeb.github.io/blog/post/gsoc-2020-june-14/)


