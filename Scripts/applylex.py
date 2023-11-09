import csv
import argparse
import os, sys
import warnings

dir = os.path.dirname(sys.argv[0])

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", help="verbose mode", action='store_true')
argParser.add_argument("-a", "--addalt", help="add altMorph", action='store_true')
argParser.add_argument("-p", "--parsealt", help="add alternatives at feature level", action='store_true')
argParser.add_argument("--debug", help="debugging mode", action='store_true')
argParser.add_argument("-f", "--file", help="conllu file to enrich")
argParser.add_argument("-l", "--lex", help="lexicon file to apply")
args, moreargs = argParser.parse_known_args()

if args.lex:
	lexfile = args.lex
else:
	print("No lexicon provided")
	quit()

if args.file:
	conllu = args.file
else:
	conllu = sys.argv[1]

lexicon = {}
with open(lexfile) as lex:
	tsvreader = csv.reader(lex, delimiter="\t")
	for row in tsvreader:
		if not row[0] in lexicon.keys():
			lexicon[row[0]] = []
		lexicon[row[0]].append(row)
		
lastopt = 1
if args.parsealt:
	lastopt = 100		
		
with open(conllu) as file:
	tsvreader = csv.reader(file, delimiter="\t")
	for row in tsvreader:
		if len(row) > 1:
			word = row[1]
			if not word in lexicon.keys():
				word = word.lower()
			if word in lexicon.keys():
				opts = lexicon[word]
				lemmas = {}
				uposs = {}
				xposs = {}
				featss = {}
				for opt in lexicon[word][0:lastopt]:
					lemmas[opt[1]] = 1
					uposs[opt[2]] = 1
					xposs[opt[3]] = 1
					featss[opt[4]] = 1
				row[2] = '/'.join(lemmas.keys())
				row[3] = '/'.join(uposs.keys())
				row[4] = '/'.join(xposs.keys())
				row[5] = '/'.join(featss.keys())
				if len(opts) > 1:
					if args.addalt:
						alts = 'altMorph=' + '#'.join('\\t'.join(opt) for opt in opts[1:])
					else:
						alts = 'lexCnt=' + str(len(opts))
					if row[9] != '_':
						alts = row[9] + "|" + alts
					row[9] = alts
		print ("\t".join(row))
