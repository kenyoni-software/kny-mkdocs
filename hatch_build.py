import shutil
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        tablesort_min_js: Path = Path(self.directory).joinpath("tablesort.min.js")
        if not tablesort_min_js.exists():
            self.app.display_info("downloading tablesort.min.js")
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/tristen/tablesort/master/dist/tablesort.min.js",
                tablesort_min_js
            )
        build_data["force_include"][str(tablesort_min_js)] = "kny_mkdocs/common/tablesort.min.js"

        mathjax_zip: Path = Path(self.directory).joinpath("mathjax.zip")
        if not mathjax_zip.exists():
            self.app.display_info("downloading mathjax")
            urllib.request.urlretrieve(
                "https://github.com/mathjax/MathJax/archive/refs/heads/master.zip",
                mathjax_zip
            )
        mathjax_dir: Path = Path(self.directory).joinpath("mathjax")
        if not mathjax_dir.exists():
            with zipfile.ZipFile(mathjax_zip, "r") as reader:
                reader.extractall(self.directory)
            Path(self.directory).joinpath("MathJax-master", "es5").rename(mathjax_dir)
        build_data["force_include"][str(mathjax_dir)] = "kny_mkdocs/common/mathjax"

    def clean(self, versions: list[str]) -> None:
        Path(self.directory).joinpath("tablesort.min.js").unlink(True)
        Path(self.directory).joinpath("mathjax.zip").unlink(True)
        shutil.rmtree(Path(self.directory).joinpath("MathJax-master"), True)
        shutil.rmtree(Path(self.directory).joinpath("mathjax"), True)
