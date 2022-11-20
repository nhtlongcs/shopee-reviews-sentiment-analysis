import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
from word_seg import rdrsegmenter
from splitwords import Splitter
import re

splitter = Splitter(language='vi')


def run(paragraph):
    sentence_ls = []
    pat = re.compile(r"([.()!])")

    paragraph = pat.sub(" \\1 ", paragraph)
    new_paragraph = []
    new_w = None
    for w in paragraph.split():
        if len(w) > 3:
            new_w = splitter.split(w.upper())
        else:
            new_w = None
        new_paragraph += [
            ' '.join(new_w).lower() if new_w is not None else w.lower()
        ]
    new_paragraph = ' '.join(new_paragraph)
    sentence_ls = rdrsegmenter.word_segment(new_paragraph)
    res = []
    for sentence in sentence_ls:
        res += sentence.split('.')
    return res


# print(
#     run('Chất liệukh biet nua nma ổn nha, kh quá dày nhưng cx kh bị mỏng đâuu. Màu sắctrắng. Đúng với mô tảuii đẹp nhee, orm okk, vải trắng kh quá dày nên ra nắng hơi lộ xíu, nma kh vấn đề, đâu ne, nchung là ưng êheheh'
#         ))
import pandas as pd
from tqdm import tqdm

df = pd.read_csv(
    '/home/nhtlong/playground/zalo-ai/applybigdata/preproc/v3.csv',
    delimiter='\t')
paragraphs = df['comment'].values.tolist()
sentences = []
for paragraph in tqdm(paragraphs):
    sentences += run(paragraph)

with open(
        '/home/nhtlong/playground/zalo-ai/applybigdata/preproc/v3_sentences.txt',
        'w') as f:
    for sentence in sentences:
        f.write(sentence.strip() + '\n')
print(len(sentences))