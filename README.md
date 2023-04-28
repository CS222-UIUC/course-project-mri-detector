# CS222: MRI Tumor Detection using Computer Vision
created by,
- Gloria Wang
- Kyler Yu
- Owen Shi 
- Nikunj Tyagi


## Install Script


## Dataset
- [Healthy](https://brain-development.org/ixi-dataset/)
- [Tumor](https://www.kaggle.com/datasets/denizkavi1/brain-tumor)

# About Vision Transformers
First introduced in 2020 by Google Brain, ViT is a powerful and efficient model that translates the popular Transformer models in NLP to computer vision.

## Model Architecture

![image.png](https://viso.ai/wp-content/uploads/2021/09/vision-transformer-vit.png)

As we can see, an image is broken into patches of fixed size like 16x16 or 32x32 (which is why "An Image is worth 16x16 words").

The patches are flattened and sent to the encoder through a linear projection. To keep track of where each patch is, a positional embedding vector is also sent into the encoder as an input.

![image1.png](https://github.com/lucidrains/vit-pytorch/raw/main/images/vit.gif)

The first token of the transformer is special.

The encoder then combines the patches with the positional embedding vector. Its output is passed directly into an MLP to obtain a classification output.
