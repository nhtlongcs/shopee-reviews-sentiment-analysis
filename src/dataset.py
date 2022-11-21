from datasets import load_dataset, Features, ClassLabel, Value

# https://huggingface.co/docs/datasets/loading#specify-features
class_names = ["Negative", "Positive"]
sentiment_feats = Features({
    'text': Value('string'),
    'label': ClassLabel(names=class_names)
})
# https://huggingface.co/docs/datasets/tabular_load#csv-files
VNMWordSegmentedDataset = load_dataset("csv",
                                       data_files={
                                           "train": "data/train.csv",
                                           "test": "data/val.csv"
                                       },
                                       features=sentiment_feats)