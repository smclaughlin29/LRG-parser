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


def mapping_diff(filename: str) -> dict:
    """Parses XML and returns dict of genome build mappings and differences



    """
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
        build_dict = item.find("mapping_span").attrib
        assert build_dict['lrg_start'] < build_dict['lrg_end'], (
                f"LRG start smaller than LRG end for {filename}")
        assert build_dict['other_start'] < build_dict['other_end'], (
                f"g. start smaller than g. end for {filename}")
        if item.findall("mapping_span/diff"):
            # if there is a base mismatch, add all of them to the dictionary
            for difference in item.findall("mapping_span/diff"):
                if 'diff' not in build_dict.keys():
                    # no diff make dictionary with current difference in
                    build_dict['diff'] = [difference.attrib]
                else:
                    # otherwise append to list of differences
                    build_dict['diff'].append(difference.attrib)
        # save build differences to builds dict using build as key
        builds[item.attrib['coord_system']] = build_dict


    assert builds, "No mapping co-ordinates found"

    return builds
