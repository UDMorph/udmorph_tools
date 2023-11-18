import re

def load_conllu(string):
    sentences = string.strip().split("\n\n")
    sents = []
    for sentence in sentences:
        sent = {"tokens": []}
        lines = sentence.strip().split("\n")
        for line in lines:
            if line[0:9] == '# text = ':
                sent['text'] = line[9:]
                continue
            if line[0:12] == '# sent_id = ':
                sent['id'] = line[12:]
                continue
            if line[0:1] == '#':
                continue
            if re.match(r"^(\d+)-(\d+)\t", line):
                continue
            token = {}
            cols = line.split("\t") + ['_', '_', '_', '_', '_', '_', '_', '_', '_']
            token['ord'] = cols[0]
            token['form'] = cols[1]
            token['lemma'] = cols[2]
            token['upos'] = cols[3]
            token['xpos'] = cols[4]
            token['feats'] = cols[5]
            token['head'] = cols[6]
            token['deprel'] = cols[7]
            token['deps'] = cols[8]
            token['misc'] = cols[9]
            sent['tokens'].append(token)
        sents.append(sent)
    return sents

def print_conllu(obj):
	for sent in obj:
		if "id" in sent.keys():
			print("# sent_id = " + sent['id'])
		print("# text = " + sent['text'])
		for i, token in enumerate(sent['tokens']):
			if "ord" not in token.keys():
				 token['ord'] = str(i+1)
			if not "form" in token.keys() :
				token['form'] = "_"            
			if not "lemma" in token.keys() :
				token['lemma'] = "_"            
			if not "upos" in token.keys() :
				token['upos'] = "_"            
			if not "xpos" in token.keys():
				token['xpos'] = "_"  
			if not "feats" in token.keys():           
				token['feats'] = "_"
			if not "deprel" in token.keys() :
				token['deprel'] = "_"  
			if not "deps" in token.keys()  :        
				token['deps'] = "_"   
			if not "head" in token.keys()   :       
				token['head'] = "_" 
			if not "misc" in token.keys()   :         
				token['misc'] = "_"          
			print(token['ord'] + "\t" + token['form'] + "\t" + token['lemma'] + "\t" + token['upos'] + "\t" + token['xpos'] + "\t" + token['feats'] + "\t" + token['head'] + "\t" + token['deprel'] + "\t" + token['deps'] + "\t" + token['misc']  ) 
		print ("")

def maptoks(inp, outp):
    for i, si in enumerate(inp):
        so = outp[i]
        if si['text'].replace(" ", "") != so['text'].replace(" ", ""):
            # Sentence mismatch - resolve?
            wrong = 1
        for j, ti in enumerate(si['tokens']):
            to = so['tokens'][j]
            if ti['form'] != to['form']:
                # Token mismatch - resolve?
                wrong = 1
                continue
            for key in to.keys():
                if to[key] != '_' and ti[key] != to[key]:
                    ti[key] = to[key] if ti[key] == '_' else ti[key] + '|' + to[key]
    return inp