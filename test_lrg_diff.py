import pytest

from .lrg_diff import choose_file


class TestChooseFile:
    def test_uppercase_file(self):
        assert choose_file('lrg_12') == 'lrg_data/LRG_12.xml'

    def test_no_lrg(self):
        with pytest.raises(Exception):
            choose_file('LRG__1')

    @pytest.mark.xfail
    def test_no_gene(self):
        with pytest.raises(Exception):
            choose_file('honestly_not_a_gene')

    def test_number_input(self):
        with pytest.raises(AssertionError):
            choose_file(5)
   

