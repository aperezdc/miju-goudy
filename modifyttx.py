#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Adrian Perez <aperez@igalia.com>
#
# Distributed under terms of the MIT license.

from xml.etree import ElementTree
import sys
import re

# Font name replacements. These are applied to elements in the "name" table.
SRC_NAME   = "Sukhumala"
DST_NAME   = "Miju Goudy"
SRC_PSNAME = SRC_NAME.replace(" ", "")
DST_PSNAME = DST_NAME.replace(" ", "")

# Additions to authors and copyright notice. Also in the "name" table.
AUTHOR_ADD = "Adrián Pérez de Castro"

# Ligatures to remove.
class Rule(object):
    def __init__(self, start, dest=".*", components=".*"):
        self._start_re = re.compile("^" + start + "$")
        self._dest_re = re.compile("^" + dest + "$")
        self._comp_re = re.compile("^" + components + "$")

    def matches(self, node):
        if node.tag != "LigatureSet":
            return ()
        start_glyph = node.get("glyph", None)
        if start_glyph is None:
            return ()
        if not self._start_re.match(start_glyph):
            return ()
        for child in node:
            components = child.get("components", None)
            substglyph = child.get("glyph", None)
            if components is None: continue
            if substglyph is None: continue 
            if self._comp_re.match(components) and self._dest_re.match(substglyph):
                yield child


LIGATURE_RULES = (Rule(r"[AEIOUaeiou]", r"[AEIOUaeiou]macron"),
                  Rule(r"asciitilde", r"[Nn]tilde", r"[Nn]"),
                  Rule(r"period", components=r"[A-Za-z](?:,[A-Za-z])?"),
                  Rule(r"quotedbl", components=r"[A-Za-z]"))

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

    def _do_visit_nodes(self, prefix, parent, silent=()):
        for node in parent:
            visitor_name = prefix + node.tag
            f = getattr(self, visitor_name, None)
            if callable(f):
                f(node, parent)
            elif node.tag not in silent:
                print("Missing:", visitor_name, "node:", node, file=sys.stderr)

    def wrangle(self):
        root = self._etree.getroot()
        for node in root.findall("./name/namerecord"):
            self.visit_namerecord(node)
        for node in root.findall("./GSUB/LookupList/Lookup/LigatureSubst/LigatureSet"):
            self.visit_ligature_set(node)

    def visit_namerecord(self, node):
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

    def visit_ligature_set(self, node):
        for rule in LIGATURE_RULES:
            for child in rule.matches(node):
                node.remove(child)


if __name__ == "__main__":
    et = ElementTree.parse(sys.argv[1])
    FontWrangler(et).wrangle()
    et.write(sys.argv[2],
             encoding="utf-8",
             xml_declaration=True)
