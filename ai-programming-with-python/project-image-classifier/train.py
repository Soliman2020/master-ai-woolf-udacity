# ==========================================================================================
# train.py (Pasted from previous response)
# ==========================================================================================
import torch
from torch import nn
from torch import optim
from torchvision import datasets, transforms, models
from collections import OrderedDict
import argparse
import os

def get_input_args():
    parser = argparse.ArgumentParser(description='Train a new image classifier network.')
    parser.add_argument('data_dir', type=str, 
                        help='Path to the dataset directory (e.g., flowers)')
    parser.add_argument('--save_dir', type=str, default='.',
                        help='Directory to save checkpoints')
    parser.add_argument('--arch', type=str, default='vgg16', 
                        choices=['vgg16', 'densenet121'],
                        help='Pre-trained model architecture to use (vgg16 or densenet121)')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                        help='Model learning rate')
    parser.add_argument('--hidden_units', type=int, default=4096,
                        help='Number of hidden units in the classifier')
    parser.add_argument('--epochs', type=int, default=3,
                        help='Number of training epochs')
    parser.add_argument('--gpu', action='store_true',
                        help='Use GPU for training if available')
    return parser.parse_args()

def get_data_loaders(data_dir):
    train_dir = os.path.join(data_dir, 'train')
    valid_dir = os.path.join(data_dir, 'valid')
    test_dir = os.path.join(data_dir, 'test')
    
    train_transforms = transforms.Compose([
        transforms.RandomRotation(30),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    valid_test_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    train_data = datasets.ImageFolder(train_dir, transform=train_transforms)
    valid_data = datasets.ImageFolder(valid_dir, transform=valid_test_transforms)
    test_data = datasets.ImageFolder(test_dir, transform=valid_test_transforms)
    
    trainloader = torch.utils.data.DataLoader(train_data, batch_size=64, shuffle=True)
    validloader = torch.utils.data.DataLoader(valid_data, batch_size=64)
    testloader = torch.utils.data.DataLoader(test_data, batch_size=64)
    
    return trainloader, validloader, testloader, train_data.class_to_idx

def build_model(arch, hidden_units):
    if arch == 'vgg16':
        model = models.vgg16(pretrained=True)
        input_size = model.classifier[0].in_features
    elif arch == 'densenet121':
        model = models.densenet121(pretrained=True)
        input_size = model.classifier.in_features
    else:
        raise ValueError(f"Architecture '{arch}' not supported. Choose 'vgg16' or 'densenet121'.")

    for param in model.parameters():
        param.requires_grad = False
    
    output_size = 102
    
    classifier = nn.Sequential(OrderedDict([
        ('fc1', nn.Linear(input_size, hidden_units)),
        ('relu1', nn.ReLU()),
        ('dropout1', nn.Dropout(0.2)),
        ('fc2', nn.Linear(hidden_units, output_size)),
        ('output', nn.LogSoftmax(dim=1))
    ]))
    
    if arch == 'vgg16':
        model.classifier = classifier
    elif arch == 'densenet121':
        model.classifier = classifier
        
    return model, input_size

def validate_model(model, criterion, validloader, device):
    valid_loss = 0
    accuracy = 0
    model.eval()
    
    with torch.no_grad():
        for inputs, labels in validloader:
            inputs, labels = inputs.to(device), labels.to(device)
            logps = model.forward(inputs)
            batch_loss = criterion(logps, labels)
            
            valid_loss += batch_loss.item()
            
            ps = torch.exp(logps)
            top_p, top_class = ps.topk(1, dim=1)
            equals = top_class == labels.view(*top_class.shape)
            accuracy += torch.mean(equals.type(torch.FloatTensor)).item()
            
    return valid_loss/len(validloader), accuracy/len(validloader)

def train_model(model, trainloader, validloader, criterion, optimizer, epochs, device):
    print_every = 40
    steps = 0
    
    model.to(device)
    
    for epoch in range(epochs):
        running_loss = 0
        model.train()
        for inputs, labels in trainloader:
            steps += 1
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            logps = model.forward(inputs)
            loss = criterion(logps, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            if steps % print_every == 0:
                valid_loss, valid_accuracy = validate_model(model, criterion, validloader, device)

                print(f"Epoch {epoch+1}/{epochs}.. "
                      f"Train Loss: {running_loss/print_every:.3f}.. "
                      f"Validation Loss: {valid_loss:.3f}.. "
                      f"Validation Accuracy: {valid_accuracy:.3f}")
                
                running_loss = 0
                model.train()
                
    print("Training complete.")


def save_checkpoint(model, input_size, arch, class_to_idx, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    
    checkpoint = {
        'input_size': input_size,
        'output_size': 102,
        'structure': arch,
        'classifier': model.classifier,
        'state_dict': model.state_dict(),
        'class_to_idx': class_to_idx
    }

    checkpoint_path = os.path.join(save_dir, 'checkpoint.pth')
    # Save with weights_only=False for compatibility when loading in the future
    torch.save(checkpoint, checkpoint_path) 
    print(f"Model checkpoint saved to {checkpoint_path}")


def main():
    args = get_input_args()
    
    device = torch.device("cuda" if args.gpu and torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    trainloader, validloader, testloader, class_to_idx = get_data_loaders(args.data_dir)
    print("Data loading complete.")

    model, input_size = build_model(args.arch, args.hidden_units)
    
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=args.learning_rate)
    
    print(f"Starting training with architecture: {args.arch}, LR: {args.learning_rate}, Epochs: {args.epochs}, Hidden Units: {args.hidden_units}")

    train_model(model, trainloader, validloader, criterion, optimizer, args.epochs, device)
    
    model.class_to_idx = class_to_idx
    save_checkpoint(model, input_size, args.arch, class_to_idx, args.save_dir)


if __name__ == '__main__':
    main()
