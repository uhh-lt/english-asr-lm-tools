import json

# set_of_keys = set()

for a in range(0,15):
    sentencedict = {}
    if a < 10:
        with open('pile/0' + str(a) + '.jsonl', 'r') as json_file:
            json_list = list(json_file)
    else:
        with open('pile/' + str(a) + '.jsonl', 'r') as json_file:
            json_list = list(json_file)
    print(f'Reading file {a} done')

    for json_str in json_list:
        result = json.loads(json_str)
        source = result['meta']['pile_set_name']
        result = result['text']

        if sentencedict.get(source):
            sentencedict[source].append(str(result + '\n'))
        else:
            sentencedict[source] = [str(result)]

    print(f'Sorting file {a} done')
    for meta in sentencedict:
        # print(sentencedict[meta])
        open(f'{meta}{a}', 'a').write(str(sentencedict[meta]))
    # sentencedict[source] = 
    # # print(set_of_keys)
    print(f'File {a} finished processing')
    

# print(set_of_keys)

# {'ArXiv', 'BookCorpus2', 'Books3', 'DM Mathematics', 'Enron Emails', 'EuroParl', 'FreeLaw', 'Github', 'Gutenberg (PG-19)', 'HackerNews', 'NIH ExPorter', 'OpenSubtitles', 'OpenWebText2', 'Pile-CC', 'PhilPapers', 'PubMed Central', 'PubMed Abstracts', 'StackExchange', 'Ubuntu IRC', 'USPTO Backgrounds', 'Wikipedia (en)', 'YoutubeSubtitles'}
        
