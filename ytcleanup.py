import cleanupTools
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import spacy_fastlang
import multiprocessing
import os
import re

punctuation = False

folder = 'lb/'

processes = 30 # Number of processes

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("language_detector")

# Tokenizer
nlpT = English()
tokenizer = nlpT.tokenizer


def readFile(filename):
    print('read file')
    with open(f'{folder}{filename}', 'r') as f:
        subtitles = f.read()
    # subtitles = '["Hey everybody I wanted to give a little plug real quick.'
    subtitles = subtitles.split('\n')
    return subtitles

def firstStage(subtitles):
    temp = []
    print('First stage')
    drop = False
    for line in subtitles: # Try to remove lines with [ ] and blocks of text with languages other than english
        # print(line)
        if not drop:
            if any(x in line for x in ('Arabic:', 'Bulgarian:', 'Chinese:', 'Czech:', 
                                        'Danish:', 'Dutch:', 'Finnish:', 'French:', 'German:', 
                                        'Hindi:', 'Hungarian:', 'Indonesian:', 'Italian:', 'Japanese:',
                                        'Korean:', 'Latvian:', 'Norwegian:', 'Persian:', 'Panjabi:',
                                        'Polish:', 'Portuguese:', 'Romanian:', 'Russian:',
                                        'Serbian:', 'Slovenian:', 'Spanish:', 'Swedish:', 'Thai:',
                                        'Turkish:', 'Ukrainian:', 'Urdu:', 'Vietnamese:')):
                drop = True
                continue
            if line:
                if any(x in line for x in ('English:', '(audience', '(sighs)', '/', '\\', 'www.', '.edu', '.com', '.org', '*', '(music)')):
                    continue
                if (line == "music"):
                    continue
                if any(x in line for x in ('[', ']', '"', ')', '(', '%', '&', '=', '`', '#', '+', '~', '<', '|', '}', '{', '^', )):
                    continue
                if line.isspace():
                    continue
                if line.isupper():
                    continue
                if any(c.isalpha() for c in line):
                    lineC = line.replace('", "', '').replace('", \'', '').replace('\', "', '').replace('-', '').replace('\', \'', '').replace('_', '').replace('>>', '').replace('  ', ' ').replace(';', '').replace("', '", "")
                    lineC = cleanupTools.rulesForCommonWords(lineC)
                    lineC = lineC.lstrip()
                    temp.append(lineC)
                
        else:
            if (line.isspace()) or (line =="English:") or (line.startswith("', '")):
                drop = False
            else:
                continue
    print("finished sort part one")
    return temp

def secondStage(subtitles):
    # Second stage is to combine single lines with a point and stick it to the previuos line if the line doesn't end with a dot.
    temp = []
    skip = False
    for id, __ in enumerate(subtitles):
        # print(id)
        if (id < len(subtitles)-1 ):
            if not skip:
                if (not subtitles[id].endswith('.')) and (subtitles[id+1].endswith('.')):
                    temp.append(subtitles[id] + ' ' + subtitles[id+1])
                    skip = True
                else:
                    temp.append(subtitles[id])
            else:
                # print(f'got one! See: {subtitlesC[id-1]} {subtitlesC[id]}')
                # print(f'line {id -1} and {id}')
                skip = False
    return temp

def thirdStage(subtitles): # Detect the rest of the sentences with spacy
    print('Third stage with spacy language detection and normalization')

    normalizer = cleanupTools.Normalization()
    temp = []

    for line in subtitles:
        result = nlp(line)
        if (result._.language == 'en') and (result._.language_score >= 0.8):
            tline = line
            tokens = tokenizer(tline)
            
            tline = normalizer.normalization(tokens)

            if not any(x for x in tline if x.isnumeric()):
                tline = cleanupTools.replaceShortforms(tline)
                tline = cleanupTools.punctuation(tline, False)
            else:
                print(tline)
                continue
            temp.append(tline)
    text = '\n'.join(str(elem) for elem in temp)
    return text

def writeToFile(subtitles, filename):
    # text = '\n'.join(str(elem).lower() for elem in subtitles)
    with open('ytClean' + filename, 'w') as f:
        f.write(subtitles)

def oneTurn(filename):
    subtitles = readFile(filename)
    subtitles = firstStage(subtitles)
    subtitles = secondStage(subtitles)
    subtitles = thirdStage(subtitles)
    writeToFile(subtitles, filename)
    return subtitles

if __name__ == '__main__':
    files = [x for x in os.listdir(folder) if x.startswith('YoutubeSubtitles')]
    pool = multiprocessing.Pool(processes)
    subtitles = pool.map(oneTurn, files)
    print(x for x in subtitles if len(x))
    # writeToFile(subtitles)
