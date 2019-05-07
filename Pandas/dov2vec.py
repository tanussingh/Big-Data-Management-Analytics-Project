from UDPipe.articlesToPandas import getDF
from misc.text_processing import process_df
from gensim.models import Doc2Vec
from datetime import datetime
import time
from tqdm import tqdm
from misc import text_processing
from misc.doc2vec import EpochLogger
import pandas as pd

m = Doc2Vec.load("../misc/models/doc2vec_2019.model")


def calculate_similarity(df, similarity_threshold=0.8, model=m, verbose=False):
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
    similarity_numbers = []
    # We can search the full index but limiting to 33% could be faster as we will definitely have more than 3 topics
    similar_docs_limit = len(df)
    current_articles = set(df['url'])

    for article in df.itertuples():
        if verbose:
            print("Processing ", article.url, " [", article.Index, "/", len(df), "] - ",
                  datetime.strftime(datetime.now(), "%H:%M:%S"), sep="")
        current_scores = dict()
        if article.cleaned_text is None:
            similarity_values.append(current_scores)
            continue
        # get top 20 most similar articles
        # similar_docs = model.docvecs.
        inferred_vector = model.infer_vector(article.cleaned_text.split())
        similarity = model.docvecs.most_similar([inferred_vector], topn=similar_docs_limit)
        # convert tuples to dictionary for easy
        similarity_dict = {doc[0]: doc[1]
                           for doc in similarity
                           if doc[0] in current_articles and doc[1] > similarity_threshold and doc[0] != article.url}
        similarity_values.append(similarity_dict)
        similarity_numbers.append(len(similarity_dict))

    similarity_values = pd.Series(similarity_values)
    similarity_numbers = pd.Series(similarity_numbers)

    df['doc2vec_scores'] = similarity_values
    df['doc2vec_duplicates'] = similarity_numbers
    return df


if __name__ == "__main__":
    df = process_df(getDF())
    res = calculate_similarity(df, verbose=True)
    res.to_csv("compare_result.csv")
    print(res)
    print("Import this file to perform doc2vec")
