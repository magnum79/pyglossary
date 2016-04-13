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

COMMA = '\0\3'
SEMICOLON = '\0\4'

START_HOMONYM       = 0x1
START_CLASS         = 0x2
START_TRANSCRIPTION = 0x4
START_TRANSLATION   = 0x8
CONTINUE_TRANSLATION= 0x10
APPEND_TRANSLATION  = 0x20
START_EXAMPLE       = 0x40
APPEND_EXAMPLE      = 0x80
APPEND_COMMENT      = 0x100

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
        'com',
        ('lang', '( .+?)'),
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


    def parse(self, line, article_tree, **options):
        r"""
        parse dsl markup in `line` and return clean valid dsl markup.

        :type line: str
        :param line: line with dsl formatting.

        :rtype: str
        """
        line = self.put_brackets_away(line)
        line = self._parse(line, article_tree, **options)
        return self.bring_brackets_back(line)


    def _parse(self, line, article_tree, **options):
        items = self._split_line_by_tags(line)
        line = self._tags_and_text_loop(items, article_tree, **options)
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
    def _tags_and_text_loop(tags_and_text, article_tree, **options):
        """
        parse chunks one by one.

        :param tags_and_text: Iterable[['OPEN', Tag] | ['CLOSE', str] | ['TEXT', str]]
        :return: str
        """

        def wrap_tags(stack, item):
            #todo check for child tags wrapping, maybe use original algorithm (to_close set)
            item_tagged = item
            if item.strip() != '':
                if len(stack[-1].tags.intersection({_layer.tag.Tag('p', 'p')})):
                    item_tagged = '<i data-abbr>' + item + '</i>'
                elif len(stack[-1].tags.intersection({_layer.tag.Tag('i', 'i')})):
                    item_tagged = '<i>' + item + '</i>'
                elif len(stack[-1].tags.intersection({_layer.tag.Tag('b', 'b')})):
                    item_tagged = '<b>' + item + '</b>'
                elif len(stack[-1].tags.intersection({_layer.tag.Tag('sup', 'sup')})):
                    item_tagged = '<sup>' + item + '</sup>'
            return item_tagged

        def append_comment(line_state, cur_def, stack, item):
            if not line_state & APPEND_COMMENT or \
                    not 'com' in cur_def:
                line_state |= APPEND_COMMENT
                cur_def['com'] = wrap_tags(stack, item)
            else:
                cur_def['com'] += wrap_tags(stack, item)
            return line_state

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

        dictType = 'default'
        if 'dictType' in options:
            dictType = options['dictType']

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
                if stack[0].tags.issuperset({_layer.tag.Tag('*' ,'*'),_layer.tag.Tag('ex' ,'ex')}):
                    line_state |= START_EXAMPLE
                    if len(stack) > 1:
                        line_state |= APPEND_EXAMPLE
                # translation starts
                elif len(stack[0].tags.intersection({_layer.tag.Tag('m'+str(margin+1), 'm')})) or \
                        len(stack[-1].tags.intersection({_layer.tag.Tag('m' + str(margin + 1), 'm')})) or \
                        (len(stack[-1].tags.intersection({_layer.tag.Tag('i', 'i')})) and
                         not len(stack[0].tags) and
                         len(stack[-2].tags.intersection({_layer.tag.Tag('m' + str(margin + 1), 'm')}))):
                    line_state |= START_TRANSLATION
                    if (not len(stack[-1].tags.intersection({_layer.tag.Tag('m' + str(margin + 1), 'm')})) and \
                                    len(stack) > 1) or \
                                    stack[-1].text != item:
                        line_state |= APPEND_TRANSLATION
                # text is bold
                elif len(stack[-1].tags.intersection({_layer.tag.Tag('b', 'b')})) == 1:
                    # line starts with bold roman number like 'IV'
                    if len(re.findall(r'^[IV]+', item)):
                        line_state |= START_HOMONYM
                        if item == 'I':
                            margin += 1
                    # line starts with arabic number like '1.'
                    elif len(re.findall(r'^\d+\.', item)):
                        line_state |= START_CLASS
                        if item == '1.':
                            margin += 1
                #assuming first line contains transcription, word category, and sometimes word forms and comments (area)
                #but check if it's not contains closing sqare bracket ] and it's acutal word category and area, not translation - a I
                elif len(re.findall(r'\\' + BRACKET_L, item)) and \
                        len(re.findall(r'\\' + BRACKET_R, item)):
                    line_state |= START_TRANSCRIPTION

                if line_state & START_HOMONYM:
                    line_state ^= START_HOMONYM
                    if 'hom' not in article_tree:
                        article_tree['hom'] = []
                    article_tree['hom'].append({})
                    cur_homonym = article_tree['hom'][-1]
                    cur_homonym['numRB'] = re.sub(r'^([IV]+)', r'\1', item)

                if line_state & START_CLASS:
                    line_state ^= START_CLASS
                    if 'def' not in cur_homonym:
                        cur_homonym['def'] = []
                    cur_homonym['def'].append({})
                    cur_homonym['def'][-1]['numB'] = int(re.sub(r'(\d+)\.', r'\1', item))

                if line_state & START_TRANSLATION and not line_state & CONTINUE_TRANSLATION:
                    line_state ^= START_TRANSLATION
                    line_state |= CONTINUE_TRANSLATION

                    #translation on the first line
                    if 'def' not in cur_homonym:
                        cur_homonym['def'] = []
                        cur_homonym['def'].append({})
                    #homonym inside definition
                    if len(re.findall(r'^[IV]+', item)):
                        line_state ^= CONTINUE_TRANSLATION
                        if 'hom' not in cur_homonym['def'][-1]:
                            cur_homonym['def'][-1]['hom'] = list()
                        cur_homonym['def'][-1]['hom'].append({})
                        re_numR_parts = re.compile(r'(^[IV]+)(\s?)([А-Я]*)(\s?)')
                        numR_match = re.match(re_numR_parts, item)
                        numR_parts = re.findall(re_numR_parts, item)[0]
                        cur_homonym['def'][-1]['hom'][-1]['numR'] = numR_parts[0]
                        if numR_parts[2] != '':
                            cur_homonym['def'][-1]['hom'][-1]['numR'] += numR_parts[1]+numR_parts[2]
                        if numR_match.endpos > numR_match.regs[-1][1]:
                            item = item[numR_match.regs[-1][1]:]
                            line_state |= APPEND_COMMENT
                    #comment after roman numeration
                    if len(re.findall(r'^[IV]+', stack[0].text)) and \
                            (len(stack) > 1 or
                                     stack[-1].text != item):
                        if line_state & CONTINUE_TRANSLATION:
                            line_state ^= CONTINUE_TRANSLATION
                        if line_state & APPEND_TRANSLATION:
                            line_state ^= APPEND_TRANSLATION
                        line_state |= APPEND_COMMENT

                    if line_state & CONTINUE_TRANSLATION:
                        cur_def = cur_homonym['def'][-1]
                        # phrasal verbs dictionary
                        if dictType == 'idioms-and-phrasal-verbs':
                            if len(stack[-1].tags.intersection({_layer.tag.Tag('b', 'b')})):
                                # remove variants from first line
                                line_state ^= CONTINUE_TRANSLATION
                                options['keyAlters'].append([])
                                options['keyAlters'][-1].append(article_tree['text'])
                                options['keyAlters'][-1].append(item)
                                article_tree['text'] = item
                            if not 'def' in cur_homonym or \
                                    not 'trn' in cur_def or \
                                    not len(cur_def['trn'][-1]['tr']):
                                # when double article title was removed
                                if line_state & APPEND_TRANSLATION:
                                    line_state ^= APPEND_TRANSLATION
                                    if item.strip() == '':
                                        if line_state & CONTINUE_TRANSLATION:
                                            line_state ^= CONTINUE_TRANSLATION
                                # area comment on the first line
                                if stack[-1].tags.issuperset(
                                        {_layer.tag.Tag('i', 'i'), _layer.tag.Tag('com', 'com')}):
                                    if line_state & CONTINUE_TRANSLATION:
                                        line_state ^= CONTINUE_TRANSLATION

                    if line_state & CONTINUE_TRANSLATION:
                        if 'hom' in cur_def:
                            cur_def = cur_def['hom'][-1]
                        if 'trn' not in cur_def:
                            cur_def['trn'] = list()
                        cur_def['trn'].append({})
                        cur_def['trn'][-1]['tr'] = list()

                if line_state & APPEND_TRANSLATION or \
                                line_state & CONTINUE_TRANSLATION or \
                                line_state & START_EXAMPLE:
                    cur_def = cur_homonym['def'][-1]
                    if 'hom' in cur_def:
                        cur_def = cur_def['hom'][-1]
                    if 'trn' not in cur_def:
                        cur_def['trn'] = list()
                        cur_def['trn'].append({})
                    cur_trn = cur_def['trn']

                if line_state & APPEND_TRANSLATION:
                    #todo check where translation comments should belong - to num or to text - abandon I 2. 4.
                    #todo check if ♢ idioms can be extracted from samples to their own hierarchy level - abandon I 2. 5.
                    append_leaf = cur_trn[-1]['tr'][-1]
                    if 'syn' in append_leaf:
                        append_leaf['syn'][-1]['text'] += wrap_tags(stack, item)
                    else:
                        append_leaf['text'] += wrap_tags(stack, item)

                elif line_state & CONTINUE_TRANSLATION:
                    greek_dot = re.findall(r'^(\d+)\. ', item)
                    if len(greek_dot):
                        cur_trn[-1]['num'] = int(greek_dot[0])
                        item = re.sub(r'^\d+. ', '', item)

                    greek_bracket = re.findall(r'^(\d+)\) ', item)
                    if len(greek_bracket):
                        if len(greek_dot):
                            cur_trn[-1]['num'] = int(greek_dot[0])
                        elif len(cur_trn) > 1 and \
                                'num' in cur_trn[-2]:
                            cur_trn[-1]['num'] = cur_trn[-2]['num']
                        cur_trn[-1]['sense'] = int(greek_bracket[0])
                        item = re.sub(r'^\d+\) ', '', item)
                    #todo also do splitting in APPEND_TRANSLATION - be II Б 2. 2), but not in comments - be II Б 15. 2), and not in double language defs - be II Б 5. and be II Б 6.
                    #todo do not split comma in special cases (i.e. long sentence) - a 5. 1), a 6.
                    #todo split translation and synonyms after comment - a I 8., a I 11. 2), a I 12.
                    #do not split comment block
                    if stack[-1].tags.issuperset({_layer.tag.Tag('i', 'i'),_layer.tag.Tag('com', 'com')}):
                        if not len(cur_trn[-1]['tr']):
                            cur_trn[-1]['tr'].append({})
                        cur_trn[-1]['tr'][-1]['text'] = wrap_tags(stack, item)
                    else:
                        #replace comma and semicolon inside brackets
                        item = re.sub(r'(\([^)]*?)([,])(.*?\))', r'\1'+COMMA+r'\3',
                               re.sub(r'(\([^)]*?)([;])(.*?\))', r'\1'+SEMICOLON+r'\3', item))
                        for variant in re.split(r'; ', item):
                            synonims = re.split(r', ', variant)
                            cur_trn[-1]['tr'].append({})
                            cur_trn[-1]['tr'][-1]['text'] = wrap_tags(stack, synonims[0].replace(COMMA, ',').replace(SEMICOLON, ';'))
                            if len(synonims) > 1:
                                del synonims[0]
                                cur_trn[-1]['tr'][-1]['syn'] = list()
                                for synonim in synonims:
                                    cur_trn[-1]['tr'][-1]['syn'].append({})
                                    cur_trn[-1]['tr'][-1]['syn'][-1]['text'] = wrap_tags(stack, synonim.replace(COMMA, ',').replace(SEMICOLON, ';'))

                elif line_state & START_TRANSCRIPTION:
                    line_state ^= START_TRANSCRIPTION
                    if 'def' not in cur_homonym:
                        #if line starts with transcription, not with bold greek number
                        cur_homonym['def'] = [{}]
                    cur_homonym['def'][-1]['ts'] = item.strip(' \\'+BRACKET_L+BRACKET_R)

                elif line_state & START_EXAMPLE:
                    if 'ex' not in cur_trn[-1]:
                        cur_trn[-1]['ex'] = list()
                    #todo analyse cyrillic numeration а) б) in example sense translations - be II Б 2. 1)
                    if len(cur_trn[-1]['ex']) and \
                        'tr' not in cur_trn[-1]['ex'][-1] and \
                        dictType != 'idioms-and-phrasal-verbs':
                        line_state |= APPEND_EXAMPLE
                    if not line_state & APPEND_EXAMPLE:
                        cur_trn[-1]['ex'].append({})
                    if len(re.findall(r' - ', item)) and \
                            stack[-1].text != item:
                        text, tr = item.split(r' - ', 1)
                        if not line_state & APPEND_EXAMPLE:
                            cur_trn[-1]['ex'][-1]['text'] = text
                            cur_trn[-1]['ex'][-1]['tr'] = tr
                        else:
                            cur_trn[-1]['ex'][-1]['text'] += text
                            cur_trn[-1]['ex'][-1]['tr'] = tr
                    else:
                        if not len(cur_trn[-1]['ex']):
                            cur_trn[-1]['ex'].append({})
                        if 'text' not in cur_trn[-1]['ex'][-1]:
                            cur_trn[-1]['ex'][-1]['text'] = wrap_tags(stack, item)
                        elif 'tr' not in cur_trn[-1]['ex'][-1]:
                            cur_trn[-1]['ex'][-1]['text'] += wrap_tags(stack, item)
                        else:
                            cur_trn[-1]['ex'][-1]['tr'] += wrap_tags(stack, item)

                #comment on first line, without transcription
                elif 'def' not in cur_homonym and \
                        stack[-1].tags.issuperset({_layer.tag.Tag('i', 'i'),_layer.tag.Tag('com', 'com')}):
                    cur_homonym['def'] = [{}]
                    line_state = append_comment(line_state, cur_homonym['def'][-1], stack, item)
                #todo parse irregular verb forms
                #todo any other comments after transcription before trn
                #todo check actual class, not just comment when translation moved to top - 'd word
                #todo do not extract area if it's within brackets - a word
                #todo do not extract transcription if it's within brackets, and first transcription already extracted - a word
                elif 'def' in cur_homonym:
                    cur_def = cur_homonym['def'][-1]
                    if 'hom' in cur_def:
                        cur_def = cur_def['hom'][-1]
                    if 'trn' not in cur_def:
                        if line_state & APPEND_COMMENT:
                            line_state = append_comment(line_state, cur_def, stack, item)
                        elif 'class' not in cur_def and \
                                'com' not in cur_def and \
                                stack[-1].tags.issuperset({_layer.p_tag}) and \
                                item.strip() != '' and \
                                dictType != 'idioms-and-phrasal-verbs':
                            # word category
                            cur_def['class'] = item
                        elif 'area' not in cur_def and \
                                'com' not in cur_def and \
                                stack[-1].tags.issuperset({_layer.p_tag}) and \
                                item.strip() != '':
                            # word area
                            cur_def['area'] = item
                        #todo treat second [p] as comment start (currently ignored) - a II
                        elif 'com' not in cur_def and \
                                len(stack[-1].tags.intersection({_layer.tag.Tag('i', 'i')})) and \
                                item.strip() != '':
                            #comment or maybe link
                            #todo analyze equal character =
                            line_state = append_comment(line_state, cur_def, stack, item)

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
