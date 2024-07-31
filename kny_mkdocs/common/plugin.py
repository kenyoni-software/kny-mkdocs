from mkdocs.config.base import Config as MkConfig
from mkdocs.config.config_options import Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files, File

admonition_idea_css: str = """/*
Icon is set in mkdocs.yml: theme -> name -> icon -> admonition -> idea
 */
.md-typeset .admonition.idea,
.md-typeset details.idea {
    border-color: rgb(200, 200, 0);
}
.md-typeset .idea > .admonition-title,
.md-typeset .idea > summary {
    background-color: rgb(200, 200, 0, 0.1);
}
.md-typeset .idea > .admonition-title::before,
.md-typeset .idea > summary::before {
    background-color: rgb(200, 200, 0);
    -webkit-mask-image: var(--md-admonition-icon--idea);
    mask-image: var(--md-admonition-icon--idea);
}
"""


class Config(MkConfig):
    admonition_idea = Type(bool, default=False)


class Plugin(BasePlugin[Config]):
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        if self.config.admonition_idea:
            config.extra_css.append("assets/stylesheets/kny/admonition_idea.css")

    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files | None:
        if self.config.admonition_idea:
            files.append(File.generated(config, "assets/stylesheets/kny/admonition_idea.css", content=admonition_idea_css))
        return files
