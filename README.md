# LRG-parser
LRG-xml parser project for Manchester University work. 

Script runs at the command line with LRG number 
or HGNC gene name. 

By default should print transcript information, 
mapping information and differences. Optional flags can be set to
only get a subset of this information. 

Outstanding items:

- Transcript information parsing and printing still needs to be added


## Setup

1. Clone repository 

   > git clone https://github.com/stefpiatek/LRG-parser.git

2. With **Python 3** in a unix environment, set up virtual environment (`pip install virtualenv`
 if not already installed)
    
   > cd LRG-parser
   >
   > virtualenv .venv 
   >
   > source .venv/bin/activate
 
3. Install requirements

   > pip install -r pip_requirements.txt

4. Download LRG data

   > wget ftp://ftp.ebi.ac.uk/pub/databases/lrgex/LRG_*.xml -P lrg_data

## Testing

Run pytest unit test suite (unit tests in `test_lrg_diff.py`)

   > python -m pytest

Unit test coverage is at 74%, with all core functions covered. 

## Usage

For usage information use the `--help` flag:

> python lrg_diff.py --help

    usage: lrg_diff.py [-h] [-t | -m] [-d] input

    Show transcript information and build differences for given LRG

    positional arguments:
      input              LRG or HGNC gene name (e.g. LRG_214 or NF1)

    optional arguments:
      -h, --help         show this help message and exit
      -t, --transcripts  Print transcript information only
      -m, --mapping      Print LRG mapping info only
      -d, --diff         Print LRG differences only

## Examples

**Running script using LRG name:**

> python lrg_diff.py LRG_1

    Placeholder for transcript information

    GRCh37.p13 details:
	    - lrg_start: 1
	    - lrg_end: 24544
	    - other_start: 48259457
	    - other_end: 48284000

    GRCh38.p7 details:
	    - lrg_start: 1
	    - lrg_end: 24544
	    - other_start: 50182096
	    - other_end: 50206639

    Difference at other_start:
	    - GRCh37: 48259457
	    - GRCh38: 50182096

    Difference at other_end:
	    - GRCh37: 48284000
	    - GRCh38: 50206639

    Sequence differences found...
	    - Type: mismatch
	    - Start: 48265495, End: 48265495
	    - Old: A, New: G

**Running script using HGNC gene name:**

> python lrg_diff.py COL1A1

    Placeholder for transcript information


    GRCh37.p13 details:
	    - lrg_start: 1
	    - lrg_end: 24544
	    - other_start: 48259457
	    - other_end: 48284000

    GRCh38.p7 details:
	    - lrg_start: 1
	    - lrg_end: 24544
	    - other_start: 50182096
	    - other_end: 50206639

    Difference at other_start:
	    - GRCh37: 48259457
	    - GRCh38: 50182096

    Difference at other_end:
	    - GRCh37: 48284000
	    - GRCh38: 50206639

    Sequence differences found...
	    - Type: mismatch
	    - Start: 48265495, End: 48265495
	    - Old: A, New: G

**Print LRG mapping info only:**

> python lrg_diff.py -m LRG_1

    GRCh37.p13 details:
	    - lrg_start: 1
	    - lrg_end: 24544
	    - other_start: 48259457
	    - other_end: 48284000

    GRCh38.p7 details:
	    - lrg_start: 1
	    - lrg_end: 24544
	    - other_start: 50182096
	    - other_end: 50206639

**Print transcript information and LRG differences only:**

> python lrg_diff.py -t -d LRG_1

    Placeholder for transcript information


    Difference at other_start:
	    - GRCh37: 48259457
	    - GRCh38: 50182096

    Difference at other_end:
	    - GRCh37: 48284000
	    - GRCh38: 50206639

    Sequence differences found...
	    - Type: mismatch
	    - Start: 48265495, End: 48265495
	    - Old: A, New: G


## User Stories

- Command line input (input from LRG number or gene symbol)
- Automatically use any files in the LRG data folder (will have function to download data files)
- User input error checking
- Print LRG summary (gene name, LRG number, transcripts, number of exons etc)
- Print genomic coordinate and sequence differences between GRCh37 and GRCh38


