#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Adrian Perez <aperez@igalia.com>
#
# Distributed under terms of the MIT license.

from xml.etree import ElementTree
import sys

# Font name replacements. These are applied to elements in the "name" table.
SRC_NAME   = "Sukhumala"
DST_NAME   = "Miju Goudy"
SRC_PSNAME = SRC_NAME.replace(" ", "")
DST_PSNAME = DST_NAME.replace(" ", "")

# Additions to authors and copyright notice. Also in the "name" table.
AUTHOR_ADD = "Adrián Pérez de Castro"

# https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html
NAME_ID_COPYRIGHT         =  0
NAME_ID_FONT_FAMILY       =  1
NAME_ID_FONT_SUBFAMILY    =  2
NAME_ID_UNIQUE_SUBFAMILY  =  3
NAME_ID_FONT_FULL_NAME    =  4
NAME_ID_TABLE_VERSION     =  5
NAME_ID_POSTSCRIPT_NAME   =  6
NAME_ID_MANUFACTURER_NAME =  8
NAME_ID_COMPATIBLE_FULL   = 18


class FontWrangler(object):
    def __init__(self, et):
        self._etree = et

    def _do_visit_nodes(self, prefix, iterable):
        for node in iterable:
            visitor_name = prefix + node.tag
            f = getattr(self, visitor_name, None)
            if callable(f):
                f(node)
            else:
                print("Missing:", visitor_name, "node:", node, file=sys.stderr)

    def wrangle(self):
        self._do_visit_nodes("visit_", self._etree.getroot())

    def visit_name(self, node):
        self._do_visit_nodes("visit_name_", node)

    def visit_name_namerecord(self, node):
        nameID = int(node.get("nameID"))
        if nameID in (NAME_ID_FONT_FAMILY,
                      NAME_ID_FONT_SUBFAMILY,
                      NAME_ID_UNIQUE_SUBFAMILY,
                      NAME_ID_FONT_FULL_NAME,
                      NAME_ID_COMPATIBLE_FULL):
            node.text = node.text.replace(SRC_NAME, DST_NAME)
        elif nameID == NAME_ID_POSTSCRIPT_NAME:
            node.text = node.text.replace(SRC_PSNAME, DST_PSNAME)
        elif nameID == NAME_ID_COPYRIGHT:
            node.text += "Copyright (c) 2016 " + AUTHOR_ADD
        elif nameID == NAME_ID_MANUFACTURER_NAME:
            node.text = AUTHOR_ADD


if __name__ == "__main__":
    et = ElementTree.parse(sys.argv[1])
    FontWrangler(et).wrangle()
    et.write(sys.argv[2],
             encoding="utf-8",
             xml_declaration=True)
