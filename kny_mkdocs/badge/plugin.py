import argparse
import re
import shlex

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page

badge_css: str = """.md-typeset .mdx-badge {
    font-size: .85em
}

.md-typeset .mdx-badge__icon {
    color: var(--md-typeset-a-color);
    box-shadow: inset 0 0 0.0rem 0.05rem var(--md-accent-fg-color);
    padding: 0.2rem;
}

.md-typeset .mdx-badge__icon:first-child {
    border-bottom-left-radius: 0.2rem;
    border-top-left-radius: 0.2rem;
}

.md-typeset .mdx-badge__icon:last-child {
    border-bottom-right-radius: 0.2em;
    border-top-right-radius: 0.2rem;
}

.md-typeset .mdx-badge__text {
    color: var(--md-typeset-a-color);
    box-shadow: inset 0 0 0.0rem 1px var(--md-accent-fg-color);
    padding: 0.2rem 0.3rem;
}

.md-typeset .mdx-badge__text:first-child {
    border-bottom-left-radius: 0.2rem;
    border-top-left-radius: 0.2rem;
}

.md-typeset .mdx-badge__text:last-child {
    border-bottom-right-radius: 0.2rem;
    border-top-right-radius: 0.2rem;
}

.kny-badge-bg {
    background: var(--md-accent-fg-color--transparent);
}
"""


def _badge_html(args: argparse.Namespace):
    left_classes: str = f"mdx-badge__icon" if args.left_text[0] == ":" and args.left_text[-1] == ":" else "mdx-badge__text"
    if args.left_bg:
        left_classes += " kny-badge-bg"
    right_classes: str = f"mdx-badge__icon" if len(args.right_text) > 2 and args.right_text[0] == ":" and args.right_text[
        -1] == ":" else "mdx-badge__text"
    if args.right_bg:
        right_classes += " kny-badge-bg"
    return "".join([
        f'<span class="mdx-badge">',
        f'<span class="{left_classes}">{args.left_text}</span>' if args.left_text else "",
        f'<span class="{right_classes}">{args.right_text}</span>' if args.right_text else "",
        f"</span>",
    ])


class Plugin(BasePlugin):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        sub_parser = self.parser.add_subparsers(dest="command", parser_class=argparse.ArgumentParser)
        parser = sub_parser.add_parser("badge", help="badge")
        parser.add_argument("left_text", type=str, default="", help="left text of the badge")
        parser.add_argument("right_text", nargs='?', type=str, default="", help="right text of the badge")
        parser.add_argument("--left-bg", action="store_true", default=False, help="left background color")
        parser.add_argument("--right-bg", action="store_true", default=False, help="left background color")

        parser: argparse.ArgumentParser = sub_parser.add_parser("badge-version", help="experimental badge")
        parser.add_argument("right_text", type=str, default="", help="right text of the badge")
        parser.add_argument("--right-bg", action="store_true", default=False, help="left background color")

        parser = sub_parser.add_parser("badge-experimental", help="experimental badge")
        parser.add_argument("right_text", type=str, default="", help="right text of the badge")
        parser.add_argument("--right-bg", action="store_true", default=False, help="left background color")

        parser = sub_parser.add_parser("badge-download", help="download badge")
        parser.add_argument("right_text", type=str, default="", help="right text of the badge")
        parser.add_argument("--right-bg", action="store_true", default=False, help="left background color")

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        config.extra_css.append("assets/stylesheets/kny/badge.css")

    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files | None:
        files.append(File.generated(config, "assets/stylesheets/kny/badge.css", content=badge_css))
        return files

    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        def replace(match: re.Match):
            args: argparse.Namespace = self.parser.parse_args(shlex.split(match.groups()[0]))
            match args.command:
                case "badge-version":
                    args.left_text = ":material-tag-outline:"
                    args.left_bg = True
                    return _badge_html(args)
                case "badge-experimental":
                    args.left_text = ":material-tag-outline:"
                    args.left_bg = True
                    return _badge_html(args)
                case "badge-download":
                    args.left_text = ":material-tag-outline:"
                    args.left_bg = True
                    return _badge_html(args)
                case "badge":
                    return _badge_html(args)

        return re.sub(r"{{\skny:((?:badge|badge-download|badge-experimental|badge-version).*?)\s}}", replace, markdown,
                      flags=re.I | re.M)
