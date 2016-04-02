# -*- coding: utf-8 -*-
from unittest import TestCase

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dsl import read
from pyglossary.glossary import Glossary

encoding = 'utf8'

class TestRead(TestCase):

    def test_word_abalone(self):
        g = Glossary(ui=self)
        filename = '../../../../dsl_to_json/dictionary/tests/En-Ru-Apresyan_abalone.dsl'
        read(g, filename, encoding)
        after = g._data[0][1]
        before = '{"text":"abalone","def":[{"area":"зоол.","ts":",æbə\'ləʋnı","trn":[{"tr":[{"text":"морское ушко (<i>Haliotis spp.</i>; <i>съедобный моллюск</i>)"}]}],"class":"n"}]}'
        self.assertEqual(after, before)

    def test_word_abaft(self):
        g = Glossary(ui=self)
        filename = '../../../../dsl_to_json/dictionary/tests/En-Ru-Apresyan_abaft.dsl'
        read(g, filename, encoding)
        after = g._data[0][1]
        before = '''{"text":"abaft","def":[{"trn":[{"tr":[{"text":"на корме <i>или</i> по направлению к корме"}]}],"area":"мор.","ts":"ə'bɑ:ft","numB":"1","class":"adv"},{"trn":[{"tr":[{"text":"сзади","syn":[{"text":"позади"}]},{"text":"за"}],"ex":[{"text":"abaft the beam","tr":"позади траверза"}]}],"area":"мор.","ts":"ə'bɑ:ft","numB":"2","class":"prep"}]}'''
        self.assertEqual(after, before)

    def test_word_abampere(self):
        g = Glossary(ui=self)
        filename = '../../../../dsl_to_json/dictionary/tests/En-Ru-Apresyan_abampere.dsl'
        read(g, filename, encoding)
        after = g._data[0][1]
        before = '''{"text":"abampere","def":[{"trn":[{"tr":[{"text":"единица силы тока СГСМ"}]}],"ts":"æ'bæmpeə","class":"n"}]}'''
        self.assertEqual(after, before)

