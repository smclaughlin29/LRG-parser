
def choose_file(name: str) -> str:
    """Takes in LRG or gene name and returns LRG file name 

    """
    assert type(name) == str
    name = name.upper()
    if name.startswith('LRG_'):
        filename = f"lrg_data/{name}.xml"
 

    return filename
