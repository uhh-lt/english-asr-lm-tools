import json
import os

sourceFolder = 'pile'
destinationFolder = 'pileSorted'

# {'ArXiv', 'BookCorpus2', 'Books3', 'DM Mathematics', 'Enron Emails', 'EuroParl', 'FreeLaw', 'Github', 'Gutenberg (PG-19)', 'HackerNews', 'NIH ExPorter', 'OpenSubtitles', 'OpenWebText2', 'Pile-CC', 'PhilPapers', 'PubMed Central', 'PubMed Abstracts', 'StackExchange', 'Ubuntu IRC', 'USPTO Backgrounds', 'Wikipedia (en)', 'YoutubeSubtitles'}

# The parts of the dataset which are saved into seperate files
keep = ['YoutubeSubtitles']

if not os.path.exists(destinationFolder):
    os.makedirs(destinationFolder)

for a in range(0,30):
    filename = f'{a:02d}.jsonl'
    print(f'Reading {filename}')
    sentencedict = {}

    with open(f'{sourceFolder}/{filename}', 'r') as json_file:
        json_list = list(json_file)

    print(f'Sorting {filename}')

    for json_str in json_list:
        result = json.loads(json_str)
        source = result['meta']['pile_set_name']
        result = result['text']

        if source in keep:
            if sentencedict.get(source):
                sentencedict[source].append(str(result + '\n'))
            else:
                sentencedict[source] = [str(result)]

    print(f'Writing sorted data from {filename}')

    for meta in sentencedict:
        with open(f'{destinationFolder}/{meta}_{a}', 'a') as output:
            part = '\n'.join(sentencedict[meta])
            output.write(part)

    print(f'Finished processing {filename}')

print('All files are processed')