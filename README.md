# udmorph_tools

This repository provides helpful tools to work with UDMorph data-sets.

## unimorph2ud.py

The unimorph2ud.py is a python script that can convert a [UniMorph](https://unimorph.github.io/) lexicon into a UD style lexicon, that UDMorph can 
use. The script is uses an inverted an adapted table from the [ud_compatibility](https://github.com/unimorph/ud-compatibility) script that converts UD into unimorph. The script only convert know tags and features, and warns about unknown ones. The script is still missing some features that could be translated, which should be added in the future. The output format uses the style of CoNLL-U with only the relevant columns: `FORM, LEMMA, UPOS, XPOS, FEATS`. 