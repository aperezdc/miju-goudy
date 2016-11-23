Miju Goudy
==========

A version of Goudy Oldstyle with the four basic variants (regular, bold,
italic, bold-italic), plus a decorative one (“hand tooled”). Miju Goudy takes
the [Sukhumala](http://www.softerviews.org/Fonts.html#Sukhumala) type face by
Bhikkhu Pesala, and removes the non-standard contextual ligatures which it has
added to allow direct usage of [Velthuis
transliteration](https://en.wikipedia.org/wiki/Velthuis).

Sukhumala itself is based upon [Barry Schwartz](http://www.crudfactory.com/)'s
[Sorts Mill Goudy](https://www.theleagueofmoveabletype.com/sorts-mill-goudy)
([source](https://github.com/theleagueof/sorts-mill-goudy)


Licensing
---------

TL;DR: Distributed under the terms of the [MIT/X11
license](http://www.opensource.org/licenses/mit-license.php).

Version 1.1 of Sorts Mill Goudy in GitHub (the repository contains a single
commit from 2011) claims to be released under the terms of the [SIL Open Font
License](http://scripts.sil.org/OFL), but Sukhumala has an embedded notice
(from 2009) in the `.otf` files claiming that it is distributed under the
terms of the MIT/X11. Assuming that Barry Schwartz changed the license at some
point between 2009 and 2011, *and* that Bhikkhu Pesala started working on
Sukhumala before the license was changed, *and* considering that Miju
Goudy derives from Sukhumala, the license has to be MIT/X11.

At any rate [IANAL](https://en.wikipedia.org/wiki/IANAL), so if you have
a good understanding of the legalese, please contact me to correct this.


Building
--------

The following tools are needed to regenerate the files under `font/`:

- [fonttools](https://github.com/behdad/fonttools)
  ([AUR](https://aur.archlinux.org/packages/python-fonttools-git/)).
- [webify](https://github.com/ananthakumaran/webify)
  ([AUR](https://aur.archlinux.org/packages/webify/)).
- `woff2_compress` from [woff2](https://github.com/google/woff2)
  ([AUR](https://aur.archlinux.org/packages/woff2-git/)).

Once they are installed in your system, just run `make`.

