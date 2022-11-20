import pandas as pd


def select_uncertainty(df, threshold_neg, threshold_pos):
    df_neg = df[df['lbl'] == 0]
    df_neg = df_neg[df_neg['prob_positve'] < threshold_neg]
    df_pos = df[df['lbl'] == 1]
    df_pos = df_pos[df_pos['prob_positve'] > threshold_pos]
    df = pd.concat([df_neg, df_pos])
    return df


def select_uncertainty_dynamic(df):
    df_neg = df[df['lbl'] == 0]
    df_neg_uncertain = df_neg[
        df_neg['prob_positve'] > df_neg['prob_positve'].quantile(0.5)]
    df_pos = df[df['lbl'] == 1]
    df_pos_uncertain = df_pos[
        df_pos['prob_positve'] < df_pos['prob_positve'].quantile(0.5)]
    uncertain_df = pd.concat([df_neg_uncertain, df_pos_uncertain])
    df = df[~df['id'].isin(uncertain_df['id'])]
    return uncertain_df, df


if __name__ == '__main__':
    rawdf = pd.read_csv('data/v3_sentences_pseudo.csv')

    uncertain_df, df = select_uncertainty_dynamic(rawdf)
    print(rawdf.shape)
    print(df.shape)
    df.to_csv('data/v3_sentences_pseudo_uncertainty.csv', index=False)