import importlib.resources as ir

from bs4 import BeautifulSoup, ResultSet
from mkdocs.config.base import Config as MkConfig
from mkdocs.config.config_options import Type, ListOfItems
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page
import material.templates


class Config(MkConfig):
    icon = Type(str, default="material/open-in-new")
    exclude = ListOfItems(Type(str), default=[])


class Plugin(BasePlugin[Config]):
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        config.extra_css.append("assets/stylesheets/kny/external_link_icon.css")

    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files | None:
        files.append(File.generated(config, "assets/stylesheets/kny/external_link_icon.css",
                     abs_src_path=str(ir.files(__package__).joinpath("external_link_icon.css"))))
        return files

    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        icon: str = ir.files(material.templates.__package__).joinpath(
            ".icons").joinpath(self.config.icon+".svg").read_text()

        link: ResultSet = []
        for link in soup.find_all("a"):
            url: str = link.get("href", "")
            if not _url_excluded(url, self.config.exclude) and (url.startswith("http") or url.startswith("https")):
                link.append(BeautifulSoup(
                    f'<span class="kny-external-link-icon">{icon}</span>', "html.parser"))

        return str(soup)


def _url_excluded(url: str, exclude: list[str]) -> bool:
    for pattern in exclude:
        if url.startswith(pattern):
            return True
    return False
