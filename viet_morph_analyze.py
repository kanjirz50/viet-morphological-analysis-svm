#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import sys
import fileinput
from libs.yamcha import YamCha
from libs.conv_format import iob2word


class VietMorphAnalyzer:
    def __init__(self, model_file_path):
        self.ym_analyzer = YamCha(model_file_path)

    def analyze(self, sentence):
        return self.ym_analyzer.analyze(sentence)

def main():
    inifile = ConfigParser.SafeConfigParser()
    inifile.read("./config.ini")

    model_file_path = inifile.get("settings", "model_path")

    vm = VietMorphAnalyzer(model_file_path)

    for line in fileinput.input():
        for word, pos in iob2word(vm.analyze(line.rstrip())):
            print '{}\t{}'.format(word, pos)
        else:
            print ''

if __name__ == '__main__':
    main()