# CS222: MRI Tumor Detection with Image Classification
created by,
- Gloria Wang, role: Prepared data, trained vision transformer model, and used model for prediction.
- Kyler Yu, role: Built frontend Flask app and middleware to run user uploaded images through the model and display output
- Owen Shi, role: Worked on frontend, experimented with different methods of storing/uploading images
- Nikunj Tyagi, role: Trained PyTorch convolutional model, worked on shading tumors red, started frontend

## Introduction
We perform image classification for brain tumors, specifically for glioma cancer, using a Vision Transformer (ViT) model trained from scratch and implemented via PyTorch. We trained our model on a manually constructed dataset of size 1091, combined from two separate datasets: the IXI dataset for healthy brain scans and a PLOS dataset for glioma scans. Our model's hyperparameters are 30 epochs with a 0.001 learning rate and a batch size of 32. We perform predictions by pulling images from a Google Drive folder.

## Installation and Setup
Clone the GitHub repo
```shell
git clone https://github.com/CS222-UIUC/course-project-mri-detector.git
```
Open ```ViT_Model.ipynb```.
Go to **Setting Up** and run the two cells.
Scroll to **Prediction** and run those two cells as well.

Make sure to either 
1. change the file paths for the prediction image folder and checkpoint
2. make sure your Colab directory follows the structure below
```
contents
├── gdrive
│   ├── MyDrive
│   │   ├── Colab Notebooks
│   │   │   ├── Datasets
│   │   │   │   ├── 222_Predictions
│   │   │   │   │   └── <filename>.png
│   │   │   │   ├── IXI-T1.tar
│   │   │   │   └── archive.zip
│   │   │   │   ├── model_checkpoint.pth
└── sample_data
```

## Technical Architecture
![image](https://user-images.githubusercontent.com/46012821/235559764-47464e1c-dfc6-47fd-84d0-4bec8936831d.png)

### Dataset
- [Healthy](https://brain-development.org/ixi-dataset/)
- [Tumor](https://www.kaggle.com/datasets/denizkavi1/brain-tumor)

### ML Model
#### About Vision Transformers
First introduced in 2020 by Google Brain, ViT is a powerful and efficient model that translates the popular Transformer models in NLP to computer vision.

#### Model Architecture

![image.png](https://viso.ai/wp-content/uploads/2021/09/vision-transformer-vit.png)

As we can see, an image is broken into patches of fixed size like 16x16 or 32x32 (which is why "An Image is worth 16x16 words").

The patches are flattened and sent to the encoder through a linear projection. To keep track of where each patch is, a positional embedding vector is also sent into the encoder as an input.

![image1.png](https://github.com/lucidrains/vit-pytorch/raw/main/images/vit.gif)

The first token of the transformer is special.

The encoder then combines the patches with the positional embedding vector. Its output is passed directly into an MLP to obtain a classification output.

#### Usage
We use PyTorch and the ViT_PyTorch library by [lucidrains](https://github.com/lucidrains/vit-pytorch) to implement ViT for image classification.

### Frontend
We created a Flask app for the frontend. The app allows the user to input an image, which the app then runs through the model checkpoint. The output of the model is then displayed on the app for the user to see.
