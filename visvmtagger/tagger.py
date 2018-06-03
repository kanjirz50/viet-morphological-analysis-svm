import pathlib

from sklearn.externals import joblib
from visvmtagger.train import iter_feature, Token


model_root = pathlib.Path(__file__).parent.parent.joinpath("models")

class Tagger:
    def __init__(self,
                 model=model_root.joinpath("svc.pkl"),
                 label=model_root.joinpath("label.pkl"),
                 vectorizer=model_root.joinpath("vectorizer.pkl"),
                 ):
        self.model = joblib.load(model)
        self.le = joblib.load(label)
        self.vectorizer = joblib.load(vectorizer)

        self.init_template()

    def init_template(self):
        word_feature = lambda x: x.surface
        pos_feature = lambda x: x.pos
        self.templates = [
            ("word-2", word_feature, -2), ("word-1", word_feature, -1), ("word", word_feature, 0), ("word+1", word_feature, 1), ("word+2", word_feature, 2),
            ("pos-2", pos_feature, -2), ("pos-1", pos_feature, -1),
        ]

    def tokenize(self, sentence):
        tokens = self.sentence_to_tokens(sentence)
        for token, feature in zip(tokens, iter_feature(tokens, self.templates)):
            vec = self.vectorizer.transform(feature)
            token.pos = self.le.inverse_transform(self.model.predict(vec))[0]

        return tokens

    def sentence_to_tokens(self, sentence):
        return [Token(surface=token, pos=None) for token in sentence.split(" ")]


def tokens_to_words(tokens, delimiter="_"):
    words = []
    for token in tokens:
        if token.pos.startswith("B"):
            words.append(token.surface)
        else:
            words[-1] += delimiter + token.surface
    return words


if __name__ == "__main__":
    # Example
    tagger = Tagger()
    tokens = tagger.tokenize(sentence='" ... Có ai về Bắc ta theo với')
    print("\n".join([f"{t.surface}\t{t.pos}" for t in tokens]))

    words = tokens_to_words(tokens)
    print(" ".join(words))
