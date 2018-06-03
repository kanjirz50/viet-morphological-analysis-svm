import pytest

from visvmtagger import Tagger


def test_tokenize():
    t = Tagger()
    tokens = t.tokenize("Số điện thoại của trường .")

    assert tokens[0].surface == "Số"
    assert tokens[0].pos == "B-NC"
