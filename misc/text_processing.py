"""
Take an input dataframe and process the column "text". Adds a new column "clean_text" after following transformations:
 - Convert to lower case
 - Remove punctuation
 - Remove stopwords
"""

from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words('spanish'))


def process_text(text):
    """
    Take input string and return cleaned string
    Parameters
    ----------
    text: str

    Returns
    -------
    str
    """
    if text is None:
        return ""

    text = text.lower()

    # remove punctuation
    # https://stackoverflow.com/a/266162
    text = text.translate(str.maketrans('', '', string.punctuation))

    # remove stopwords
    return " ".join(word for word in text.split() if word not in stop_words)


def process_df(df, col="text", new="cleaned_text"):
    """
    Take input dataframe with optional 'col' and add a new column with cleaned text
    Parameters
    ----------
    df: DataFrame
    col: str
        Name of column with text data
    new: str
        Name of new column to create

    Returns
    -------
    DataFrame
    """
    if col not in df.columns:
        raise ValueError("Column", col, "is not present in the dataframe")

    df[new] = df[col].apply(process_text)
    return df


if __name__ == "__main__":
    inp = input("Enter text you want to clean: ")
    cleaned = process_text(inp)
    print(cleaned)
    print("Original length:", len(inp))
    print("Cleaned length:", len(cleaned))
