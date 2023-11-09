import argparse
import re, glob, random, os

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", help="verbose mode", action='store_true')
argParser.add_argument("--debug", help="debugging mode", action='store_true')
argParser.add_argument("--input", "-i", help="Folder with CoNLL-U files to distribute", required=True)
argParser.add_argument("--output", "-o", help="Folder to write dev/test/train", required=True)
argParser.add_argument("--corpus", "-c", help="Corpus name", default="")
args, moreargs = argParser.parse_known_args()

def load_conllu_file(data_file):
    with open(data_file, "r", encoding="utf-8") as f:
        data = f.read()
        fileid = data_file.split("/").pop().replace(".conllu", "")
        return load_conllu(data, fileid)

def load_conllu(string, fileid = ""):
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
            if fileid != "":
                line = line.replace("tokId=", "fileId="++"|tokId=")
            sent['tokens'].append(line)
            sent['count'] = len(sent['tokens'])
        if 'text' in sent.keys() and len(sent['tokens']):
            sents.append(sent)
    return sents

sents = []
totcnt = 0
for file in glob.glob(args.input + '/*.conllu'):
    if args.verbose:
        print(file)
    tmp = load_conllu_file(file)
    sents = sents + tmp
    totcnt = totcnt + sum(sent['count'] for sent in tmp)
    
random.shuffle(sents)
print(str(len(sents)) + ' sentences')
print(str(totcnt) + ' tokens')
print('---------------')

basename = args.corpus
tmp = os.path.abspath(args.input).split('/')
while basename == 'git' or basename == 'git-files' or basename == 'conllu' or basename == 'data' or basename == '':
    basename = tmp.pop()

fs = {}
fs['test'] = open(args.output + '/' + basename + "-test.conllu", "w")
fs['train'] = open(args.output + '/'  + basename + "-train.conllu", "w")
fs['dev'] = open(args.output + '/'  + basename + "-dev.conllu", "w")
sd = {}
sd['train'] = 0
sd['test'] = 0
sd['dev'] = 0
ss = {}
ss['train'] = 0
ss['test'] = 0
ss['dev'] = 0
sz = {}
sz['train'] = int(totcnt*0.8)
sz['test'] = int(totcnt*0.1)
sz['dev'] = int(totcnt*0.1)
for sent in sents:
    dest = "train"
    for c in fs.keys():
        if sd[c] < sz[c]:
            dest = c
    fs[dest].write("# text = " + sent['text'] + "\n")
    fs[dest].write("\n".join(sent['tokens']) + "\n\n")
    sd[dest] = sd[dest] + len(sent['tokens'])
    ss[dest] = ss[dest] + 1

for c in fs.keys():
    print(c, sz[c], sd[c], ss[c])


