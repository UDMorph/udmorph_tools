from requests.auth import HTTPBasicAuth
import requests
import re, os, csv, sys

desc = "CTexT NCHLT Web Services"

x2f= {}
x2u = {}

here = os.path.dirname(sys.argv[0])
upostr = here + "/../Resources/CText-UD.tsv"
with open(upostr) as file:
    tsv_file = csv.reader(file, delimiter="\t")
    for line in tsv_file:
        if len(line) > 1:
            x2u[line[0]] = line[1]
        if len(line) > 2:
            x2f[line[0]] = line[2]


def runtagger(lang, txt):

    response = requests.post("https://v-ctx-lnx7.nwu.ac.za:8443/CTexTWebAPI/services/setuser", headers={"Authorization":"Basic SGllcmRpZSBzYWwgd2Vyaw==","Connection":"keep-alive"})
    token = response.json()['token'][0]

    url = "https://v-ctx-lnx7.nwu.ac.za:8443/CTexTWebAPI/services?core=pos&lang=" + lang + "&text=" + txt
    response = requests.get(url, headers={"Authtoken":token})
    if 'PoS Tagger-streams' not in response.json().keys():
        print ("Failed to load tagged data - " + response.text)
        quit()
    poslist = response.json()['PoS Tagger-streams']

    dotxt = txt
    # print(txt)

    ord = 0
    senttxt = ""
    toktxt = ""
    lastform = ""
    sents = []
    sent = {"tokens": []}
    for j, pst in enumerate(poslist):

        tmp = pst.split('\t')
        form = tmp[0]
        
        token = {}

        if lastform:
            if dotxt.startswith(form):
                token['misc'] = "SpaceAfter=No"
            else:
                senttxt = senttxt + " "
                token['misc'] = "_"
            lastform = ""
            dotxt = dotxt.lstrip()
            dotxt = dotxt.lstrip(form)
        else:
            if ord > 0 :
                toktxt = toktxt  + "\t_\n"
            dotxt = dotxt.lstrip()
            dotxt = dotxt.lstrip(form)

        if pst == '':
            continue

        if pst == '\n':
            sent['text'] = senttxt
            sents.append(sent)
            sent = {"tokens": []}
            ord = 0
            senttxt = ""
            continue
            
        token['lemma'] = token['upos'] = token['feats'] = token['form'] = token['xpos'] = token['head'] = token['deprel'] = token['deps'] = token['misc'] = "_"

        token['form'] = tmp[0]
        if len(tmp) > 1:
            token['xpos'] = tmp[1]

        tmp = re.sub('\d+$', '', token['xpos']) # This should also do numbers prob. (the CSV can be big)
        token['upos'] = x2u[token['xpos']] if token['xpos'] in x2u.keys() else x2u[tmp] if tmp in x2u.keys() else "_"
        token['feats'] = x2f[token['xpos']] if token['xpos'] in x2f.keys() else x2f[tmp] if tmp in x2f.keys() else "_"

        ord = ord + 1
        token['ord'] = str(ord)
        
        sent['tokens'].append(token)
    
        senttxt = senttxt + form 
    
        lastform = form
        
    return sents