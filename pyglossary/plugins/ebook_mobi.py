# -*- coding: utf-8 -*-
# The MIT License (MIT)

# Copyright (C) 2012-2016 Alberto Pettarin (alberto@albertopettarin.it)
# Copyright (C) 2016 Saeed Rasooli <saeed.gnu@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from formats_common import *
from pyglossary.ebook_base import *

enable = True
format = 'Mobi'
description = 'MOBI E-Book'
extentions = ['.mobi',]
readOptions = []
writeOptions = [
]


class MobiWriter(EbookWriter):
    ebook_format = u"mobi"

    CSS_CONTENTS = u""""@charset "UTF-8";"""
    GROUP_XHTML_TEMPLATE = u"""<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 <head>
  <title>{title}</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
 </head>
 <body id="groupPage" class="groupPage">
  <h1 class="groupTitle">{group_title}</h1>
  <div class="groupNavigation">
   <a href="{previous_link}">[ Previous ]</a>
{index_link}
   <a href="{next_link}">[ Next ]</a>
  </div>
{group_contents}
 </body>
</html>"""

    GROUP_XHTML_INDEX_LINK = u"""   <a href="index.xhtml">[ Index ]</a>"""

    GROUP_XHTML_WORD_TEMPLATE = u"""   <span class="groupHeadword"><idx:entry><idx:orth>{headword}</idx:orth></idx:entry></span>"""

    GROUP_XHTML_WORD_JOINER = u" &#8226;\n"

    GROUP_XHTML_WORD_DEFINITION_TEMPLATE = u"""  <div class="groupEntry">
   <idx:entry>
    <h2 class="groupHeadword"><idx:orth>{headword}</idx:orth></h2>
    <p class="groupDefinition">{definition}</p>
   </idx:entry>
  </div>"""


    OPF_TEMPLATE = u"""<?xml version="1.0" encoding="utf-8"?>
<package unique-identifier="uid">
 <metadata>
  <dc-metadata xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openebook.org/namespaces/oeb-package/1.0/">
   <dc:Title>{title}</dc:Title>
   <dc:Language>{sourceLang}</dc:Language>
   <dc:Identifier id="uid">{identifier}</dc:Identifier>
   <dc:Creator>{creator}</dc:Creator>
   <dc:Rights>{copyright}</dc:Rights>
   <dc:Subject BASICCode="REF008000">Dictionaries</dc:Subject>
  </dc-metadata>
  <x-metadata>
   <output encoding="utf-8"></output>
   <DictionaryInLanguage>{sourceLang}</DictionaryInLanguage>
   <DictionaryOutLanguage>{targetLang}</DictionaryOutLanguage>
   <EmbeddedCover>{cover}</EmbeddedCover>
  </x-metadata>
 </metadata>
 <manifest>
{manifest}
 </manifest>
 <spine>
{spine}
 </spine>
 <tours></tours>
 <guide></guide>
</package>"""





