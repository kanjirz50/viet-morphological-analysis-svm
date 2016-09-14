#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script converts vnPOS corpus format to Yamcha training format.
"""

from __future__ import print_function
import sys
import re

def main():
    for line in sys.stdin:
        sentence = line.rstrip()
        words = sentence.split(' ')

        fixed_words = fix_wrong(words)

        splited_words = [split_vnpos(word) for word in fixed_words]
        morphs = words2morphs(splited_words)

        print_morphs(morphs)

def split_vnpos(vnpos_elem):
    """
    :param str vnpos_elem:
    """
    word, pos = vnpos_elem.rsplit('\t', 1)
    pos = pos_conv(pos)
    return (word, pos)

def pos_conv(pos):
    """
    :param str pos:
    """
    # Uppercasing
    if pos.isalpha():
        pos = pos.upper()
        # fix tags
        if pos == 'CN':
            return 'CC'
        elif pos == 'DN':
            return 'D'
        elif pos == 'N':
            return 'NN'
        else:
            return pos.upper()
    # Convert Symbols POS to SB
    else:
        return 'SB'

def words2morphs(words):
    """
    Convert words to syllables
    :param list words:
    """
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
    """
    Print syllables
    :param list morphs:
    """
    iob = '{}\t{}-{}'
    for lemma, iob_tag, pos in morphs:
        print(iob.format(lemma, iob_tag, pos))
    else:
        print('')


def fix_wrong(words):
    """
    Fix wrong sentence in vnPOS corpus.
    :param list words:
    """
    fixed_words = []

    for word in words:
        # For "////"
        if re.match(r'/{3,}', word) is not None:
            word = '/\t/'
            fixed_words.append(word)

        # For URL
        elif re.match(r'http://', word) is not None:
            word = re.sub(r'(http://\S+)//(NP)', r'\1\t\2', word)
            fixed_words.append(word)

        # For ".//.Theo//NP" ,forget to insert space.
        elif len(re.findall(r'//', word)) == 2:
            if re.match(r'(\S+)//\1(\S+//\S+)', word) is None:
                word = re.sub(r'(\S+)//(VB|NP|NN|JJ|B|DN|NC)(\S+//\S+)', r'\1//\2__\3', word)
            else:
                word = re.sub(r'(\S+)//\1(\S+//\S+)', r'\1//\1__\2', word)

            temp_words = word.split('__')
            fixed_words.extend([temp_word.replace('//', '\t') for temp_word in temp_words])

        # For normal format
        else:
            word = word.replace('//', '\t')
            fixed_words.append(word)

    return fixed_words

if __name__ == "__main__":
    main()
