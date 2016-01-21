#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def main():
    for line in sys.stdin:
        sentence = line.rstrip()
        words = sentence.split(' ')

        splited_words = [split_vnpos(word) for word in words]
        morphs = words2morphs(splited_words)

        print_morphs(morphs)

def split_vnpos(vnpos_elem):
    word, pos = vnpos_elem.rsplit('//', 1)
    pos = pos_conv(pos)

    return (word, pos)

def pos_conv(pos):
    if pos.isalpha():
        # 品詞がアルファベットのみの場合、大文字に正規化して返す。
        return pos.upper()
    else:
        # 記号はSB
        return 'SB'

def words2morphs(words):
    # 単語列を形態素列に変換する
    B_tag = 'B'
    I_tag = 'I'
    morphs = []
    for lemma, pos in words:
        if '_' in lemma:
            morphs.append((lemma.split('_')[0], B_tag, pos))

            for w in lemma.split('_')[1:]:
                morphs.append((w, I_tag, pos))
        else:
            morphs.append((lemma, B_tag, pos))
    return morphs

def print_morphs(morphs):
    iob = '{}\t{}-{}'
    for lemma, iob_tag, pos in morphs:
        print iob.format(lemma, iob_tag, pos)
    else:
        print ''

if __name__ == "__main__":
    main()
