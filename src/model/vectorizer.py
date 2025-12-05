from sklearn.feature_extraction.text import TfidfVectorizer

def fit_vectorizer(cleaned_texts, max_features=5000):
    """
    Fit TF-IDF vectorizer on cleaned texts.
    Returns (vectorizer, X)
    """
    vec = TfidfVectorizer(max_features=max_features, ngram_range=(1,2))
    X = vec.fit_transform(cleaned_texts)
    return vec, X
