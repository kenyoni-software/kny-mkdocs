import importlib.resources as ir
from pathlib import Path

from mkdocs.config.base import Config as MkConfig
from mkdocs.config.config_options import Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files, File

import kny_mkdocs.utils as utils


class Config(MkConfig):
    admonition_idea = Type(bool, default=False)
    mathjax = Type(bool, default=False)
    tablesort = Type(bool, default=False)


class Plugin(BasePlugin[Config]):
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        if self.config.admonition_idea:
            if "admonition" not in config.markdown_extensions:
                config.markdown_extensions.append("admonition")
            config.extra_css.append("assets/stylesheets/kny/admonition_idea.css")
            if config.theme["icon"] is None:
                config.theme["icon"] = {}
            config.theme["icon"].setdefault("admonition", {}).setdefault("idea", "material/lightbulb-on")
        if self.config.mathjax:
            if "pymdownx.arithmatex" not in config.markdown_extensions:
                config.markdown_extensions.append("pymdownx.arithmatex")
            config.mdx_configs.setdefault("pymdownx.arithmatex", {})["generic"] = True
            config.extra_javascript.append("assets/javascripts/kny/mathjax.js")
            config.extra_javascript.append("assets/javascripts/mathjax/tex-mml-chtml.js")
        if self.config.tablesort:
            config.extra_javascript.append("assets/javascripts/kny/tablesort.js")
            config.extra_javascript.append("assets/javascripts/tablesort.min.js")

    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files | None:
        if self.config.admonition_idea:
            files.append(
                File.generated(config, "assets/stylesheets/kny/admonition_idea.css", abs_src_path=str(ir.files(__package__).joinpath("admonition_idea.css"))))
        if self.config.mathjax:
            files.append(File.generated(config, "assets/javascripts/kny/mathjax.js", abs_src_path=str(ir.files(__package__).joinpath("mathjax.js"))))
            utils.add_files_recursive(ir.files(__package__).joinpath("mathjax"), Path("assets/javascripts/mathjax/"), files, config)
        if self.config.tablesort:
            files.append(File.generated(config, "assets/javascripts/kny/tablesort.js", abs_src_path=str(ir.files(__package__).joinpath("tablesort.js"))))
            files.append(File.generated(config, "assets/javascripts/tablesort.min.js", abs_src_path=str(ir.files(__package__).joinpath("tablesort.min.js"))))
        return files
