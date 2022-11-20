import pandas as pd

lbl_map = {
    0: 0,
    1: 1,
    2: 0,
}
df = pd.read_csv('data/automated/v3_sentences_pseudo_uncertainty.csv')
df['label'] = df['lbl'].map(lbl_map)
df['sentiment'] = df['lbl'].map({0: 'Negative', 1: 'Positive'})
df['text'] = df['txt']
df[['text', 'label']].to_csv('pseudo_labelstudio.csv', index=False)
