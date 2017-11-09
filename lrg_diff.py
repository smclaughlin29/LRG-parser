from xml.etree import ElementTree as ET
from glob import glob


def index_lrgs(directory="lrg_data/") -> dict:
    """Parse all files in directory and return dict of gene names to LRGs"""
    files = glob(f"{directory}LRG*.xml")
    gene_names = {}
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        locus = root.find("updatable_annotation/annotation_set[@type='lrg']/lrg_locus")
        gene_names[locus.text] = (file.replace(".xml", '')
                                      .replace(directory, ''))
    return gene_names

def choose_file(name: str) -> str:
    """Takes in LRG or gene name and returns LRG file name

    """
    assert type(name) == str
    name = name.upper()
    if name.startswith('LRG_'):
        lrg = name
    else:
        # create dictionary of gene names to LRGs
        gene_names = index_lrgs()
        try:
            # try lookup of gene name
            lrg = gene_names[name]
        except KeyError:
            raise KeyError(f"No LRG found for gene {name}")

    filename = f"lrg_data/{lrg}.xml"
    return filename


def mapping_diff(filename):

    try:
        tree = ET.parse(filename)
    except IOError:
        raise IOError(f"{filename} does not exist. Please enter correct LRG name")

    root = tree.getroot()

    try:
        mapping_list = (root.find("updatable_annotation/annotation_set[@type='lrg']")
                            .findall("mapping"))
    except AttributeError:
        raise AttributeError("No LRG annotation found, corrupted LRG file?\n"
                              f"Please check {filename}")

    builds = {}

    for item in mapping_list:
        builds[item.attrib['coord_system']] = item.attrib

    assert builds, "No mapping co-ordinates found"

    return builds
