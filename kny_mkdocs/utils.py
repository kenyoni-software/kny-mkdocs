from importlib.abc import Traversable
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files, File


def add_files_recursive(directory: Traversable, output: Path, files: Files, config: MkDocsConfig) -> None:
    dirs: set = {directory}
    while dirs:
        dire: Traversable = dirs.pop()
        for path in dire.iterdir():
            if path.is_dir():
                dirs.add(path)
            if path.is_file():
                files.append(File.generated(config, str(output.joinpath(str(path).removeprefix(str(directory) + "/"))), abs_src_path=str(path)))
