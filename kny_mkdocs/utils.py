from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files, InclusionLevel


def add_files_recursive(
    directory: Path, output: Path, files: Files, config: MkDocsConfig, exclude_suffixes: list[str] | None = None
) -> None:
    if exclude_suffixes is None:
        exclude_suffixes = []
    dirs: set[Path] = {directory}
    while dirs:
        dir: Path = dirs.pop()
        for path in dir.iterdir():
            if path.is_dir():
                dirs.add(path)
            if path.is_file() and "".join(path.suffixes) not in exclude_suffixes:
                files.append(
                    File.generated(
                        config,
                        str(output.joinpath(str(path).removeprefix(str(directory) + "/"))),
                        abs_src_path=str(path),
                        inclusion=InclusionLevel.NOT_IN_NAV,
                    )
                )
