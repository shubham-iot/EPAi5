# dataloader/preprocessors.py

import numpy as np
from PIL import Image

def default_preprocess(sample):
    return sample

def normalize(sample):
    features = np.array(sample.features).astype(np.float32) / 255.0
    return DataSample(features=features, label=sample.label)

def augment(sample):
    if isinstance(sample.features, np.ndarray):
        # Image augmentation
        img = Image.fromarray(sample.features.astype('uint8'), 'RGB')
        img = img.rotate(10)  # Rotate by 10 degrees
        return DataSample(features=np.array(img), label=sample.label)
    else:
        # Text augmentation (example: add noise)
        features = sample.features + ' ' + ''.join(np.random.choice(list('abcdefghijklmnopqrstuvwxyz'), size=5))
        return DataSample(features=features, label=sample.label)

def tokenize(sample):
    if isinstance(sample.features, str):
        tokens = sample.features.split()
        return DataSample(features=tokens, label=sample.label)
    return sample
