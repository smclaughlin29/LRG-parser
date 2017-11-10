import pytest

from lrg_diff import choose_file, mapping_diff, index_lrgs, return_differences


class TestChooseFile:
    def test_uppercase_file(self):
        assert choose_file('lrg_12') == 'lrg_data/LRG_12.xml'

    def test_no_gene(self):
        with pytest.raises(KeyError):
            choose_file('honestly_not_a_gene')

    def test_number_input(self):
        with pytest.raises(AssertionError):
            choose_file(5)


class TestMappingDiff:
    def test_no_file(self):
        with pytest.raises(IOError):
            mapping_diff('test_data/not_a_file')

    def test_lrg_1(self):
        builds = mapping_diff('test_data/LRG_1.xml')
        assert builds
        assert builds['GRCh37.p13']['other_start'] == "48259457"
        assert builds['GRCh38.p7']['other_end'] == "50206639"
        assert builds['GRCh37.p13']['diff']

    def test_lrg_214(self):
        builds = mapping_diff('test_data/LRG_214.xml')
        assert builds
        assert builds['GRCh37.p13']['lrg_end'] == "289701"
        assert builds['GRCh37.p13']['lrg_end'] == builds['GRCh38.p7']['lrg_end']

    def test_no_lrg_anno(self):
        with pytest.raises(AttributeError):
            builds = mapping_diff('test_data/no-lrg-annotation_set_LRG_2.xml')


class TestIndexLRGs:
    def test_HGNC(self):
        gene_names = index_lrgs('test_data/')
        assert gene_names
        assert gene_names['COL1A1'] == 'LRG_1'
        assert gene_names['NF1'] == 'LRG_214'


class TestReturnDifferences:
    def setup(self):
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
        builds = dict(self.builds)
        builds['GRCh37.p13'].pop('diff')
        output = return_differences(builds)
        assert not any(["sequence differences" in line
                        for line in output])
        assert any(["70000" in line
                    for line in output])

    def test_sequence_diff(self):
        builds = dict(self.builds)
        output = return_differences(builds)
        assert any(["Sequence differences" in line
                    for line in output])
        assert any(["Difference at other_start" in line
                    for line in output])
        assert any(["70000" in line
                    for line in output])

    def test_invalid_build(self):
        builds = dict(self.builds)
        builds.pop('GRCh37.p13')
        with pytest.raises(KeyError):
            return_differences(builds)
