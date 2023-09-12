# Split Bloodhound files

Bloodhound often fails to load large input files.  
[Existing](https://gist.github.com/mgeeky/3eb9e9caef9136d5b0f3b4dbd5ad77c4) [tools](https://github.com/ustayready/ShredHound) to split those files into chunks often fail due to MemoryErrors (they load the entire input file to memory at once).

This tool uses ijson which loads accessed items to memory only.

## Usage
```
git clone https://github.com/Syslifters/split-bloodhound.git
pip3 install -r requirements.txt
python3 split-bloodhound.py --input input.json
python3 split-bloodhound.py --input input.json --output-dir out/
python3 split-bloodhound.py --input input.json --chunksize 2  # Chunksize 2 GB; default 10% of the filesize
```


