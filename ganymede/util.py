import importlib
import pathlib


## Import every file in this module
def import_submodules(file, name):
    for entry in pathlib.Path(file).parent.iterdir():
        if entry.name.startswith("_"):
            continue

        if entry.suffix == ".py" or (entry / "__init__.py").is_file():
            importlib.import_module(f".{entry.stem}", name)
