import TTSTextNormalization.classification
import pickle
import re

def rulesForCommonWords(line):
    rules = {'Covid19': 'Covid 19', 'covid19': 'covid 19', 'COVID19': 'COVID 19', 'COVID-19': 'COVID 19',
            'Covid-19': 'Covid 19', 'CO2': 'C O 2', 'co2': 'CO 2', 'SARSCoV2': 'SARSCoV 2', 
            ' ° C ': 'degree Celsius', ' ° F ': 'degree Farenheit'}
    for rule, replacement in rules.items():
        line = line.replace(rule, replacement)
    return line
    
def replaceShortforms(line):
    short_replace = {' n t ': "n't ", ' l l': "'ll", ' m ': "'m ", ' v e': "'ve ", 
                    ' s ': "'s ", ' r e ': "'re ", " n't ": "n't "}
    for key, value in short_replace.items():
        # Replace key character with value character in string                    
        line = line.replace(key, value)
        if line.endswith(key[:-1]): # If the part is on the end of the string
            line = line.replace(key[:-1], value[:-1])
    return line

def punctuation(line, punctuation=False):
    line = re.sub(' +', ' ', line)
    marks = (',', '.', '?', '!', '-', ';', ':')
    if punctuation:
        for mark in marks:
            line = line.replace(' ' + mark, mark)
    else:
        for mark in marks:
            line = line.replace(' ' + mark, '')
    return line

class Normalization:
    def __init__(self):
        xgb_model_path = 'TTSTextNormalization/models/xgb_sub5750_5c_4w_5f_v18_model.dat'
        self.model = pickle.load(open(xgb_model_path, 'rb'))
        self.normalizer = TTSTextNormalization.classification.Test()

    def normalization(self, tokens):
        df = self.normalizer.predict(self.model, tokens)
        result = self.normalizer.convert(df)
        line = ' '.join(result['cust_after'])
        return line