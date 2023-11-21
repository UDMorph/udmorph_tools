# udmorph_tools

This repository provides helpful tools and resources to work with UDMorph data-sets.

## udm_tagger.py

The script udm_tagger.py is a central hub to provide a uniform input/output workflow across several taggers. It is the workflow used by many of the tagger in the UDMorph GUI. The metatagger takes an argument `--tagger`, which will run a subprocess with the actual tagger - such as udm_udpipe1.py for UDPIPE1, and udm_stanza.py for Stanza. The primary input types are plain text and CoNLL-U, and the main output is in CoNLL-U. 

## unimorph2ud.py

The script unimorph2ud.py is a python script that can convert a [UniMorph](https://unimorph.github.io/) lexicon into a UD style lexicon, that UDMorph can 
use. The script is using an inverted and adapted version of the table of the [ud_compatibility](https://github.com/unimorph/ud-compatibility) script that converts UD into unimorph. The script only converts known tags and features, and warns about unknown ones. The script is still missing some features that could be translated, which should be added in the future. The output format uses the style of CoNLL-U with only the relevant columns: `FORM, LEMMA, UPOS, XPOS, FEATS`, where the `FEATS` column contains the original UniMorph tag. 

## applylex.py

The script applylex.py is a python script that can take a udlex file (for instance created by unimorph2ud.py) and apply it to a CoNLL-U file. By default, it will take the first item from the lexicon (which should hence ideally be order by frequency of the words, at least within alternatives for the same word) and load the data for that reading into the relevant column, and adds a feature lexCnt to the `MISC` column if there is more than one reading. Instead of a lexCnt, it can also add all other readings in compressed for as an attribute altMorph. And it can be asked to unpack all the reading, and put alternatives in each field with a / sign.
