import argparse
import importlib.resources as ir
import re
import shlex
from typing import cast

from mkdocs.config.base import Config as MkConfig
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page


_DEFAULT_BACKGROUND: str = "var(--md-accent-fg-color--transparent)"
_DEFAULT_TEXT_COLOR: str = "var(--md-typeset-a-color)"


def _get_relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate the WCAG relative luminance of an RGB color."""
    linear: list[float] = []
    for channel in rgb:
        # normalize channel to 0.0 - 1.0
        s_rgb: float = channel / 255.0
        
        # convert sRGB to linear RGB (De-gamma filtering)
        if s_rgb <= 0.04045:
            linear.append(s_rgb / 12.92)
        else:
            linear.append(((s_rgb + 0.055) / 1.055) ** 2.4)
            
    # apply standard WCAG coefficients for human eye spectral sensitivity
    r: float
    g: float
    b: float
    r, g, b = linear
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _get_contrast_ratio(lum1: float, lum2: float) -> float:
    """Calculate the contrast ratio between two relative luminances."""
    l1: float = max(lum1, lum2)
    l2: float = min(lum1, lum2)
    return (l1 + 0.05) / (l2 + 0.05)


def _get_contrast_color(bg_str: str) -> str:
    """Parse hex or names and returns high-contrast text (#000000 or #ffffff) or default text color."""
    if bg_str == _DEFAULT_BACKGROUND or bg_str is None:
        return _DEFAULT_TEXT_COLOR

    bg_lower: str = bg_str.lower().strip()
    
    color_map: dict[str, tuple[int, int, int]] = {
        "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0),
        "green": (0, 128, 0), "lime": (0, 255, 0), "blue": (0, 0, 255),
        "yellow": (255, 255, 0), "cyan": (0, 255, 255), "magenta": (255, 0, 255),
        "silver": (192, 192, 192), "gray": (128, 128, 128), "maroon": (128, 0, 0),
        "purple": (128, 0, 128), "olive": (128, 128, 0), "navy": (0, 0, 128),
        "teal": (0, 128, 128)
    }
    bg_rgb: tuple[int, int, int] = (255, 255, 255) 

    if bg_lower in color_map:
        bg_rgb = color_map[bg_lower]
    elif bg_lower.startswith("#"):
        hex_val: str = bg_lower.lstrip("#")
        if len(hex_val) == 3:
            hex_val = "".join(c * 2 for c in hex_val)
        try:
            bg_rgb = (int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16))
        except ValueError:
            pass
            
    bg_luminance: float = _get_relative_luminance(bg_rgb)
    contrast_with_white: float = _get_contrast_ratio(bg_luminance, 1.0)
    contrast_with_black: float = _get_contrast_ratio(bg_luminance, 0.0)
    
    return "#000000" if contrast_with_black > contrast_with_white else "#ffffff"


def _badge_attrs_str(text: str, bg: str) -> str:
    attrs: dict[str, list[str]] = {"class": [], "style": []}

    if text:
        is_icon: bool = text.startswith(":") and text.endswith(":")
        attrs["class"].append("mdx-badge__icon" if is_icon else "mdx-badge__text")
    
    if bg != _DEFAULT_BACKGROUND and bg is not None:
        attrs["style"].append("box-shadow: none;")

    if bg != "":
        contrast_color: str = _get_contrast_color(bg)

        attrs["style"].append(f"background: {bg};")
        attrs["style"].append(f"color: {contrast_color};")

    return "".join(f' {key}="{" ".join(val)}"' for key, val in attrs.items() if val)


def _badge_html(args: argparse.Namespace) -> str:
    has_left: bool = args.left_text != "" or args.left_bg is not None
    has_right: bool = args.right_text != "" or args.right_bg is not None
    left_attrs: str = _badge_attrs_str(args.left_text, args.left_bg)
    right_attrs: str = _badge_attrs_str(args.right_text, args.right_bg)

    return "".join(
        [
            '<span class="mdx-badge">',
            f'<span {left_attrs}>{args.left_text}</span>' if has_left else "",
            f'<span {right_attrs}>{args.right_text}</span>' if has_right else "",
            "</span>",
        ]
    )


class Config(MkConfig):
    pass


class Plugin(BasePlugin[Config]):
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        sub_parser = self.parser.add_subparsers(dest="command", parser_class=argparse.ArgumentParser)
        parser = sub_parser.add_parser("badge", help="badge")
        parser.add_argument("left_text", type=str, default="", help="left text of the badge")
        parser.add_argument("right_text", nargs="?", type=str, default="", help="right text of the badge")
        parser.add_argument("--left-bg", nargs="?", action="store", type=str, default=None, help="left background color")
        parser.add_argument("--right-bg", nargs="?", action="store", type=str, default=None, help="left background color")

        parser: argparse.ArgumentParser = sub_parser.add_parser("badge-version", help="experimental badge")
        parser.add_argument("right_text", type=str, default="", help="right text of the badge")
        parser.add_argument("--left-bg", nargs="?", action="store", type=str, default=None, help="left background color")
        parser.add_argument("--right-bg", nargs="?", action="store", type=str, default=None, help="left background color")

        parser = sub_parser.add_parser("badge-experimental", help="experimental badge")
        parser.add_argument("right_text", type=str, default="", help="right text of the badge")
        parser.add_argument("--left-bg", nargs="?", action="store", type=str, default=None, help="left background color")
        parser.add_argument("--right-bg", nargs="?", action="store", type=str, default=None, help="left background color")

        parser = sub_parser.add_parser("badge-download", help="download badge")
        parser.add_argument("right_text", type=str, default="", help="right text of the badge")
        parser.add_argument("--left-bg", nargs="?", action="store", type=str, default=None, help="left background color")
        parser.add_argument("--right-bg", nargs="?", action="store", type=str, default=None, help="left background color")

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        config.extra_css.append("assets/stylesheets/kny/badge.css")

    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files | None:
        files.append(
            File.generated(config, "assets/stylesheets/kny/badge.css", abs_src_path=str(ir.files(__package__).joinpath("badge.css")))
        )
        return files

    def on_page_markdown(self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        def replace(match: re.Match[str]) -> str:
            args: argparse.Namespace = self.parser.parse_args(shlex.split(match.groups()[0]))
            match cast(str, args.command):
                case "badge-version":
                    args.left_text = ":material-tag-outline:"
                    if args.left_bg is None:
                        args.left_bg = _DEFAULT_BACKGROUND
                    return _badge_html(args)
                case "badge-experimental":
                    args.left_text = ":material-tag-outline:"
                    if args.left_bg is None:
                        args.left_bg = _DEFAULT_BACKGROUND
                    return _badge_html(args)
                case "badge-download":
                    args.left_text = ":material-tag-outline:"
                    if args.left_bg is None:
                        args.left_bg = _DEFAULT_BACKGROUND
                    return _badge_html(args)
                case "badge":
                    return _badge_html(args)
                case _:
                    pass
            return ""

        return re.sub(r"{{\skny:((?:badge|badge-download|badge-experimental|badge-version).*?)\s}}", replace, markdown, flags=re.I | re.M)
