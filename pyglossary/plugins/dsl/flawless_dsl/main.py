# -*- coding: utf-8 -*-
# flawless_dsl/main.py
#
""" exposed API lives here."""
#
# Copyright (C) 2016 Ratijas <ratijas.t@me.com>
#
# This program is a free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# You can get a copy of GNU General Public License along this program
# But you can always get it from http://www.gnu.org/licenses/gpl.txt
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.


import copy
import re

from . import tag as _tag
from . import layer as _layer


def process_closing_tags(stack, tags):
    """
    close `tags`, closing some inner layers if necessary.

    :param stack: Iterable[layer.Layer]
    :param tags: Iterable[str]
    """
    index = len(stack) - 1
    for tag in copy.copy(tags):
        index_for_tag = _tag.index_of_layer_containing_tag(stack, tag)
        if index_for_tag is not None:
            index = min(index, index_for_tag)
        else:
            tags.remove(tag)

    if not tags:
        return

    to_open = set()
    for layer in stack[:index:-1]:
        for lt in layer.tags:
            if lt.closing not in tags:
                to_open.add(lt)
        _layer.close_layer(stack)

    to_close = set()
    layer = stack[index]
    for lt in layer.tags:
        if lt.closing in tags:
            to_close.add(lt)
    _layer.close_tags(stack, to_close, index)

    if to_open:
        _layer.Layer(stack)
        stack[-1].tags = to_open


OPEN = 1
CLOSE = 2
TEXT = 3

BRACKET_L = '\0\1'
BRACKET_R = '\0\2'

START_HOMONYM = 0x1
FIRST_HOMONYM = 0x2
START_CLASS = 0x4
FIRST_CLASS = 0x8
START_TRANSCRIPTION = 0x10
START_TRANSLATION = 0x20
CONTINUE_TRANSLATION = 0x40
APPEND_TRANSLATION = 0x80
START_EXAMPLE = 0x100
APPEND_EXAMPLE = 0x200

# precompiled regexs
re_m_tag_with_content = re.compile(r'(\[m\d\])(.*?)(\[/m\])')
re_non_escaped_bracket = re.compile(r'(?<!\\)\[')
_startswith_tag_cache = {}


