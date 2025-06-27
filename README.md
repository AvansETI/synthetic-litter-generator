## Synthetic litter data generator

A small Proof of Concept Python project to create synthetic litter data in Blender.

![image](https://github.com/user-attachments/assets/71aa398a-c1d0-4af4-9c4d-a116b3ca96a9)

## Description

Litter is a world-wide problem where the litter can vary to many different and unique objects. Training an algorithm on litter images is possible, but it requires a substantial amount of images of each litter item. 
This means you need dozens of images of cigarettes, plastic bottles, candy wraps, and the list goes on. There are always under represented categories, even in litter. Fortunately, it is possible to balance these with
the work of synthetic data. This project aims to create synthetic litter data with the work of 3D models, Python and Blender.

## Installation

- Pycharm - A Python IDE [Download](https://www.jetbrains.com/pycharm/download/?section=windows)
- Blender version 4.4.3 [Download](https://www.blender.org/download/releases/4-4/)

1. In Blender, go to `Edit` -> `Preferences` -> `Add-Ons`
2. Install the Python script as Add-On
3. Assert that a tab 'LitterGen' is present at the screen

It is optional to integrate a virtual environment or conda environment.

## Functionalities

1. Clear Blender environment and set Camera and Light
2. Import a canvas model
3. Import a litter object model
4. Select the amount of images to render
5. Randomizer of camera, light, and litter item
6. Render of synthetic litter images

![4_littergen_render](https://github.com/user-attachments/assets/4c5ecbb9-a94b-41c6-b144-8acb2bd6f77a)
![10_littergen_render](https://github.com/user-attachments/assets/97a95888-f75f-4b91-ad26-2c622e6c7fe1)
![33_littergen_render](https://github.com/user-attachments/assets/427223b5-0e98-48d5-8d37-5d8b5bf76a6a)
![45_littergen_render](https://github.com/user-attachments/assets/f0cacb96-0dea-4e35-bfc5-acdd46807133)

## Missing functionalities

1. Integration with [Tencent/Hunyuan3D-2.1](https://huggingface.co/spaces/tencent/Hunyuan3D-2.1):
This integration could have led to more 3D models through an integration of Blender, and a bigger variation of results. Unfortunatly, Hunyuan required too much computing power and the installation process was difficult to follow.
2. Perfect layering:
It sometimes happens that the litter object goes through the canvas or out of the 'bounds'. Due to time limitations this is not worked out.
3. Litter object modifications:
Adding damage, scratches, and bendings to the object probably increase the possible realness.

