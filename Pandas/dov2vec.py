from UDPipe.articlesToPandas import getDF
from misc.text_processing import process_df
from gensim.models import Doc2Vec
from datetime import datetime
import time
from tqdm import tqdm
from misc import text_processing
from misc.doc2vec import EpochLogger
import pandas as pd

m = Doc2Vec.load("../misc/models/doc2vec_1_day.model")


def calculate_similarity(df, model=m, verbose=False):
    """
    Take a pandas dataframe and add a new column with similarity scores

    Parameters
    ----------
    df: DataFrame
        A pandas dataframe.
    model: Dov2Vec
        A pre-trained Doc2Vec model
    verbose: bool
        Whether to show detailed output or not

    Returns
    -------
    DataFrame
    """
    similarity_values = []

    # TODO: Optimize this by not comparing with already compared rows
    for article in df.itertuples():
        if verbose:
            print("Processing ", article.url, " [", article.Index, "/", len(df), "] - ",
                  datetime.strftime(datetime.now(), "%H:%M:%S"), sep="")
        current_scores = dict()
        if article.cleaned_text is None:
            continue
        for compared in df.itertuples():
            if compared.cleaned_text is None:
                continue
            current_scores[compared.url] = model.docvecs.similarity_unseen_docs(
                model, article.cleaned_text.split(), compared.cleaned_text.split())
        similarity_values.append(current_scores)
    similarity_values = df.Series().append(similarity_values)

    df['doc2vec_scores'] = similarity_values
    return df


if __name__ == "__main__":
    df = process_df(getDF())
    res = calculate_similarity(df, verbose=True)
    res.to_csv("compare_result.csv")
    print(res)
    print("Import this file to perform doc2vec")
