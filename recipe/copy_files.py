import os, sys, shutil
from pathlib import Path

SRC = Path(os.environ["SRC_DIR"])
OUT = Path(os.environ["PREFIX"]) / "share" / "hunspell_dictionaries"

OUT.mkdir(exist_ok=True, parents=True)

PKG = os.environ["PKG_NAME"]
L10N = PKG.split("-")[-1].upper()
PATH = next(SRC.glob(f"en_{L10N}*"))

for glob in ["*.aff", "*.dic", "README*"]:
    for path in PATH.glob(glob):
        shutil.copy2(path, OUT / path.name)
        if path.name.startswith("README"):
            shutil.copy2(path, SRC / path.name)


print(sorted(OUT.glob("*")))
