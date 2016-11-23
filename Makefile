VARIANTS := Regular Italic Bold BoldItalic HandTooled
TABLES   := name GSUB

DST_TTX  := $(patsubst %,%.ttx,$(VARIANTS))
SRC_TTX  := $(patsubst %,%.src.ttx,$(VARIANTS))
TTF      := $(patsubst %,font/MijuGoudy-%.ttf,$(VARIANTS))
EOT      := $(patsubst %,font/MijuGoudy-%.eot,$(VARIANTS))
SVG      := $(patsubst %,font/MijuGoudy-%.svg,$(VARIANTS))
WOFF     := $(patsubst %,font/MijuGoudy-%.woff,$(VARIANTS))
WOFF2    := $(patsubst %,font/MijuGoudy-%.woff2,$(VARIANTS))

all: ttf eot svg woff woff2

ttf: $(TTF)
eot: $(EOT)
svg: $(SVG)
woff: $(WOFF)
woff2: $(WOFF2)
.PHONY: ttf eot svg woff woff2

src-ttx: $(SRC_TTX)
dst-ttx: $(DST_TTX)
.PHONY: src-ttx dst-ttx

%.src.ttx: sukhumala/Sukhumala-%.otf Makefile
	ttx -q -f $(patsubst %,-t %,$(TABLES)) -o $@ $<

%.ttx: %.src.ttx modifyttx.py
	python3 modifyttx.py $< $@

font/MijuGoudy-%.ttf: sukhumala/Sukhumala-%.otf %.ttx
	ttx -q -f -o $@ -m $^

%.eot %.svg %.woff: %.ttf
	@webify --zopfli --svg-enable-kerning $<

%.woff2: %.ttf
	@woff2_compress $<
