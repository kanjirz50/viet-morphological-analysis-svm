#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys

class YamCha:
    def __init__(self, model_path):
        """YamChaの設定"""
        # subprocessモジュールで扱うためのコマンド
        self.cmd = ('yamcha', '-m', model_path)

    def analyze(self, sentence):
        # 入力文を解析
        p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # 末尾の要素2つの空要素となるため、削除する
        yamcha_result = p.communicate(self.sentence2iob_format(sentence))[0].split('\n')[:-2]
        return self.yamcha_result2iob_format(yamcha_result)

    def sentence2iob_format(self, sentence):
        """入力文をIOB2フォーマットへ変換する"""
        syllables = sentence.split(' ')
        # YamChaは標準入力で1行1音節の要素を渡し、最後に文末を示すEOSを挿入
        syllables.append('EOS')
        return '\n'.join(syllables)

    def yamcha_result2iob_format(self, yamcha_result):
        # YamChaの結果をIOB2タグ形式のタプルへ変換する
        return [(line.rstrip().split('\t')) for line in yamcha_result]
