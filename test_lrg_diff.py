import pytest

from lrg_diff import (choose_file, mapping_diff, index_lrgs, return_mappings,
                      return_differences)


class TestChooseFile:
    def test_uppercase_file(self):
        """if lowercase name given, final output should have uppercase LRG"""
        assert choose_file('lrg_12') == 'lrg_data/LRG_12.xml'

    def test_remove_xml(self):
        """if '.xml' in input, the final file should still be valid"""
        assert choose_file('LRG_12.xml') == 'lrg_data/LRG_12.xml'

    def test_no_gene(self):
        """if an gene name is given that doesn't exist, raise KeyError"""
        with pytest.raises(KeyError):
            choose_file('honestly_not_a_gene')

    def test_number_input(self):
        """If input is not a str, should raise AssertionError"""
        with pytest.raises(AssertionError):
            choose_file(5)


class TestMappingDiff:
    def test_no_file(self):
        """If file does not exist, should raise IOError"""
        with pytest.raises(IOError):
            mapping_diff('test_data/not_a_file')

    def test_lrg_1(self):
        """test using lrg_1 data"""
        builds = mapping_diff('test_data/LRG_1.xml')
        # dictionary should not be empty
        assert builds
        assert builds['GRCh37.p13']['other_start'] == "48259457"
        assert builds['GRCh38.p7']['other_end'] == "50206639"
        # should have a sequence difference
        assert builds['GRCh37.p13']['diff']
        # should only have one sequence difference
        assert len(builds['GRCh37.p13']['diff']) == 1

    def test_lrg_214(self):
        """test using LRG_214 data"""
        builds = mapping_diff('test_data/LRG_214.xml')
        # dictionary should not be empty
        assert builds
        assert builds['GRCh37.p13']['lrg_end'] == "289701"
        # lrg_end of both builds should be the same
        GRC37 = builds['GRCh37.p13']['lrg_end']
        GRC38 = builds['GRCh38.p7']['lrg_end']
        assert GRC37 == GRC38

    def test_no_lrg_anno(self):
        """If no lrg anntation in LRG file, should raise AttributeError"""
        with pytest.raises(AttributeError):
            builds = mapping_diff('test_data/no-lrg-annotation_set_LRG_2.xml')

    def test_multiple_diff(self):
        """LRG with multiple sequence differences

         differences list should have more than one item
        """
        builds = mapping_diff('test_data/LRG_992.xml')
        assert len(builds['GRCh37.p13']['diff']) > 1


class TestIndexLRGs:
    def test_HGNC(self):
        """gene name should map to the correct LRG after indexing"""
        gene_names = index_lrgs('test_data/')
        assert gene_names
        assert gene_names['COL1A1'] == 'LRG_1'
        assert gene_names['NF1'] == 'LRG_214'


class TestReturnMappings:
    def setup(self):
        """setup for tests, allowing the same object to be used in class"""
        self.builds = {'GRCh37.p13': {'lrg_start': '1', 'lrg_end': '5000',
                                      'other_start': '50000',
                                      'other_end': '60000',
                                      'diff': [{'type': 'mismatch',
                                                'other_start': '55000',
                                                'other_end': '55000',
                                                'lrg_sequence': 'G',
                                                'other_sequence': 'A'}]
                                      },
                       'GRCh38.p7': {'lrg_start': '1', 'lrg_end': '5000',
                                     'other_start': '60000',
                                     'other_end': '70000'
                                     }
                       }

    def test_summary(self):
        """summary information sanity check"""
        builds = dict(self.builds)
        output = return_mappings(builds)
        # generator expression in square brackets makes a list of booleans
        # - if "lrg_start: 1" in any item in the list of strings, returns True
        assert any(["lrg_start: 1" in line
                    for line in output])
        assert any(["lrg_end: 5000" in line
                    for line in output])

    def test_invalid_build(self):
        """should raise KeyError if either build isn't found in dictionary"""
        for GRC in ['GRCh37.p13', 'GRCh38.p7']:
            builds = dict(self.builds)
            builds.pop(GRC)
            with pytest.raises(KeyError):
                return_mappings(builds)


class TestReturnDifferences:
    def setup(self):
        """Setup function to allow for objects to be used across class"""
        self.builds = {'GRCh37.p13': {'lrg_start': '1', 'lrg_end': '5000',
                                      'other_start': '50000',
                                      'other_end': '60000',
                                      'diff': [{'type': 'mismatch',
                                                'other_start': '55000',
                                                'other_end': '55000',
                                                'lrg_sequence': 'G',
                                                'other_sequence': 'A'}]
                                      },
                       'GRCh38.p7': {'lrg_start': '1', 'lrg_end': '5000',
                                     'other_start': '60000',
                                     'other_end': '70000'
                                     }
                       }

    def test_mapping_only(self):
        """remove sequence differences,
        should only report mapping differences"""
        builds = dict(self.builds)
        builds['GRCh37.p13'].pop('diff')
        output = return_differences(builds)
        assert not any(["sequence differences" in line
                        for line in output])
        assert any(["70000" in line
                    for line in output])

    def test_sequence_diff(self):
        """should report mapping and sequence differences"""
        builds = dict(self.builds)
        output = return_differences(builds)
        assert any(["Sequence differences" in line
                    for line in output])
        assert any(["Difference at other_start" in line
                    for line in output])
        assert any(["70000" in line
                    for line in output])

    def test_invalid_build(self):
        """should raise KeyError if either build isn't found in dictionary"""
        for GRC in ['GRCh37.p13', 'GRCh38.p7']:
            builds = dict(self.builds)
            builds.pop(GRC)
            with pytest.raises(KeyError):
                return_mappings(builds)
