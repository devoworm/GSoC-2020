# OpenDevoCell - Platform to connect all logistics of DevoWorm Group at one place.

## Goals of OpenDevoCell

This project will focus on improving the data science and machine learning infrastructure of the DevoWorm group. The work will focus on an extension of the Summer of Code projects completed in 2017 [1] and 2019 [2]. The first two aims are to improve upon the OpenDevoCell web interface (https://open-devo-cell.herokuapp.com/) and to improve segmentation techniques overall. While the OpenDevoCell interface has been implemented as a Heroku app, we would like to develop a dashboard for interpretation as well as tighter integration with DevoZoo's (https://devoworm.github.io/devozoo.htm) collection of open-source microscopy data. The third aim is to deploy the code package as a unified Python library, which would be done in concert with the improvement of segmentation techniques.

The priority for this Summer is to improve the web interface both in terms of interactivity and functionality. Ideally, we would like to provide users with multiple options for analysis. This includes the ability to incorporate new forms of analysis as well as algorithms for new types of data. Currently, our web app is optimized for microscopy images acquired using the SPIM technique. However, we would also like to segment microscopy images acquired using a wide range of technologies. Feeding into this is the ability to segment and obtain features for the data in our DevoZoo. The ability to extract quantitative data from these movie images is key to conducting the comparative and time-series analysis. The development of a dashboard would ideally enable users to employ various machine learning and simulation techniques in one place.

These improvements are meant to increase participation in our open science initiative and make sophisticated analytical techniques more accessible to students and potential collaborators alike. We are looking for someone who can work with programming tools, including HTML/CSS, TensorFlow, ReactJS, and Python. Improvements to segmentation performance might include the implementation of a pre-trained model such as Deeplab [3] or a means to plug in new components as they are developed. You will join the DevoWorm group, a project within the OpenWorm Foundation (http://openworm.org/), where we are trying to build the first virtual organism

## Unified Model Diagram for User Interaction.

The Below diagram is the main flow for how the user is going to interact with the OpenDevocell Portal.

![alt text](https://github.com/ujjwalll/GSoC-2020/blob/master/OpenDevoCell%20Integration/Images_Readme/OpenDevoCell_UML.png?raw=true)

## Splash page for OpenDevoCell
<p align="center"> 
<img src="https://github.com/devoworm/GSoC-2020/blob/master/OpenDevoCell%20Integration/Images_Readme/DEMO.gif" width="1000" height="500">
</p>
