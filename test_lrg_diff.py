import pytest

from lrg_diff import choose_file, mapping_diff


class TestChooseFile:
    def test_uppercase_file(self):
        assert choose_file('lrg_12') == 'lrg_data/LRG_12.xml'

    @pytest.mark.xfail
    def test_no_gene(self):
        with pytest.raises(Exception):
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

    def test_lrg_214(self):
        builds = mapping_diff('test_data/LRG_214.xml')
        assert builds
        assert builds['GRCh37.p13']['other_name'] == "17"
        assert builds['GRCh37.p13']['other_name'] == builds['GRCh38.p7']['other_name']

    def test_no_lrg_anno(self):
        with pytest.raises(AttributeError):
            builds = mapping_diff('test_data/LRG_2_no-lrg-annotation_set.xml')
