import os
import shutil
import sys
from pathlib import Path

SRC = Path(os.environ["SRC_DIR"])
OUT = Path(os.environ["PREFIX"]) / "share/hunspell_dictionaries"

PKG = os.environ["PKG_NAME"]
L10N = PKG.split("-")[-1].upper()
PATH = sorted(SRC.glob(f"en_{L10N}*"))[0]
GLOBS = ["*.aff", "*.dic"]


def copy_files():
    if not PATH.exists():
        print(PATH, "does not exist")
        return 1

    print("\n".join(sorted(map(str, PATH.glob("*")))))

    print("Copying files to", OUT)

    dict_files = sorted(sum([[*PATH.glob(glob)] for glob in GLOBS], []))

    if not dict_files:
        PATH.glob("*")
        return 1

    OUT.mkdir(exist_ok=True, parents=True)

    for path in dict_files:
        print("...", path.name)
        shutil.copy2(path, OUT / path.name)

    return 0


if __name__ == "__main__":
    sys.exit(copy_files())
