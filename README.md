# english-asr-lm-tools

These tools can be used to prepare texts for asr tasks.
A toolset for german can be found: https://github.com/bmilde/german-asr-lm-tools/

These tools work best with the Pile dataset: https://pile.eleuther.ai/

## Requirements
ZST library to decompress the Pile
```
sudo apt install zstd
```
Create an virtual environment
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

