from UDPipe.articlesToPandas import getDF
from misc.text_processing import process_df
from gensim.models import Doc2Vec
from datetime import datetime
import time
from tqdm import tqdm
from misc import text_processing
from misc.doc2vec import EpochLogger
from gensim.matutils import cossim, dense2vec
import pandas as pd

m = Doc2Vec.load("../misc/models/doc2vec_2019.model")


def calculate_single_document_vector(document=None, model=m):
    """
    Calculate vector from a single document
    Parameters
    ----------
    document: str
        A list of words. Should be preprocessed
    model: Doc2Vec
        A pre-trained doc2vec model

    Returns
    -------
    list
    """
    if document is None:
        return []

    return m.infer_vector(document.split())


def calculate_document_vectors(df, col='cleaned_text', new='d2v_vector', model=m):
    """
    Take a pandas dataframe and for each document, calculate vector
    Parameters
    ----------
    df: DataFrame
    col: str
        Column where old text is saved
    new: str
        New column to add
    model: Doc2Vec
        A pre-trained Doc2Vec model

    Returns
    -------
    DataFrame
    """
    if col not in df.columns:
        raise ValueError("Given dataframe doesn't have text column", col, ". Columns:", df.columns)

    df[new] = df.apply(lambda row: calculate_single_document_vector(row[col], model=model), axis=1)
    return df


def calculate_similarity(df, similarity_threshold=0.6, model=m, verbose=False):
    """
    Take a pandas dataframe and add a new column with similarity scores

    Parameters
    ----------
    df: DataFrame
        A pandas dataframe.
    similarity_threshold: float
        Minimum similarity threshold below which similarity will be ignored
    model: Dov2Vec
        A pre-trained Doc2Vec model
    verbose: bool
        Whether to show detailed output or not

    Returns
    -------
    DataFrame
    """
    similarity_scores = []
    df_v = calculate_document_vectors(df, model=model)
    num_articles = len(df_v)

    for article in df_v.itertuples():
        if verbose:
            print("Processing ", article.url, " [", article[0], "/", num_articles, "]",
                  " - ", datetime.strftime(datetime.now(), "%H:%M:%S"), sep="")
        score = {}
        for compared in df_v.itertuples():
            # don't compare with current article
            if article.url == compared.url:
                continue
            similarity = cossim(dense2vec(article.d2v_vector), dense2vec(compared.d2v_vector))
            if similarity > similarity_threshold:
                score[compared.url] = similarity
        similarity_scores.append(score)

    df_v['d2v_sim'] = pd.Series(similarity_scores)
    df_v['d2v_dup_count'] = df_v.apply(lambda row: len(row.d2v_sim), axis=1)
    return df_v


if __name__ == "__main__":
    df = process_df(getDF().head(1000))
    res = calculate_similarity(df, verbose=True)
    res.to_csv("res_dummy.csv")
    print(res)
    print("Import this file to perform doc2vec")
