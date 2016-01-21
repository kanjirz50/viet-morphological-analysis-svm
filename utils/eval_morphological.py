#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
精度と再現率
"""

import sys

def main():
    # 再現率と適合率を計算するための総数を保持する
    correct_sum = 0 # 正解の総数
    true_bounds_sum = 0 # 正解の境界の総数
    answers_bounds_sum = 0 # システム出力の境界の総数

    # 標準入力から入力
    for trues, answers in stdin2trues_answers():
        # 正解とシステム出力の境界を取得
        true_bounds = IOB2chunk_nums(trues)
        answers_bounds = IOB2chunk_nums(answers)

        # 正解数を取得
        correct_num = len(check_correct(true_bounds, answers_bounds))

        # 総数に追加
        correct_sum += correct_num
        true_bounds_sum += len(true_bounds)
        answers_bounds_sum += len(answers_bounds)

    # 再現率、適合率、F値を計算する。
    recall, presicion, f_measure = 0.0, 0.0, 0.0
    try:
        recall = 100.0 * correct_sum / true_bounds_sum
        presicion = 100.0 * correct_sum / answers_bounds_sum

        f_measure = (2.0 * recall * presicion) / (recall + presicion)
    except:
        pass

    print "Recall：{0}\nPrecision：{1}\nF-value：{2}".format(recall, presicion, f_measure)

def check_correct(true_bounds, answer_bounds):
    """正解数を返す"""
    return set(true_bounds) & set(answer_bounds)

def stdin2trues_answers():
    """IOB2フォーマットを標準入力する。"""
    trues = []
    answers = []
    for line in sys.stdin:
        line = line.rstrip()
        if line == "":
            yield (trues, answers)
            trues = []
            answers = []
        else:
            lemma, true_answer, answer = line.split()
            trues.append(true_answer)
            answers.append(answer)

def IOB2chunk_nums(IOB2tags):
    """
    IOB2タグによるチャンキングを境界で要素を区切る。
    一つの要素は(単語境界の開始位置, 単語境界の終了位置, タグ)
    """
    word_bounds = []
    tags = []
    priv_word_bound = 0
    n = len(IOB2tags)
    i = 0
    for i in xrange(n - 1):
        tags.append(IOB2tags[i].split("-")[1])
        if IOB2tags[i + 1].split("-")[0] == 'B':
            word_bounds.append((priv_word_bound, i + 1, "_".join(tags)))
            priv_word_bound = i + 1
            tags = []
    else:
        if IOB2tags[i].split("-")[0] == 'I' and IOB2tags[0].split("-")[0] == 'B':
            word_bounds.append((priv_word_bound, i + 2, "_".join(tags)))
    return word_bounds


if __name__ == "__main__":
    main()
