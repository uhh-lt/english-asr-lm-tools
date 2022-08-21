# english-asr-lm-tools

These tools can be used to prepare texts for asr tasks.
A toolset for german can be found: https://github.com/bmilde/german-asr-lm-tools/

These tools work best with the Pile dataset: https://pile.eleuther.ai/

## Requirements
At least one (or more!) terabyte of free space because the Pile is decompressed 825GB large and some of the following steps create copys of the dataset.

ZST library to decompress the Pile
```
sudo apt install zstd
```
Create and start a virtual environment
```
virtualenv -p python3.9 env
source env/bin/active
pip install -r requirements.txt
```
## Download and decompress Files
At first download and decompress the Pile:
```
./downloadPile.sh
```

The 30 parts are now decompressed in the `pile` folder.

## Sort the files
To run the scripts we need to unmix the files at first.
in `convertPile.py` in Line 10 you can define the needed datasources.
The unmixed data is stored into the pileSorted folder.
To sort the files start
```
python convertPile.py
```