class FlawlessDSLParser(object):
    """
    only clean flawless dsl on output!
    """

    def __init__(self, tags=frozenset({
        ('m', '\d'),
        '*',
        'ex',
        'i',
        ('c', '(?: \w+)?'),
        'p',
        "'",
        'b',
        's',
        'sup',
        'sub',
        'ref',
        'url',
    })):
        """
        :type tags: set[str | tuple[str]] | frozenset[str | tuple[str]]
        :param tags: set (or any other iterable) of tags where each tag is a
                     string or two-tuple.  if string, it is tag name without
                     brackets, must be constant, i.e. non-save regex characters
                     will be escaped, e.g.: 'i', 'sub', '*'.
                     if 2-tuple, then first item is tag's base name, and
                     second is its extension for opening tag,
                     e.g.: ('c', r' (\w+)'), ('m', r'\d')
        """
        tags_ = set()
        for tag, ext_re in (t if isinstance(t, tuple) else (t, '') for t in tags):
            tag_re = re.escape(tag)
            tag_open_re = r'\[%s%s\]' % (tag_re, ext_re)
            tags_.add((tag, tag_re, ext_re, tag_open_re))
        self.tags = frozenset(tags_)


    def parse(self, line, article_tree):
        r"""
        parse dsl markup in `line` and return clean valid dsl markup.

        :type line: str
        :param line: line with dsl formatting.

        :rtype: str
        """
        line = self.put_brackets_away(line)
        line = self._parse(line, article_tree)
        return self.bring_brackets_back(line)


    def _parse(self, line, article_tree):
        items = self._split_line_by_tags(line)
        line = self._tags_and_text_loop(items, article_tree)
        return line


    def _split_line_by_tags(self, line):
        """
        split line into chunks, each chunk is whether opening / closing tag or text.

        return iterable of two-tuples. first element is item's type, one of:
        - OPEN, second element is Tag object
        - CLOSE, second element is str with closed tag's name
        - TEXT, second element is str

        :param line: str
        :return: Iterable
        """
        ptr = 0
        while ptr < len(line):
            bracket = line.find('[', ptr)
            if bracket != -1:
                chunk = line[ptr:bracket]
            else:
                chunk = line[ptr:]

            if chunk:
                yield TEXT, chunk

            if bracket == -1:
                break

            ptr = bracket
            bracket = line.find(']', ptr + 2)  # at least two chars after opening bracket
            if line[ptr + 1] == '/':
                yield CLOSE, line[ptr + 2:bracket]
            else:
                for tag, _, _, tag_open_re in self.tags:
                    if re.match(tag_open_re, line[ptr:bracket + 1]):
                        yield OPEN, _tag.Tag(line[ptr + 1:bracket], tag)
                        break
                else:
                    tag = line[ptr + 1:bracket]
                    yield OPEN, _tag.Tag(tag, tag)
            ptr = bracket + 1


    @staticmethod
    def _tags_and_text_loop(tags_and_text, article_tree):
        """
        parse chunks one by one.

        :param tags_and_text: Iterable[['OPEN', Tag] | ['CLOSE', str] | ['TEXT', str]]
        :return: str
        """
        state = TEXT
        stack = []
        closings = set()

        #dsl margin
        margin = 0

        cur_homonym = article_tree

        if 'hom' in article_tree:
            cur_homonym = article_tree['hom'][-1]
            margin += 1
        if 'def' in cur_homonym and \
                        'numB' in cur_homonym['def'][-1]:
            #more than one word class
            margin += 1

        line_state = 0

        for item_t, item in tags_and_text:

            if item_t is OPEN:
                if _tag.was_opened(stack, item) and item.closing not in closings:
                    continue

                if item.closing == 'm' and len(stack) >= 1:
                    # close all layers.  [m*] tags can only appear at top layer.
                    # note: do not reopen tags that were marked as closed already.
                    to_open = set.union(set(),
                                        *((t for t in l.tags if t.closing not in closings)
                                          for l in stack))
                    for i in range(len(stack)):
                        _layer.close_layer(stack)
                    # assert len(stack) == 1
                    # assert not stack[0].tags
                    _layer.Layer(stack)
                    stack[-1].tags = to_open

                elif state is CLOSE:
                    process_closing_tags(stack, closings)

                if not stack or stack[-1].text:
                    _layer.Layer(stack)

                stack[-1].tags.add(item)
                state = OPEN
                continue

            elif item_t is CLOSE:
                if state in (OPEN, TEXT):
                    closings.clear()
                closings.add(item)
                state = CLOSE
                continue

            elif item_t is TEXT:
                if state is CLOSE:
                    process_closing_tags(stack, closings)

                if not stack:
                    _layer.Layer(stack)
                stack[-1].text += item

                # example starts
                if stack[0].tags.issuperset(set([_layer.tag.Tag('*' ,'*'),_layer.tag.Tag('ex' ,'ex')])):
                    line_state |= START_EXAMPLE
                    if len(stack) > 1:
                        line_state |= APPEND_EXAMPLE
                # translation starts
                elif len(stack[0].tags.intersection(set([_layer.tag.Tag('m'+str(margin+1), 'm')]))) or \
                        len(stack[-1].tags.intersection(set([_layer.tag.Tag('m' + str(margin + 1), 'm')]))) or \
                        (not len(stack[-1].tags.difference(set([_layer.tag.Tag('i', 'i')]))) and \
                         len(stack[-1].tags) and \
                         not len(stack[0].tags) and \
                         len(stack[-2].tags.intersection(set([_layer.tag.Tag('m' + str(margin + 1), 'm')])))):
                    line_state |= START_TRANSLATION
                    # special case - [m#] tag is on the same line with transcription
                    if (not len(stack[-1].tags.intersection(set([_layer.tag.Tag('m' + str(margin + 1), 'm')]))) and \
                                    len(stack) > 1):
                        line_state |= APPEND_TRANSLATION
                # text is italic
                #elif not len(stack[-1].tags.difference(set([_layer.tag.Tag('i', 'i')]))) and \
                #        len(stack[-1].tags):
                #    line_state |= APPEND_TRANSLATION
                # text is bold
                elif len(stack[-1].tags.intersection(set([_layer.tag.Tag('b', 'b')]))) == 1:
                    # line starts with bold roman number like 'IV'
                    if len(re.findall(r'^[IV]+', item)):
                        line_state |= START_HOMONYM
                        if item == 'I':
                            line_state |= FIRST_HOMONYM
                            margin += 1
                    # line starts with arabic number like '1.'
                    elif len(re.findall(r'^\d+\.', item)):
                        line_state |= START_CLASS
                        if item == '1.':
                            line_state |= FIRST_CLASS
                            margin += 1
                #assuming first line contains transcription, word category, and sometimes word forms and comments (area)
                elif len(re.findall(r'\\' + BRACKET_L, item)) and \
                        len(re.findall(r'\\' + BRACKET_R, item)):
                    line_state |= START_TRANSCRIPTION

                if line_state & FIRST_HOMONYM:
                    line_state ^= FIRST_HOMONYM
                    article_tree['hom'] = []

                if line_state & START_HOMONYM:
                    line_state ^= START_HOMONYM
                    article_tree['hom'].append({})
                    cur_homonym = article_tree['hom'][-1]
                    cur_homonym['numRB'] = re.sub(r'^([IV]+)', r'\1', item)
                    cur_homonym['def'] = [{}]

                if line_state & FIRST_CLASS:
                    line_state ^= FIRST_CLASS
                    cur_homonym['def'] = []

                if line_state & START_CLASS:
                    line_state ^= START_CLASS
                    #if 'hom' not in article_tree:
                    cur_homonym['def'].append({})
                    cur_homonym['def'][-1]['numB'] = re.sub(r'(\d+)\.', r'\1', item)

                if line_state & START_TRANSLATION and not line_state & CONTINUE_TRANSLATION:
                    line_state ^= START_TRANSLATION
                    line_state |= CONTINUE_TRANSLATION
                    if 'trn' not in cur_homonym['def'][-1]:
                        cur_homonym['def'][-1]['trn'] = list()
                    cur_homonym['def'][-1]['trn'].append({})
                    cur_homonym['def'][-1]['trn'][-1]['tr'] = list()

                if line_state & APPEND_TRANSLATION:
                    item_tagged = item
                    #todo check where translation comments should belong - to num or to text - abandon I 2. 4.
                    #todo check if ♢ idioms can be extracted from samples to their own hierarchy level - abandon I 2. 5.
                    if item.strip() != '':
                        if len(stack[-1].tags.intersection(set([_layer.tag.Tag('p', 'p')]))):
                            item_tagged = '<i data-abbr>' + item + '</i>'
                        elif len(stack[-1].tags.intersection(set([_layer.tag.Tag('i', 'i')]))):
                            item_tagged = '<i>' + item + '</i>'
                    append_leaf = cur_homonym['def'][-1]['trn'][-1]['tr'][-1]
                    if 'syn' in append_leaf:
                        append_leaf['syn'][-1]['text'] += item_tagged
                    else:
                        append_leaf['text'] += item_tagged
                elif line_state & CONTINUE_TRANSLATION:
                    greek = re.findall(r'^(\d+)\. ', item)
                    if len(greek):
                        cur_homonym['def'][-1]['trn'][-1]['num'] = greek[0]
                        item = re.sub(r'^\d+. ', '', item)

                    for variant in re.split(r'; ', item):
                        synonims = re.split(r', ', variant)
                        cur_homonym['def'][-1]['trn'][-1]['tr'].append({})
                        cur_homonym['def'][-1]['trn'][-1]['tr'][-1]['text'] = synonims[0]
                        if len(synonims) > 1:
                            del synonims[0]
                            cur_homonym['def'][-1]['trn'][-1]['tr'][-1]['syn'] = list()
                            for synonim in synonims:
                                cur_homonym['def'][-1]['trn'][-1]['tr'][-1]['syn'].append({})
                                cur_homonym['def'][-1]['trn'][-1]['tr'][-1]['syn'][-1]['text'] = synonim

                if line_state & START_TRANSCRIPTION:
                    line_state ^= START_TRANSCRIPTION
                    if 'def' not in cur_homonym:
                        #if line starts with transcription, not with bold greek number
                        cur_homonym['def'] = [{}]
                    cur_homonym['def'][-1]['ts'] = item.strip(' \\'+BRACKET_L+BRACKET_R)

                if line_state & START_EXAMPLE:
                    if 'ex' not in cur_homonym['def'][-1]['trn'][-1]:
                        cur_homonym['def'][-1]['trn'][-1]['ex'] = list()
                    if not line_state & APPEND_EXAMPLE:
                        cur_homonym['def'][-1]['trn'][-1]['ex'].append({})
                    if len(re.findall(r' - ', item)):
                        text, tr = re.split(r' - ', item)
                        if not line_state & APPEND_EXAMPLE:
                            cur_homonym['def'][-1]['trn'][-1]['ex'][-1]['text'] = text
                            cur_homonym['def'][-1]['trn'][-1]['ex'][-1]['tr'] = tr
                        else:
                            cur_homonym['def'][-1]['trn'][-1]['ex'][-1]['text'] += text
                            cur_homonym['def'][-1]['trn'][-1]['ex'][-1]['tr'] = tr
                    else:
                        item_tagged = item
                        if item.strip() != '':
                            if len(stack[-1].tags.intersection(set([_layer.tag.Tag('p', 'p')]))):
                                item_tagged = '<i data-abbr>' + item + '</i>'
                            elif len(stack[-1].tags.intersection(set([_layer.tag.Tag('i', 'i')]))):
                                item_tagged = '<i>' + item + '</i>'
                        if not len(cur_homonym['def'][-1]['trn'][-1]['ex']):
                            cur_homonym['def'][-1]['trn'][-1]['ex'].append({})
                        if 'text' not in cur_homonym['def'][-1]['trn'][-1]['ex'][-1]:
                            cur_homonym['def'][-1]['trn'][-1]['ex'][-1]['text'] = item_tagged
                        elif 'tr' not in cur_homonym['def'][-1]['trn'][-1]['ex'][-1]:
                            cur_homonym['def'][-1]['trn'][-1]['ex'][-1]['text'] += item_tagged
                        else:
                            cur_homonym['def'][-1]['trn'][-1]['ex'][-1]['tr'] += item_tagged

                elif item.strip() != '':
                    if 'class' not in cur_homonym['def'][-1] \
                            and stack[-1].tags.issuperset(_layer.i_and_c):
                        # word category
                        cur_homonym['def'][-1]['class'] = item
                    elif 'trn' not in cur_homonym['def'][-1] and \
                            'area' not in cur_homonym['def'][-1] and \
                            stack[-1].tags.issuperset(set([_layer.p_tag])):
                        # word area
                        cur_homonym['def'][-1]['area'] = item

                state = TEXT
                continue

        if state is CLOSE and closings:
            process_closing_tags(stack, closings)
        # shutdown unclosed tags
        return ''.join(map(lambda l: l.text, stack))


    def put_brackets_away(self, line):
        """put away \[, \] and brackets that does not belong to any of given tags.

        :rtype: str
        """
        clean_line = ''
        startswith_tag = _startswith_tag_cache.get(self.tags, None)
        if startswith_tag is None:
            openings = '|'.join('%s%s' % (_[1], _[2]) for _ in self.tags)
            closings = '|'.join(_[1] for _ in self.tags)
            startswith_tag = re.compile(r'(?:(?:%s)|/(?:%s))\]' % (openings, closings))
            _startswith_tag_cache[self.tags] = startswith_tag
        for i, chunk in enumerate(re_non_escaped_bracket.split(line)):
            if i != 0:
                m = startswith_tag.match(chunk)
                if m:
                    clean_line += '[%s%s' % (m.group(), chunk[m.end():].replace('[', BRACKET_L).replace(']', BRACKET_R))
                else:
                    clean_line += BRACKET_L + chunk.replace('[', BRACKET_L).replace(']', BRACKET_R)
            else:  # firsr chunk
                clean_line += chunk.replace('[', BRACKET_L).replace(']', BRACKET_R)
        return clean_line


    @staticmethod
    def bring_brackets_back(line):
        return line.replace(BRACKET_L, '[').replace(BRACKET_R, ']')


def parse(line, tags=None):
    """parse DSL markup.

    WARNING!
    `parse` function is not optimal because it creates new parser instance on each call.
    consider cache one [per thread] instance of FlawlessDSLParser in your code.
    """
    import warnings
    warnings.warn("""`parse` function is not optimal because it creates new parser instance on each call.
consider cache one [per thread] instance of FlawlessDSLParser in your code.\
""")
    if tags:
        parser = FlawlessDSLParser(tags)
    else:
        parser = FlawlessDSLParser()
    return parser.parse(line)
