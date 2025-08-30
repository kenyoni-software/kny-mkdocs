import importlib.resources as ir
import logging
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

from mkdocs.config.base import Config as MkConfig
from mkdocs.config.config_options import Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files, InclusionLevel

import kny_mkdocs.utils as utils


class Config(MkConfig):
    admonition_idea = Type(bool, default="")
    mathjax = Type(str, default="")
    tablesort = Type(str, default="")


class Plugin(BasePlugin[Config]):
    _CACHE_DIR: Path = Path(tempfile.gettempdir()).joinpath("kny_mkdocs_cache")
    _MATHJAX_DIR: Path = _CACHE_DIR.joinpath("mathjax")
    _TABLESORT_FILE: Path = _CACHE_DIR.joinpath("tablesort.min.js")

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        if self.config.admonition_idea:
            self._add_admonition(config)
        if self.config.mathjax != "":
            self._add_mathjax(config)
        if self.config.tablesort:
            self._add_tablesort(config)

    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files | None:
        if self.config.admonition_idea:
            files.append(
                File.generated(
                    config,
                    "assets/stylesheets/kny/admonition_idea.css",
                    abs_src_path=str(ir.files(__package__).joinpath("admonition_idea.css")),
                    inclusion=InclusionLevel.NOT_IN_NAV,
                )
            )
        if self.config.mathjax:
            files.append(
                File.generated(
                    config,
                    "assets/javascripts/kny/mathjax.js",
                    abs_src_path=str(ir.files(__package__).joinpath("mathjax.js")),
                    inclusion=InclusionLevel.NOT_IN_NAV,
                )
            )
            utils.add_files_recursive(Plugin._MATHJAX_DIR, Path("assets/javascripts/mathjax/"), files, config)
        if self.config.tablesort:
            files.append(
                File.generated(
                    config,
                    "assets/javascripts/kny/tablesort.js",
                    abs_src_path=str(ir.files(__package__).joinpath("tablesort.js")),
                    inclusion=InclusionLevel.NOT_IN_NAV,
                )
            )
            files.append(
                File.generated(
                    config,
                    "assets/javascripts/tablesort.min.js",
                    abs_src_path=str(Plugin._TABLESORT_FILE.absolute()),
                    inclusion=InclusionLevel.NOT_IN_NAV,
                )
            )
        return files

    def _add_admonition(self, config: MkDocsConfig) -> None:
        if "admonition" not in config.markdown_extensions:
            config.markdown_extensions.append("admonition")
        config.extra_css.append("assets/stylesheets/kny/admonition_idea.css")
        if config.theme["icon"] is None:
            config.theme["icon"] = {}
        config.theme["icon"].setdefault("admonition", {}).setdefault("idea", "material/lightbulb-on")

    def _add_mathjax(self, config: MkDocsConfig) -> None:
        Plugin._CACHE_DIR.mkdir(parents=True, exist_ok=True)

        url: str = "https://github.com/mathjax/MathJax/archive/refs/heads/master.zip"
        suffix: str = "master"
        if self.config.mathjax != "latest":
            url = f"https://github.com/mathjax/MathJax/archive/refs/tags/{self.config.mathjax}.zip"
            suffix = self.config.mathjax
        logging.getLogger("mkdocs.plugins.kny_common").info("Downloading mathjax: %s", self.config.mathjax)
        mathjax_zip: Path = Plugin._CACHE_DIR.joinpath("mathjax.zip")
        try:
            urllib.request.urlretrieve(url, mathjax_zip)
            with zipfile.ZipFile(mathjax_zip, "r") as reader:
                reader.extractall(Plugin._CACHE_DIR)
            shutil.rmtree(Plugin._MATHJAX_DIR, True)
            Plugin._CACHE_DIR.joinpath(f"MathJax-{suffix}").rename(Plugin._MATHJAX_DIR)
        except urllib.error.URLError:
            # ignore download fails if one version is already there (to not block offline building)
            if not Plugin._MATHJAX_DIR.exists():
                raise
            logging.getLogger("mkdocs.plugins.kny_common").warning("Downloading mathjax failed, will use cached one")

        Plugin._CACHE_DIR.joinpath("mathjax.zip").unlink(True)

        if "pymdownx.arithmatex" not in config.markdown_extensions:
            config.markdown_extensions.append("pymdownx.arithmatex")
        config.mdx_configs.setdefault("pymdownx.arithmatex", {})["generic"] = True
        config.extra_javascript.append("assets/javascripts/kny/mathjax.js")
        config.extra_javascript.append("assets/javascripts/mathjax/tex-mml-chtml.js")

    def _add_tablesort(self, config: MkDocsConfig) -> None:
        Plugin._CACHE_DIR.mkdir(parents=True, exist_ok=True)

        url: str = "https://raw.githubusercontent.com/tristen/tablesort/master/dist/tablesort.min.js"
        if self.config.tablesort != "latest":
            url = f"https://raw.githubusercontent.com/tristen/tablesort/refs/tags/{self.config.tablesort}/tablesort.min.js"
        logging.getLogger("mkdocs.plugins.kny_common").info("Downloading tablesort: %s", self.config.tablesort)
        try:
            urllib.request.urlretrieve(url, Plugin._TABLESORT_FILE)
        except urllib.error.URLError:
            # ignore download fails if one version is already there (to not block offline building)
            if not Plugin._TABLESORT_FILE.exists():
                raise
            logging.getLogger("mkdocs.plugins.kny_common").warning("Downloading tablesort failed, will use cached one")

        config.extra_javascript.append("assets/javascripts/kny/tablesort.js")
        config.extra_javascript.append("assets/javascripts/tablesort.min.js")
