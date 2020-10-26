import json

import mock
import pytest

from bnb.config import Config, _defaults


class TestConfig:
    content = {
        "folders": [
            {"key": "12345", "color": "#F", "name": "Default"},
            {"key": "67890", "color": "#A", "name": "Programming"},
        ],
        "version": "1.0",
    }

    @pytest.fixture
    def settings_file_cfg(self, tmp_path):
        option = next(co for co in _defaults if co.name == "BNOTE_SETTINGS_FILE")
        settings_file = tmp_path / option.value
        settings_file.write_text(json.dumps(self.content))

        return Config(bnote_settings_file=settings_file)

    def test_init_has_options(self):
        cfg = Config()

        assert hasattr(cfg, "markdown_start")
        assert hasattr(cfg, "metadata_extension")

    @pytest.mark.parametrize("count", (0, 1, 2, 3, 4, 5))
    def test_init_options_have_default_values(self, count):
        cfg = Config()

        option = _defaults[count]
        val = getattr(cfg, option.key)

        assert val == option.default
        assert option.default == option.value

    @pytest.mark.parametrize(
        "cfg_name",
        ("MARKDOWN_START", "MARKDOWN_END", "TAGS_INDICATOR", "BNOTE_SETTINGS_FILE"),
    )
    def test_init_options_get_env_var_as_value(self, cfg_name, monkeypatch):
        monkeypatch.setenv(cfg_name, "New value not in defaults!")
        option = next(co for co in _defaults if co.name == cfg_name)

        cfg = Config()
        val = getattr(cfg, option.key)

        assert val == option.value
        assert option.default != option.value

    def test_init_can_set_new_options(self):
        cfg = Config(spullekes="dingens")

        assert hasattr(cfg, "spullekes")
        assert cfg.spullekes == "dingens"

    def test_init_kwargs_can_override_defaults(self):
        option = _defaults[0]
        kwargs = {option.key: "new_value_not_in_defaults"}

        cfg = Config(**kwargs)
        val = getattr(cfg, option.key)

        assert val == "new_value_not_in_defaults"
        assert val != option.value
        assert val != option.default

    def test_reading_bnote_settings_raises_file_not_found_and_stops(self):
        cfg = Config()

        with pytest.raises(FileNotFoundError):
            cfg.read_boostnote_settings()

    def test_reading_bnote_settings_gives_json(self, settings_file_cfg):
        cfg = settings_file_cfg
        cfg.read_boostnote_settings()

        assert cfg.bnote_settings == self.content

    def test_folders_grouped_from_settings(self, settings_file_cfg):
        folders = settings_file_cfg.folders

        assert len(folders) == 2
        assert folders[0][0] == self.content["folders"][0]["key"]
        assert folders[1][1] == self.content["folders"][1]["name"]

    @mock.patch("bnb.config.json.loads")
    def test_folders_are_cached_when_read(self, mock_loads, settings_file_cfg):
        cfg = settings_file_cfg
        mock_loads.return_value = self.content

        assert not cfg.bnote_settings
        assert mock_loads.call_count == 0

        folders = cfg.folders

        assert cfg.bnote_settings
        assert mock_loads.call_count == 1

        folders_two = cfg.folders

        assert mock_loads.call_count == 1
