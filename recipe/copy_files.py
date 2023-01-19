import os, shutil
from pathlib import Path

SRC = Path(os.environ["SRC_DIR"])
OUT = Path(os.environ["PREFIX"]) / "share/hunspell_dictionaries"

OUT.mkdir(exist_ok=True, parents=True)

PKG = os.environ["PKG_NAME"]
L10N = PKG.split("-")[-1].upper()
PATH = next(SRC.glob(f"en_{L10N}*"))

print("Copying files to", OUT)

for glob in ["*.aff", "*.dic"]:
    for path in sorted(PATH.glob(glob)):
        print("...", path.name)
        shutil.copy2(path, OUT / path.name)
