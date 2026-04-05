# DDR ARC

Extract and create DDRA archives

`pip install tqdm`

`python arc_extract.py file.arc [file2.arc]`

`python arc_create.py folder file.arc`

`python arc_extract_to_dal.py file.arc [file2.arc]`

## Dal
Converting .arc to .dal *(or .inc)* enables the game to read files in folders directly without repacking .arc files. Note that hex editing the respective gamemdx.dll string file.arc -> file.dal is required.

Credit and thanks to nibs for this discovery!
