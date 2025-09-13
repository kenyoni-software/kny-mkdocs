import argparse
import re
import shlex

from mkdocs.config.base import Config as MkConfig
from mkdocs.config.config_options import Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


class Config(MkConfig):
    source_url = Type(str, default="")


class Plugin(BasePlugin[Config]):
    def __init__(self) -> None:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        self.parser.add_argument("path", type=str, default="", help="source path")
        self.parser.add_argument("text", nargs="?", type=str, default="", help="text")

    def on_page_markdown(self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        def replace(match: re.Match[str]) -> str:
            args: argparse.Namespace = self.parser.parse_args(shlex.split(match.groups()[0]))
            return f"[{args.path if args.text == '' else args.text}]({self.config.source_url}{args.path})"

        return re.sub(r"{{\skny:source\s(.*?)\s}}", replace, markdown, flags=re.I | re.M)
