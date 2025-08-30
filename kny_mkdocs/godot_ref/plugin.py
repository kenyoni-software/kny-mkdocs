import argparse
import importlib.resources as ir
import re
import shlex

from mkdocs.config.base import Config as MkConfig
from mkdocs.config.config_options import Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page


class Config(MkConfig):
    godot_url = Type(str, default="https://docs.godotengine.org/en/stable")


class Plugin(BasePlugin[Config]):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("class_name", type=str, default="", help="class name")

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        config.extra_css.append("assets/stylesheets/kny/godot_ref.css")

    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files | None:
        files.append(
            File.generated(
                config, "assets/stylesheets/kny/godot_ref.css", abs_src_path=str(ir.files(__package__).joinpath("godot_ref.css"))
            )
        )
        return files

    def on_page_markdown(self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        def replace(match: re.Match):
            args: argparse.Namespace = self.parser.parse_args(shlex.split(match.groups()[0]))
            return f'<a class="kny-godot-ref" href="{self.config.godot_url}/classes/class_{args.class_name.lower()}.html">{args.class_name}</a>'

        return re.sub(r"{{\skny:godot\s(.*?)\s}}", replace, markdown, flags=re.I | re.M)
