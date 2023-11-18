import re, subprocess, time, udm_functions, os
import udm_functions as udm

desc = "UDPIPE 1"
inputs = ["plain", "conllu"]
input = "plain"
output = "conllu"
raw = ""

def runtagger(lang, txt):
    tmpfile = "/tmp/udm-"+str(int(time.time()))
    with open(tmpfile, "w") as text_file:
        text_file.write(txt)
    if input == "conllu":
        result = subprocess.check_output(['udpipe', '--tag', '--input=conllu', lang, tmpfile]).decode('utf-8')
    else:
        result = subprocess.check_output(['udpipe', '--tag', '--tokenize', lang, tmpfile]).decode('utf-8')
    os.remove(tmpfile)
    sents = udm.load_conllu(result)
    global raw
    raw = result
    return sents