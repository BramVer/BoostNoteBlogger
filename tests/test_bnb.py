from pathlib import Path

from bnb.blogger import Blogger


class TestBlogger:
    def test_it_can_run(self, cfg):
        blogger = Blogger(cfg)
        assert hasattr(blogger, "run")

    def test_it_will_create_the_index_file(self, cfg, base_dir):
        assert Path(base_dir).exists()
        assert not Path(base_dir / "index.html").exists()

        blogger = Blogger(cfg)
        blogger.run()

        assert Path(base_dir / "index.html").exists()
