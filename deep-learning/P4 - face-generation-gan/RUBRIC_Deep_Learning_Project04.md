---
title: "Deep Learning"
source: "https://learn.udacity.com/nd101?version=15.0.10&partKey=cd1823&lessonKey=2e7428ec-40bb-46d0-84b4-4f6e30b69561&project=rubric"
author:
published:
created: 2026-02-04
description:
tags:
  - "clippings"
---
## Rubric

Use this project rubric to understand and assess the project criteria.

## Section 1: Code quality

| Criteria | Submission Requirements |
| --- | --- |
| The project code is clean and modular. | Scripts have an intuitive, easy-to-follow structure with code separated into logical functions. Naming for variables and functions follows the PEP8 style guidelines. |

## Section 2: Generator and discriminator design

| Criteria | Submission Requirements |
| --- | --- |
| The generator model should output an RGB image. | The generator should take a batched 1d latent vector as input and output a batch of RGB images (3 channels). |
| The discriminator model should output a single score for an input image. | The discriminator should take as input a batch of images and output a score for each image in the batch. |
| Generator and Discriminator are written in a torch-friendly way. | Generator and Discriminator are inheriting from the torch `Module` class. The layers are defined in the `init` method and called in the `forward` method. |

## Section 3: Data pipeline

| Criteria | Submission Requirements |
| --- | --- |
| The `get_transform` function outputs a callable of transforms that fits the requirements. | (Provide specific details on how the student will fulfill the criteria.) The `get_transform` function should output a `Compose` of different torchvision (or non torchvision) transforms. |
| The `DatasetDirectory` class is written as a map-style torch dataset. | The custom dataset should have the `__len__` and the `__get_item__` methods implemented and working. The dataset should return a tensor image in the -1 / 1 range. |

## Section 4: Loss implementation and training

| Criteria | Submission Requirements |
| --- | --- |
| The generator and discriminator loss functions are correctly implemented. | Both loss functions are accomplishing their roles: the discriminator should be trained to separate fake and real images and the generator should be trained to fool the discriminator. No specific functions are required. |
| The optimizers are correctly implemented and reasonable parameters are chosen. | Two optimizers are created, one for the generator and one for the discriminator. They are both using low learning rates. |
| The training code is running and the loss values are changing. | The ` discriminator_step` and `generator_step` functions are correctly implemented. The model is training for enough epochs. |
| The model, loss function, and training strategy are updated based on initial results. | The student makes reasonable decisions based on initial results. |
| The model generates faces. | The generated samples should have face attributes (eyes, nose, mouth, hair) and a rough resemblance to a face. |

## Suggestions to Make Your Project Stand Out

1. The student writes some additional visualization code (show more than 16 images during training, implement latent space interpolation) and log losses and images to tensorboard.
2. The student implements and experiments with multiple GAN training tricks (label smoothing, adding noise to input image, etc) and documents thoroughly the impact of each one by performing an ablation study.
3. The student implements metrics like FID to measure the performance of their model.

