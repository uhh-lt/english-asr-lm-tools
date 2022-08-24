import cleanupTools
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from bz2 import BZ2File as bzopen
import argparse
import multiprocessing
import re
import os

# Tokenizer
nlpT = English()
tokenizer = nlpT.tokenizer

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
            try:
                line = normalizer.normalization(tokens)
            except:
                continue
            line = line.replace('\n', '')
            if line.isspace():
                continue
            if not any(x for x in line if x.isnumeric()):
                line = cleanupTools.replaceShortforms(line)
                line = cleanupTools.punctuation(line, punctuation)
            else:
                continue
            if not any(x for x in line if x.isalpha()):
                continue
            if any(x in line for x in ('-', '<', '>', '§', '/', '*', '°')):
                continue
            if len(line.split(' ')) < 3: # remove short lines
                continue
            if not re.findall("[\s']\S[\s']\S[\s']\S", line): # Catches words like "m i d d a's"
                temp.append(line.lower())

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=False, default='wikipedia', help='changes the source folder')
    parser.add_argument('-o', '--output', type=str, required=False, default='wikiclean', help='changes the destination folder')
    parser.add_argument('-p', '--punctuation', type=bool, required=False, default=False, help='Remove(default) or preserve punctuation')
    parser.add_argument('-n', '--number', type=int, required=False, default=40, help='Number of multiprocessing tasks')
    args = parser.parse_args()
    input = args.input
    output = args.output
    punctuation = args.punctuation
    processes = args.number
    
    wikifiles =[]
    for subdir, dirs, files in os.walk(input):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".bz2"):
                wikifiles.append(filepath)

    # Create output folders
    if not os.path.exists(output):
        os.makedirs(f'{output}/wikipedia/AA')
        os.makedirs(f'{output}/wikipedia/AB')
        os.makedirs(f'{output}/wikipedia/AC')

    pool = multiprocessing.Pool(processes)
    subtitles = pool.map(completeRun, wikifiles)
    pool.close()