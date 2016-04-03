# -*- coding: utf-8 -*-
from unittest import TestCase

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dsl import read
from pyglossary.glossary import Glossary

def test_word(self, before, after):
    g = Glossary()
    read(g, '../../../../dsl_to_json/dictionary/tests/' + before, 'utf8')
    self.assertEqual(after, g._data[0][1])

class TestRead(TestCase):

    def test_word_abalone(self):
        before = 'En-Ru-Apresyan_abalone.dsl'
        after = '{"text":"abalone","def":[{"area":"зоол.","ts":",æbə\'ləʋnı","trn":[{"tr":[{"text":"морское ушко (<i>Haliotis spp.</i>; <i>съедобный моллюск</i>)"}]}],"class":"n"}]}'
        test_word(self, before, after)

    def test_word_abaft(self):
        before = 'En-Ru-Apresyan_abaft.dsl'
        after = '''{"text":"abaft","def":[{"trn":[{"tr":[{"text":"на корме <i>или</i> по направлению к корме"}]}],"area":"мор.","ts":"ə'bɑ:ft","numB":"1","class":"adv"},{"trn":[{"tr":[{"text":"сзади","syn":[{"text":"позади"}]},{"text":"за"}],"ex":[{"text":"abaft the beam","tr":"позади траверза"}]}],"area":"мор.","ts":"ə'bɑ:ft","numB":"2","class":"prep"}]}'''
        test_word(self, before, after)

    def test_word_abampere(self):
        before = 'En-Ru-Apresyan_abampere.dsl'
        after = '''{"text":"abampere","def":[{"trn":[{"tr":[{"text":"единица силы тока СГСМ"}]}],"ts":"æ'bæmpeə","class":"n"}]}'''
        test_word(self, before, after)

    def test_word_abandon(self):
        before = 'En-Ru-Apresyan_abandon.dsl'
        after = '''{"text":"abandon","hom":[{"numRB":"I","def":[{"trn":[{"tr":[{"text":"абандон"}]}],"area":"страх.","ts":"ə'bændən","numB":"1","class":"n"},{"trn":[{"num":"1","tr":[{"text":"отказываться"},{"text":"оставлять"}],"ex":[{"text":"to abandon the attempt","tr":"отказаться от попытки, прекратить попытки"},{"text":"to abandon (all) hope","tr":"оставить (всякую) надежду"},{"text":"abandon hope all ye who enter here (<i>Dante</i>)","tr":"оставь надежду всяк сюда входящий"},{"text":"the search was abandoned","tr":"поиски были прекращены"},{"text":"to abandon a custom","tr":"не сохранить /предать забвению/ обычай"},{"text":"immigrants slow to abandon their native languages","tr":"иммигранты, неохотно отказывающиеся от своего родного языка"}]},{"num":"2","tr":[{"text":"сдавать"}],"ex":[{"text":"to abandon the city to the enemy","tr":"сдать город врагу"},{"text":"to abandon oneself to the conqueror's mercy","tr":"сдаться на милость победителя"}]},{"num":"3","tr":[{"text":"покидать","syn":[{"text":"оставлять"}]},{"text":"самовольно уходить (<i>с поста </i><i data-abbr>и т. п.</i>)"}],"ex":[{"text":"to abandon smb.","tr":"бросить кого-л."},{"text":"to abandon the sinking ship","tr":"покинуть тонущий корабль"},{"text":"courage abandoned him","tr":"мужество покинуло его"}]},{"num":"4","tr":[{"text":"<i data-abbr>юр.</i> отказаться (<i>от собственности, от права </i><i data-abbr>и т. п.</i>)"}]},{"num":"5","tr":[{"text":"закрывать"},{"text":"консервировать (<i>предприятие </i><i data-abbr>и т. п.</i>)"}],"ex":[{"text":" <i data-abbr>♢</i> to abandon oneself to smth.","tr":"предаваться чему-л.; отдаваться чему-л."},{"text":"to abandon oneself to passion [despair]","tr":"предаваться страсти [отчаянию]"},{"text":"to be abandoned to smth.","tr":"предаваться чему-л.; испытывать что-л."},{"text":"to be abandoned to grief [despair]","tr":"предаться горю [отчаянию]"}]}],"ts":"ə'bændən","numB":"2","class":"v"}]},{"numRB":"II","def":[{"trn":[{"num":"1","tr":[{"text":"<i data-abbr>книжн.</i> развязность; несдержанность"}],"ex":[{"text":"to do smth. with /at, in/ (complete) abandon","tr":"делать что-л., (совершенно) забыв обо всём /отдавшись порыву/"}]},{"num":"2","tr":[{"text":"импульсивность"},{"text":"энергия"}],"ex":[{"text":"to sing with abandon","tr":"петь с чувством, забыться в песне"},{"text":"to wave one's hand with abandon","tr":"энергично размахивать рукой"},{"text":"he spoke with complete abandon","tr":"он говорил, забыв обо всём; его словно прорвало"}]}],"ts":"ə'bændən","class":"n"}]}]}'''
        test_word(self, before, after)

    def test_word_abandonment(self):
        before = 'En-Ru-Apresyan_abandonment.dsl'
        after = '''{"text":"abandonment","hom":[{"numRB":"I","def":[{"trn":[{"num":"1","tr":[{"text":"1) оставление"}]},{"tr":[{"text":"2) <i data-abbr>юр.</i> оставление жены, ребёнка"}]},{"num":"2","tr":[{"text":"заброшенность","syn":[{"text":"запущенность"}]}]},{"num":"3","tr":[{"text":"1) <i data-abbr>юр.</i> отказ (<i>от права, иска</i>)"}]},{"tr":[{"text":"2) <i data-abbr>страх.</i> абандон"}]}],"ts":"ə'bændənmənt","class":"n"}]},{"numRB":"II","def":[{"com":"<i>= abandon</i><sup>2 </sup>","ts":"ə'bændənmənt"}]}]}'''
        test_word(self, before, after)
