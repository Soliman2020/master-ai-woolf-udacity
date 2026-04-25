# ==========================================================================================
# predict.py (Pasted from previous response)
# ==========================================================================================

import torch
from torch import nn
from torchvision import models
from PIL import Image
import numpy as np
import json
import argparse
import os
from collections import OrderedDict

def get_input_args():
    parser = argparse.ArgumentParser(description='Predict flower class from an image.')
    parser.add_argument('image_path', type=str, 
                        help='Path to the image file')
    parser.add_argument('checkpoint', type=str, 
                        help='Path to the model checkpoint file')
    parser.add_argument('--top_k', type=int, default=1,
                        help='Return the top K most likely classes')
    parser.add_argument('--category_names', type=str, default='cat_to_name.json',
                        help='Path to a JSON file mapping categories to real names')
    parser.add_argument('--gpu', action='store_true',
                        help='Use GPU for inference if available')
    return parser.parse_args()


def load_checkpoint(filepath):
    """
    Loads a checkpoint file and rebuilds the model.
    """
    # Use weights_only=False to load the custom Sequential object safely
    checkpoint = torch.load(filepath, weights_only=False)
    
    arch = checkpoint['structure']
    
    if arch == 'vgg16':
        model = models.vgg16(pretrained=True)
    elif arch == 'densenet121':
        model = models.densenet121(pretrained=True)
    else:
        raise ValueError(f"Unsupported architecture: {arch}")
        
    # Freeze parameters
    for param in model.parameters():
        param.requires_grad = False
        
    # Load the classifier and state dictionary
    model.classifier = checkpoint['classifier']
    model.load_state_dict(checkpoint['state_dict'])
    model.class_to_idx = checkpoint['class_to_idx']
    
    return model, arch


def process_image(image_path):
    ''' Scales, crops, and normalizes a PIL image for a PyTorch model,
        returns an Numpy array.
    '''
    img = Image.open(image_path)

    # 1. Resize: shortest side to 256
    if img.size[0] > img.size[1]:   # landscape
        img.thumbnail((10000, 256))
    else:                           # portrait
        img.thumbnail((256, 10000))

    # 2. Crop: center 224x224
    left = (img.width - 224) / 2
    bottom = (img.height - 224) / 2
    right = left + 224
    top = bottom + 224
    img = img.crop((left, bottom, right, top))

    # 3. Normalize: Convert to 0-1 float and normalize
    np_img = np.array(img) / 255
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    np_img = (np_img - mean) / std

    # 4. Transpose: PyTorch expects color channel first
    np_img = np_img.transpose((2, 0, 1))

    return np_img


def predict(image_path, model, topk, device):
    ''' Predict the class (or classes) of an image using a trained deep learning model.
    '''
    
    model.to(device)
    model.eval()

    # Pre-process image
    img = process_image(image_path)
    
    # Convert numpy to torch tensor and add batch dimension
    img_tensor = torch.from_numpy(img).type(torch.FloatTensor)
    img_tensor = img_tensor.unsqueeze(0) 
    img_tensor = img_tensor.to(device)

    # Inference (Forward pass)
    with torch.no_grad():
        logps = model.forward(img_tensor)
        ps = torch.exp(logps)
        top_p, top_class = ps.topk(topk, dim=1)

    # Convert results to standard Python lists
    top_p = top_p.cpu().numpy()[0].tolist()
    top_class = top_class.cpu().numpy()[0].tolist()

    # Map indices back to class labels
    idx_to_class = {v: k for k, v in model.class_to_idx.items()}
    top_classes = [idx_to_class[c] for c in top_class]

    return top_p, top_classes


def main():
    args = get_input_args()
    
    device = torch.device("cuda" if args.gpu and torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load model
    model, arch = load_checkpoint(args.checkpoint)
    print(f"Model ({arch}) loaded from {args.checkpoint}.")
    
    # Load category names
    with open(args.category_names, 'r') as f:
        cat_to_name = json.load(f)
    print(f"Category names loaded from {args.category_names}.")

    # Predict
    probs, classes = predict(args.image_path, model, args.top_k, device)
    
    # Display results
    print(f"\n--- Prediction Results for {args.image_path} ---")
    
    if args.top_k == 1:
        flower_name = cat_to_name.get(classes[0], classes[0])
        print(f"The most likely flower is: {flower_name}")
        print(f"Probability: {probs[0]*100:.2f}%")
    else:
        # Create a list of (name, probability) tuples
        results = []
        for class_index, prob in zip(classes, probs):
            flower_name = cat_to_name.get(class_index, class_index)
            results.append((flower_name, prob))
        
        print(f"Top {args.top_k} Predictions:")
        for name, prob in results:
            print(f"  {name: <25}: {prob*100:.2f}%")
    
    print("-" * 40)


if __name__ == '__main__':
    main()
