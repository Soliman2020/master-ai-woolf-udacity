---
title: "Deep Learning"
source: "https://learn.udacity.com/nd101?version=15.0.10&partKey=cd1818&lessonKey=f85a29b2-c4de-4093-b214-fa75cf026606&project=rubric"
author:
published:
created: 2026-02-04
description:
tags:
  - "clippings"
---
## Rubric

Use this project rubric to understand and assess the project criteria.

## Section 1: Data Loading and Exploration

| Criteria | Submission Requirements |
| --- | --- |
| Transform data for use in neural networks. | Data is preprocessed and converted to a tensor, either using the.ToTensor() transform from `torchvision.transforms` or simply manually with torch.Tensor. |
| Use `DataLoader` to input training data to the neural network. | A `DataLoader` object for both train and test sets has been created using the train and test sets loaded from `torchvision`. |
| Explore datasets and describe their properties to set and optimize neural network parameters. | Notebook contains code which shows the size and shape of the training and test data.  The provided function or some other method (e.g. plt.imshow) is used to print one or more images from the dataset |
| Provide a brief justification of any necessary preprocessing steps or why no preprocessing is needed. | The submission contains a justification of necessary preprocessing steps (e.g. flattening, converting to tensor, normalization) in a comment or (preferably) a markdown block. |

## Section 2: Model Design and Training

| Criteria | Submission Requirements |
| --- | --- |
| Use PyTorch to build a neural network for image classification. | A `Model` or `Sequential` class is created with at least two hidden layers and implements a `forward` method that outputs a prediction probability for each of the 10 classes using softmax. |
| Select an appropriate loss function for training a classification network. | A loss function that works for classification tasks is specified. |
| Define an optimizer to minimize loss function and update model parameters for improved accuracy. | Any optimizer from `torch.optim` is used to minimize the loss function. |

## Section 3: Model Testing and Evaluation

| Criteria | Submission Requirements |
| --- | --- |
| Use DataLoader and the holdout set to test the accuracy of the model. | The test `DataLoader` is used to get predictions from the neural network and compare the predictions to the true labels. |
| Optimize model hyperparameters to achieve a desired level of accuracy. | Hyperparameters are modified to attempt to improve accuracy and the model achieves at least 90% classification accuracy. |
| Save trained model parameters for later use. | The `torch.save()` function is used to save the weights of the trained model. |

## Suggestions to Make Your Project Stand Out

1. Implement a Validation set to check your accuracy at each epoch.
2. Use a more advanced architecture (e.g. convolutional neural network) and obtain even higher accuracy.
3. Contextualize your model – based on the results from Yann LeCun’s webpage, how does your model rank?

