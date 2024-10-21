# main.py

import sys
import argparse
from dataloader import DataLoader
from dataloader.preprocessors import normalize, augment, tokenize

def main():
    parser = argparse.ArgumentParser(description="DataLoader Demo")
    parser.add_argument("--dataset", default="MNIST", help="Dataset to load (default: MNIST)")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size (default: 32)")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle the data")
    args = parser.parse_args()

    # Initialize DataLoader
    data_loader = DataLoader(dataset_name=args.dataset, batch_size=args.batch_size, 
                             shuffle=args.shuffle, preprocess_func=lambda x: normalize(augment(x)))

    # Iterate over data
    with data_loader.batch_context():
        for i, batch in enumerate(data_loader):
            print(f"Processing batch {i+1} of size {len(batch)}")
            if i == 4:  # Process 5 batches for demonstration
                break

    # Print statistics
    print("Dataset statistics:", data_loader.data_statistics)

    # Demonstrate transformation and filtering
    data_loader.apply_transformation(lambda x: DataSample(features=[f*2 for f in x.features], label=x.label))
    data_loader.filter_data(lambda x: x.label % 2 == 0)  # Keep only even-labeled samples

    print("After transformation and filtering:")
    print("Dataset statistics:", data_loader.data_statistics)

if __name__ == '__main__':
    main()
