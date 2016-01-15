#!/usr/bin/env python
# -*- coding: utf-8 -*-

pos_dict = {
    'NN':'N',
    'NC':'N',
    'NP':'N',
}

def iob2word(iob_tags):
    words = []

    word_stack = []
    for lemma, pos in reversed(iob_tags):
        if pos.startswith('I'):
            word_stack.append(lemma)

        elif pos.startswith('B') and len(word_stack) == 0:
            words.append((lemma, pos_formater(pos)))

        elif pos.startswith('B') and len(word_stack) > 0:
            word_stack.append(lemma)
            words.append((' '.join(reversed(word_stack)), pos_formater(pos)))

            word_stack = []

    return reversed(words)

def pos_formater(iob2pos):
    pos = iob2pos.split('-')[1]
    if pos_dict.get(pos):
        return pos_dict.get(pos)
    else:
        return pos
