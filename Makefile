VARIANTS := Regular Italic Bold BoldItalic
TABLES   := name GSUB

DST_TTX  := $(patsubst %,%.ttx,$(VARIANTS))
SRC_TTX  := $(patsubst %,%.src.ttx,$(VARIANTS))
TTF      := $(patsubst %,MijuGoudy-%.ttf,$(VARIANTS))

all: $(TTF)

src-ttx: $(SRC_TTX)
dst-ttx: $(DST_TTX)
.PHONY: src-ttx dst-ttx

%.src.ttx: sukhumala/Sukhumala-%.otf
	ttx -q -f $(patsubst %,-t %,$(TABLES)) -o $@ $<

%.ttx: %.src.ttx modifyttx.py
	python3 modifyttx.py $< $@

MijuGoudy-%.ttf: sukhumala/Sukhumala-%.otf %.ttx
	ttx -q -f -o $@ -m $^
