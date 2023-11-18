import sys, os, argparse
import udm_functions as udm

argParser = argparse.ArgumentParser(description='Meta-script to run taggers in CoNLL-U')
argParser.add_argument('--tagger', help='tagger to run', required=True)
argParser.add_argument('--debug', '-d', help='debug mode', action='store_true')
argParser.add_argument('--download', help='download model', action='store_true')
argParser.add_argument('--file', '-f', help='filename of the file to tag')
argParser.add_argument('--input', help='input format')
argParser.add_argument('--text', help='text input')
argParser.add_argument('--model', '-m', help='model file', required=True)
argParser.add_argument('--upos', '-u', help='XPOS to UD translation table', required=False)
args, moreargs = argParser.parse_known_args()

if args.file:
    infile = args.file
    fh = open(infile, "r")
    txt = "".join(fh.readlines())
    fh.close()
elif args.text:
    txt = args.text
else:
    txt = "".join(moreargs)

if not txt:
    print("No text provided ")
    exit()
  
modulename = 'udm_' + args.tagger     
tagger = __import__(modulename)       
  
sents = False

if args.input:
    if hasattr(tagger, "inputs") and args.input in tagger.inputs:
        print("Using native parsing for " + args.input)
        tagger.input = args.input
    else:
        if args.input == "conllu":
            sents = udm.load_conllu(txt)
            txt = ""
            for sent in sents:
                for token in sent['tokens']:
                    txt = txt + token['form'] + " "
                txt = txt + "\n"
  
tagged = tagger.runtagger(args.model, txt)    
    
if hasattr(tagger, "desc"):
    taggerdesc = tagger.desc
else:
     taggerdesc = args.tagger  

if hasattr(tagger, "modeldesc"):
    modeldesc = tagger.modeldesc
else:
    modeldesc = os.path.basename(args.model)

print("# generator = UDMorph")
print("# tagger = " + taggerdesc)
print("# model = " + modeldesc)

if hasattr(tagger, "output") and tagger.output == "conllu":
    print (tagger.raw)
else:
	if sents:
		tmp = tagged
		tagged = udm.maptoks(sents, tmp)

	udm.print_conllu(tagged)



