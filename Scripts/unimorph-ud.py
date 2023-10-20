import csv
import argparse
import os, sys
import warnings

dir = os.path.dirname(sys.argv[0])

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", help="verbose mode", action='store_true')
argParser.add_argument("--debug", help="debugging mode", action='store_true')
argParser.add_argument("-f", "--file", help="lexicon file to convert", action='store_true')
args, moreargs = argParser.parse_known_args()

convfile = dir + '/../Resources/UniMorph-UD.tsv'
convs = {}
with open(convfile) as tsv:
	tsvreader = csv.reader(tsv, delimiter="\t")
	for row in tsvreader:
		convs[row[0]] = row[1]
	
if args.file:
	lexfile = args.file
else:
	lexfile = sys.argv[1]
	
with open(lexfile) as lex:
	tsvreader = csv.reader(lex, delimiter="\t")
	for row in tsvreader:
		upos = ''
		feats = []
		for um in row[2].split(';'):
			if um in convs.keys():
				ud = convs[um]
				if "=" in ud:
					feats.append(ud)		
				else:
					if upos != '':
						warnings.warn('Double upos: ' + row[2] + ' < ' + ud)
					upos = ud
			elif um != row[0]:
				warnings.warn('No conversion for: ' + '\t'.join(row))
		if upos == '':
			upos = '_'
		if feats == []:
			feats.append('_')
		print(row[1] + "\t" + row[0] + "\t" + upos + "\t" + '|'.join(feats))