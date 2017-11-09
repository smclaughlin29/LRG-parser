from xml.etree import ElementTree as ET


def choose_file(name: str) -> str:
    """Takes in LRG or gene name and returns LRG file name 

    """
    assert type(name) == str
    name = name.upper()
    if name.startswith('LRG_'):
        filename = f"lrg_data/{name}.xml"
    else:
        # try to lookup

    return filename


def mapping_diff(filename):

    try:
        tree = ET.parse(filename)
    except IOError:
        raise IOError(f"{filename} does not exist. Please enter correct LRG name")

    root = tree.getroot()

    mapping_list = (root.find("updatable_annotation/annotation_set[@type='lrg']")
                        .findall("mapping"))

    builds = {}

    for item in mapping_list:
        builds[item.attrib['coord_system']] = item.attrib

    assert builds, "No mapping co-ordinates found"

    return builds



