import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
from splitwords import Splitter
import re
import pandas as pd
from tqdm import tqdm

model = RobertaForSequenceClassification.from_pretrained(
    "wonrax/phobert-base-vietnamese-sentiment")

tokenizer = AutoTokenizer.from_pretrained(
    "wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

# Just like PhoBERT: INPUT TEXT MUST BE ALREADY WORD-SEGMENTED!

splitter = Splitter(language='vi')
# sentence = "chất_lượng sản_phẩm tạm ổn"
df_txts = []
df_lbls = []
lbl_map = {
    0: 0,  # negative -> negative
    1: 1,  # positive -> positive
    2: 0,  # neutral  -> negative
}
prob_pos = []
with open(
        '/home/nhtlong/playground/zalo-ai/applybigdata/preproc/v3_sentences.txt',
        'r') as f:
    sentences = f.readlines()
    sentences = [sentence.strip() for sentence in sentences][:]
    sentences = [sentence for sentence in sentences if len(sentence) > 0]
    print(len(sentences))
    sentences_ids = [tokenizer.encode(sentence) for sentence in sentences]
    for i in tqdm(range(0, len(sentences_ids))):
        input_ids = torch.tensor([sentences_ids[i]])
        with torch.no_grad():
            out = model(input_ids)
            prob = out.logits.softmax(dim=-1)
            lbl = torch.argmax(prob, dim=-1)
            prob_pos.append(prob.tolist()[0][1])
            df_lbls.append(lbl_map[lbl.item()])

df_txts = sentences
df = pd.DataFrame({'txt': df_txts, 'lbl': df_lbls, 'prob_positve': prob_pos})
stat = df.groupby('lbl').count()
print(stat)
df.to_csv('v3_sentences_pseudo.csv', index=False)