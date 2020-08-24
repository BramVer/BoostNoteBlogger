import pytest

from bnb.config import Config, _defaults


class TestConfig:
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

    @pytest.mark.parametrize("cfg_name", (
        "MARKDOWN_START",
        "MARKDOWN_END",
        "TAGS_INDICATOR",
        "BNOTE_SETTINGS_FILE")
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
