# https://huggingface.co/docs/transformers/tasks/sequence_classification

from model import RobertaForSequenceClassification
from dataset import VNMWordSegmentedDataset
from transformers import TrainingArguments, Trainer, AutoTokenizer, DataCollatorWithPadding
import evaluate
import numpy as np


def compute_metrics(eval_pred):
    # https://discuss.huggingface.co/t/log-multiple-metrics-while-training/8115/4
    f1_func = evaluate.load("f1")
    pr_func = evaluate.load("precision")
    rc_func = evaluate.load("recall")
    acc_func = evaluate.load("accuracy")

    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision = pr_func.compute(predictions=predictions,
                                references=labels)["precision"]
    recall = rc_func.compute(predictions=predictions,
                             references=labels)["recall"]
    acc = acc_func.compute(predictions=predictions,
                           references=labels)["accuracy"]
    f1 = f1_func.compute(predictions=predictions, references=labels)["f1"]
    return {
        "accuracy": acc,
        "f1": f1,
        "precision": precision,
        "recall": recall,
    }


model = RobertaForSequenceClassification.from_pretrained(
    "vinai/phobert-base", num_labels=2, ignore_mismatched_sizes=True)

dataset = VNMWordSegmentedDataset

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)


def tokenize_func(batch):
    return tokenizer(
        batch['text'],
        padding=True,
    )


tokenized_datasets = dataset.map(tokenize_func, batched=True)

train_dataset = tokenized_datasets['train'].shuffle(seed=42)
valid_dataset = tokenized_datasets['test'].shuffle(seed=43)

# https://huggingface.co/docs/transformers/training#finetune-with-trainer
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=20,
    weight_decay=0.01,
    evaluation_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()