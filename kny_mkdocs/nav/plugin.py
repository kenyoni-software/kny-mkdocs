import html
import importlib.resources as ir
import re

from mkdocs.config.base import Config as MkConfig
from mkdocs.config.config_options import Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files, InclusionLevel
from mkdocs.structure.pages import Page


class Config(MkConfig):
    theme = Type(str, default="classic")
    delimiter = Type(str, default="❯")


class Plugin(BasePlugin[Config]):
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        if self.config.theme not in {"classic", "modern"}:
            raise ValueError(f"Unsupported kny_nav theme: {self.config.theme}")
        config.extra_css.append(f"assets/stylesheets/kny/nav-{self.config.theme}.css")

    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files | None:
        files.append(
            File.generated(
                config,
                f"assets/stylesheets/kny/nav-{self.config.theme}.css",
                abs_src_path=str(ir.files(__package__).joinpath(f"nav-{self.config.theme}.css")),
                inclusion=InclusionLevel.NOT_IN_NAV,
            )
        )
        return files

    def on_page_markdown(self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        def render(items: list[str]) -> str:
            rendered: list[str] = []
            for item in items:
                active = item.startswith("*")
                label = item[1:].lstrip() if active else item
                active_class = " kny-nav__item--active" if active else ""
                rendered.append(f'<span class="kny-nav__item{active_class}">{html.escape(label)}</span>')
            seperator = '<span class="kny-nav__sep"></span>'
            if self.config.theme == "classic":
                seperator = f'<span class="kny-nav__sep">{html.escape(self.config.delimiter)}</span>'
            return f'<span class="kny-nav">{seperator.join(rendered)}</span>'

        def replace_brackets(match: re.Match[str]) -> str:
            items = [item.strip() for item in match.group(1).split("/")]
            return render([item for item in items if item])

        return re.sub(r"\[\[\s*(.*?)\s*\]\]", replace_brackets, markdown, flags=re.MULTILINE)
