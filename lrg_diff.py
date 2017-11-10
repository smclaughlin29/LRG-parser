from argparse import ArgumentParser
from xml.etree import ElementTree as ET
from glob import glob


def index_lrgs(directory="lrg_data/") -> dict:
    """Parse all files in directory and return dict of gene names to LRGs

    :arg
        directory -- str: default to lrg_data, but can be changed for testing

    :return
        gene_names -- dict: gene_name key to LRG value

    :example
        # Assuming directory with LRG_1 and LRG_214
        output = index_lrgs()
        output == {'COL1A1': 'LRG_1', 'NF1': 'LRG_214'}
    """
    files = glob(f"{directory}LRG*.xml")
    gene_names = {}
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        locus = root.find("updatable_annotation"
                          "/annotation_set[@type='lrg']/lrg_locus")
        gene_names[locus.text] = (file.replace(".xml", '')
                                      .replace(directory, ''))
    return gene_names


def choose_file(name: str) -> str:
    """Takes in LRG or gene name and returns LRG file name

    Takes input name and makes it uppercase. if name is in LRG format,
    loads file otherwise runs index_lrgs and looks up name in
    the lookup dictionary.

    :arg
        name -- str: LRG number, or gene_name

    :return
        filename -- str: relative path to filename for the LRG

    :raise
        AssertionError if name is not a string
        KeyError if gene name does not exist in gene_name dict

    :example
        choose_file('lrg_1') == 'lrg_data/LRG_1.xml'
        # assuming directory with LRG_214.xml (NF1)
        choose_file('NF1') == 'lrg_data/LRG_214.xml'

    """
    assert type(name) == str
    name = name.replace(".xml", "").upper()
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

    builds dictionary currently should have keys 'GRCh37.p13' and 'GRCh38.p7'
    - each of these has mapping co-ordinates and list of sequence
      differences (these are themselves dictionaries)

    :arg
        filename -- str: relative path to xml file to parse

    :return
        builds -- dict: dictionary of all lrg genome builds
                  keys for lrg start and end, genome start and end
                  if there are sequence differences:
                    'diff' key contains list of dictionaries of differences

    :raise
        IOError if filename does not exist
        AttributeError if no LRG annotation is found within LRG file
        AssertionError if builds dictionary is not filled
    """
    try:
        tree = ET.parse(filename)
    except IOError:
        raise IOError(f"{filename} does not exist. "
                      "Please enter correct LRG name")

    root = tree.getroot()
    try:
        # list of all mapping annotations for lrgs
        mapping_list = (root.find("updatable_annotation"
                                  "/annotation_set[@type='lrg']")
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


def return_mappings(builds: dict) -> str:
    """Return sequence differences,
    assumes builds are 'GRCh37.p13' and 'GRCh38.p7', update if this changes

    :param
        builds -- dict:

    :example
        return_differences({'GRCh37.p13': {'lrg_start': '1', 'lrg_end': '5000',
                                           'other_start': '50000',
                                           'other_end': '60000',
                                           'diff': [{'type': 'mismatch',
                                                     'other_start': '55000',
                                                     'other_end': '55000',
                                                     'lrg_sequence': 'G',
                                                     'other_sequence': 'A'}]
                                           }
                            'GRCh38.p7': {'lrg_start': '1', 'lrg_end': '5000',
                                           'other_start': '60000',
                                           'other_end': '70000'
                                          }
                            })
    """
    output_list = []
    mapping_keys = ['lrg_start', 'lrg_end', 'other_start', 'other_end']
    # summary of mappings
    for GRC in ['GRCh37.p13', 'GRCh38.p7']:
        output_list.append(f"\n{GRC} details:")
        for key in mapping_keys:
            try:
                output_list.append(f"\t- {key}: {builds[GRC][key]}")
            except KeyError:
                raise KeyError("LRG file corrupted or "
                               "builds have been updated")

    return output_list


def return_differences(builds: dict) -> str:
    """Return mapping and sequence differences,
    assumes builds are 'GRCh37.p13' and 'GRCh38.p7', update if this changes

    :param
        builds -- dict:

    :example
        return_differences({'GRCh37.p13': {'lrg_start': '1', 'lrg_end': '5000',
                                           'other_start': '50000',
                                           'other_end': '60000',
                                           'diff': [{'type': 'mismatch',
                                                     'other_start': '55000',
                                                     'other_end': '55000',
                                                     'lrg_sequence': 'G',
                                                     'other_sequence': 'A'}]
                                           }
                            'GRCh38.p7': {'lrg_start': '1', 'lrg_end': '5000',
                                           'other_start': '60000',
                                           'other_end': '70000'
                                          }
                            })
    """
    output_list = []
    mapping_keys = ['lrg_start', 'lrg_end', 'other_start', 'other_end']
    # write out differences between keys
    for key in mapping_keys:
        if builds['GRCh37.p13'][key] != builds['GRCh38.p7'][key]:
            output_list.append(f"\nDifference at {key}:\n"
                               f"\t- GRCh37: {builds['GRCh37.p13'][key]}\n"
                               f"\t- GRCh38: {builds['GRCh38.p7'][key]}")
    # Sequence differences
    if 'diff' in builds['GRCh37.p13'].keys():
        for diff in builds['GRCh37.p13']['diff']:
            output_list.append("\nSequence differences found...")
            output_list.append(f"\t- Type: {diff['type']}")
            output_list.append(
                f"\t- Start: {diff['other_start']}, End: {diff['other_start']}"
            )
            output_list.append(
                f"\t- Old: {diff['other_sequence']}, "
                f"New: {diff['lrg_sequence']}"
            )

    return output_list


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Show transcript information and '
                    'build differences for given LRG')

    group = parser.add_mutually_exclusive_group()
    parser.add_argument('input', help='LRG or HGNC name (e.g. LRG_214 or NF1)')
    group.add_argument('-t', '--transcripts',
                       help='Print transcript information only',
                       action='store_true')
    group.add_argument('-m', '--mapping',
                       help='Print LRG mapping info only', action='store_true')
    parser.add_argument('-d', '--diff',
                        help='Print LRG differences', action='store_true')
    args = parser.parse_args()

    # run functions
    filename = choose_file(args.input)
    builds = mapping_diff(filename)
    mapping_output = return_mappings(builds)
    diff_output = return_differences(builds)

    if not any([args.transcripts, args.mapping, args.diff]):
        print("Placeholder for transcript information\n")
        for line in mapping_output:
            print(line)
        for line in diff_output:
            print(line)

    if args.transcripts:
        # print transcripts and exons
        print("Placeholder for transcript information\n")
    elif args.mapping:
        for line in mapping_output:
            print(line)

    if args.diff:
        for line in diff_output:
            print(line)
