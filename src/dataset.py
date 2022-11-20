from datasets import load_dataset, Features, ClassLabel, Value

class_names = ["Negative", "Positive"]
sentiment_feats = Features({
    'text': Value('string'),
    'label': ClassLabel(names=class_names)
})
VNMWordSegmentedDataset = load_dataset("csv",
                                       data_files={
                                        "train": "../train.csv",
                                        "test": "../train.csv"
                                       },
                                       features=sentiment_feats)
# print(dataset['train'].features)