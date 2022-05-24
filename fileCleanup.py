subt = ''
file = 'BookCorpus2'

groups = ['ArXiv', 'BookCorpus2', 'Books3', 'DM Mathematics', 'Enron Emails', 'EuroParl', 'FreeLaw', 'Github', 'Gutenberg (PG-19)', 'HackerNews', 'NIH ExPorter', 'OpenSubtitles', 'OpenWebText2', 'Pile-CC', 'PhilPapers', 'PubMed Central', 'PubMed Abstracts', 'StackExchange', 'Ubuntu IRC', 'USPTO Backgrounds', 'Wikipedia (en)', 'YoutubeSubtitles']
for element in groups:

    for a in range(0, 15):
        print(f'{element}{a}')
        with open(f'{element}{a}', 'r') as f:
            subt = f.read()

        subt = subt.encode('ascii', 'ignore').decode('unicode_escape')
        # subt.join(subtL)

        with open(f'lb/{element}{a}', "w") as f:
            f.write(subt)
        print(f'end of {a}')