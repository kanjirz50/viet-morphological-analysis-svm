import re
import warnings

from logzero import logger
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC


warnings.filterwarnings("ignore", category=DeprecationWarning)


class Token:
    def __init__(self, surface, pos=None):
        self.surface = surface
        self.pos = pos

    def __str__(self):
        return f"{self.surface}({self.pos})"

    def __repr__(self):
        return self.__str__()


def load_corpus(path="../data/vnpos_corpus.txt"):
    with open(path, "r") as fin:
        return [to_tokens(sentence.rstrip()) for sentence in fin]


def to_tokens(sentence):
    tokens = []
    for token in sentence.split(" "):
        tokens.extend(split_token(token))
    return tokens


def split_token(token):
    matched = re.search(r"//\S+", token)
    split_pos = matched.span()[0]

    surface = token[:split_pos]
    pos = token[split_pos+2:].upper()

    if not re.fullmatch(r"[A-Z]+", pos):
        pos = "SB"

    if not "_" in surface:
        return [Token(surface, "B-" + pos)]

    surfaces = surface.split("_")
    tokens = [Token(surfaces[0], "B-" + pos)]
    tokens.extend([Token(s, "I-" + pos) for s in surfaces[1:]])
    return tokens


def iter_feature(tokens, templates):
    tokens_len = len(tokens)
    for i in range(tokens_len):
        feature = {"bias": 1.0}
        for label, f, target in templates:

            current = i + target
            if current < 0 or current >= tokens_len:
                continue
            feature[label] = f(tokens[current])
        if i == 0:
            feature["BOS"] = True
        elif i == tokens_len - 1:
            feature["EOS"] = True
        yield feature


def main():
    # Define features
    word_feature = lambda x: x.surface
    pos_feature = lambda x: x.pos
    templates = [
        ("word-2", word_feature, -2), ("word-1", word_feature, -1), ("word", word_feature, 0), ("word+1", word_feature, 1), ("word+2", word_feature, 2),
        ("pos-2", pos_feature, -2), ("pos-1", pos_feature, -1),
    ]

    logger.info("Loading corpus.")
    corpus = load_corpus("../data/vnpos_corpus.txt")
    features = []
    for sentence in corpus:
        features.extend(iter_feature(sentence, templates))

    logger.info("Creating features.")
    vectorizer = DictVectorizer()
    vec = vectorizer.fit_transform(features)
    joblib.dump(vectorizer, "../models/vectorizer.pkl", compress=9)

    logger.info("Encoding part-of-speech.")
    le = LabelEncoder()
    y = le.fit_transform([token.pos for sentence in corpus for token in sentence])
    joblib.dump(le, "../models/label.pkl", compress=9)

    logger.info("Start training.")
    clf = LinearSVC(verbose=True)
    clf.fit(vec, y)

    logger.info("Compressing model and save.")
    joblib.dump(clf, "../models/svc.pkl", compress=9)


if __name__ == "__main__":
    main()
