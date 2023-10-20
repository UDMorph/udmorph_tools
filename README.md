# udmorph_tools

This repository provides helpful tools to work with UDMorph data-sets.

## unimorph2ud.py

The script unimorph2ud.py is a python script that can convert a [UniMorph](https://unimorph.github.io/) lexicon into a UD style lexicon, that UDMorph can 
use. The script is uses an inverted an adapted table from the [ud_compatibility](https://github.com/unimorph/ud-compatibility) script that converts UD into unimorph. The script only convert know tags and features, and warns about unknown ones. The script is still missing some features that could be translated, which should be added in the future. The output format uses the style of CoNLL-U with only the relevant columns: `FORM, LEMMA, UPOS, XPOS, FEATS`, where the `FEATS` column contains the original UniMorph tag. 

The output format is intended to be usable to improve the accuracy of taggers, and can be used in TEITOK to provide a selection list of options. For use in TEITOK, the lexicon should names Resources/XXX.udlex (with XXX being the language code), or specified by name in the settings.

## applylex.py

The script applylex.py is a python script that can take a udlex file (for instance created by unimorph2ud.py) and apply it to a CoNLL-U file. By default, it will take the first item from the lexicon (which should hence ideally be order by frequency of the words, at least within alternatives for the same word) and load the data for that reading into the relevant column, and adds a feature lexCnt to the `MISC` column if there is more than one reading. Instead of a lexCnt, it can also add all other readings in compressed for as an attribute altMorph. And it can be asked to unpack all the reading, and put alternatives in each field with a / sign.