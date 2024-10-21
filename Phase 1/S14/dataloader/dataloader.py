# dataloader/dataloader.py

import os
import sys
import requests
from collections import namedtuple
from contextlib import contextmanager
from .preprocessors import default_preprocess
from .utils import download_file, timer, cached_property
import csv
from PIL import Image
import numpy as np
from typing import List, Callable, Any, Generator

DataSample = namedtuple('DataSample', ['features', 'label'])

class DataLoader:
    def __init__(self, dataset_name='MNIST', batch_size=32, shuffle=True, **kwargs):
        self.dataset_name = dataset_name
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.kwargs = kwargs
        self.data: List[DataSample] = []
        self.index = 0
        self.load_data()
    
    @timer
    def load_data(self):
        if not os.path.exists(f'datasets/{self.dataset_name}'):
            self.download_dataset()
        self.data = list(self.preprocess_data(self.read_data()))
    
    @timer
    def download_dataset(self):
        print(f"Downloading {self.dataset_name} dataset...")
        url = self.get_dataset_url()
        download_file(url, f'datasets/{self.dataset_name}')
    
    def get_dataset_url(self):
        # Define URLs for different datasets
        urls = {
            'MNIST': 'http://yann.lecun.com/exdb/mnist/',
            'CIFAR-10': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
            'CIFAR-100': 'https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz',
        }
        return urls.get(self.dataset_name, '')
    
    def read_data(self) -> Generator[DataSample, None, None]:
        data_path = f'datasets/{self.dataset_name}'
        
        if self.dataset_name in ['MNIST', 'CIFAR-10', 'CIFAR-100']:
            yield from self._read_image_data(data_path)
        elif self.dataset_name.endswith('.csv'):
            yield from self._read_csv_data(data_path)
        else:
            yield from self._read_unstructured_data(data_path)
    
    def _read_image_data(self, data_path: str) -> Generator[DataSample, None, None]:
        for root, _, files in os.walk(data_path):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(root, file)
                    try:
                        with Image.open(img_path) as img:
                            label = int(os.path.basename(root))
                            yield DataSample(features=np.array(img), label=label)
                    except IOError:
                        print(f"Error reading image: {img_path}")
    
    def _read_csv_data(self, data_path: str) -> Generator[DataSample, None, None]:
        try:
            with open(data_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    features = [float(x) for x in row[:-1]]
                    label = int(row[-1])
                    yield DataSample(features=features, label=label)
        except (IOError, ValueError) as e:
            print(f"Error reading CSV file: {e}")
    
    def _read_unstructured_data(self, data_path: str) -> Generator[DataSample, None, None]:
        for root, _, files in os.walk(data_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    label = os.path.basename(root)
                    yield DataSample(features=content, label=label)
                except IOError:
                    print(f"Error reading file: {file_path}")
    
    def preprocess_data(self, data: Generator[DataSample, None, None]) -> Generator[DataSample, None, None]:
        preprocess_func = self.kwargs.get('preprocess_func', default_preprocess)
        return map(preprocess_func, data)
    
    def __iter__(self):
        self.index = 0
        if self.shuffle:
            import random
            random.shuffle(self.data)
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            batch = self.data[self.index:self.index + self.batch_size]
            self.index += self.batch_size
            return batch
        else:
            raise StopIteration

    @contextmanager
    def batch_context(self):
        try:
            yield self
        finally:
            self.index = 0

    @cached_property
    def data_statistics(self):
        if not self.data:
            return None
        
        num_features = len(self.data[0].features)
        feature_sums = [sum(sample.features[i] for sample in self.data) for i in range(num_features)]
        feature_means = [sum_i / len(self.data) for sum_i in feature_sums]
        
        return {
            "num_samples": len(self.data),
            "num_features": num_features,
            "feature_means": feature_means
        }

    def apply_transformation(self, transformation: Callable[[DataSample], DataSample]):
        self.data = list(map(transformation, self.data))

    def filter_data(self, condition: Callable[[DataSample], bool]):
        self.data = list(filter(condition, self.data))
