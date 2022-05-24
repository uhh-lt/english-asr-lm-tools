import cleanupTools
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from bz2 import BZ2File as bzopen
import multiprocessing
import re
import os

# Tokenizer
nlpT = English()
tokenizer = nlpT.tokenizer

folder = 'wikipedia/'

processes = 40 # Number of processes

def readFile(filename):
    content = []
    with bzopen(filename) as bzin:
        for line in bzin:
            if line.isspace():
                continue
            else:
                content.append(line.decode('utf-8'))
    return content

def splitArticle(content):
    sentences = []
    temp = []
    for line in content:
        temp.extend(line.split('. '))
    for sentence in temp:
        if sentence.isspace():
            continue
        sentences.append(sentence)
    return sentences

def normalization(content):
    normalizer = cleanupTools.Normalization()
    temp = []

    for line in content:
        if line:
            if any(x in line for x in ('[', ']', "r'", '"', ')', '(', '%', '&', '=', '`', '#', '+', '~', '<', '|', '}', '{', '^')):
                continue
            line = cleanupTools.rulesForCommonWords(line)
            tokens = tokenizer(line)
            # print(f'{line = }')
            line = normalizer.normalization(tokens)
            line = line.replace('\n', '')
            if line.isspace():
                continue
            if not any(x for x in line if x.isnumeric()):
                line = cleanupTools.replaceShortforms(line)
                line = cleanupTools.punctuation(line)
            else:
                print(line)
                continue
            if not any(x for x in line if x.isalpha()):
                continue
            if any(x in line for x in ('-', '.', ',', '<', '>', '§', '/', '*', '°')):
                continue
            if len(line.split(' ')) < 3: # remove short lines
                continue
            if not re.findall("[\s']\S[\s']\S[\s']\S", line): # Catches words like "m i d d a's"
                temp.append(line.lower())
            else:
                print(line)

    text = '\n'.join(str(elem) for elem in temp)
    return text

def writeFile(sentences, filename):
    filename = filename.split('.')[0]
    with open(f'wikiclean/{filename}', 'w') as f:
        f.write(sentences)

def completeRun(filename):
    content = readFile(filename)
    text = normalization(content)
    writeFile(text, filename)

if __name__ == "__main__":
    wikifiles =[]
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            #print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            if filepath.endswith(".bz2"):
                wikifiles.append(filepath)
    print(wikifiles)
    
    pool = multiprocessing.Pool(processes)
    subtitles = pool.map(completeRun, wikifiles)

    # content = readFile('wikiclean/AA/wiki_00.bz2')
    # sentences = splitArticle(content)
    # sentences = normalization(sentences)
    # writeFile(sentences)