import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
from word_seg import rdrsegmenter
from splitwords import Splitter
import re

model = RobertaForSequenceClassification.from_pretrained(
    "wonrax/phobert-base-vietnamese-sentiment")

tokenizer = AutoTokenizer.from_pretrained(
    "wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

# Just like PhoBERT: INPUT TEXT MUST BE ALREADY WORD-SEGMENTED!

splitter = Splitter(language='vi')
sentence = "chất_lượng sản_phẩm tạm ổn"
input_ids = torch.tensor([tokenizer.encode(sentence)])

with torch.no_grad():
    out = model(input_ids)
    print(out.logits.softmax(dim=-1).tolist())
