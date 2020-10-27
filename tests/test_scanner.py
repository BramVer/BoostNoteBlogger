import pytest

from bnb.scanner import Scanner


class TestScanner:
    @pytest.fixture
    def scanner(self, cfg):
        return Scanner(cfg)

    def test_it_can_run(self, scanner, tmp_path):
        assert hasattr(scanner, "run")

    def test_it_runs_a_list_of_results(self, scanner, tmp_path):
        assert isinstance(scanner.run(tmp_path), list)

    def test_it_lists_all_files(self, scanner, base_dir):
        result = scanner.run(base_dir)

        assert len(result) == 15
        assert len([r for r in result if "subfolder" in str(r)]) == 15
        assert len([r for r in result if "subbestfolder" in str(r)]) == 5
