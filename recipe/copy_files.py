import os
import shutil
import sys
from pathlib import Path

SRC = Path(os.environ["SRC_DIR"])
OUT = Path(os.environ["PREFIX"]) / "share/hunspell_dictionaries"

PKG = os.environ["PKG_NAME"]
L10N = PKG.split("-")[-1].upper()
PATH = next(SRC.glob(f"en_{L10N}*"))
GLOBS = ["*.aff", "*.dic"]


def copy_files():
    if not PATH.exists():
        print(PATH, "does not exist")
        return 1

    print("Copying files to", OUT)

    all_files = sorted(sum([[*PATH.glob(glob)] for glob in GLOBS], []))

    if not all_files:
        return 1

    OUT.mkdir(exist_ok=True, parents=True)

    for path in all_files:
        print("...", path.name)
        shutil.copy2(path, OUT / path.name)

    return 0


if __name__ == "__main__":
    sys.exit(copy_files())
