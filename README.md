# LRG-parser
Parser for LRGs 

## Setup

- Clone repository 

      git clone https://github.com/stefpiatek/LRG-parser.git

- With python 3 in a unix environment, set up virtual environment (`pip install virtualenv`
 if not already installed)
    
      cd LRG-parser
      virtualenv .venv
      source .venv/bin/activate 
- Install requirements

      pip install -r pip_requirements.txt

- Download LRG data

      wget ftp://ftp.ebi.ac.uk/pub/databases/lrgex/LRG_*.xml -P lrg_data

## User Stories

- Command line input (input from LRG number or gene symbol)
- Automatically use any files in the LRG data folder (will have function to download data files)
- User input error checking
- Print LRG summary (gene name, LRG number, transcripts, number of exons etc)
- Print genomic coordinate and sequence differences between GRCh37 and GRCh38
