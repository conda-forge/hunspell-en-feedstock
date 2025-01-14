import os
import shutil
import sys
from pathlib import Path

SRC = Path(os.environ["SRC_DIR"])
OUT = Path(os.environ["PREFIX"]) / "share" / "hunspell_dictionaries"

PKG = os.environ["PKG_NAME"]

INSTALL = {
    "aoo-mozilla-en-dict-au": ["en_AU.aff", "en_AU.dic"],
    "aoo-mozilla-en-dict-ca": ["en_CA.aff", "en_CA.dic"],
    "aoo-mozilla-en-dict-gb": ["en_GB.aff", "en_GB.dic"],
    "aoo-mozilla-en-dict-us": ["en_US.aff", "en_US.dic"],
    "aoo-mozilla-en-dict-za": ["en_ZA.aff", "en_ZA.dic"],
}

def copy_verbose(src, dst):
    print(f"Copying {src} to {dst}")
    shutil.copy2(src, dst)

def copy_files():
    OUT.mkdir(exist_ok=True, parents=True)

    for path in INSTALL[PKG]:
        copy_verbose(SRC / path, OUT / path)

        # Older versions of en_GB installed as en-GB
        if PKG == "aoo-mozilla-en-dict-gb":
            copy_verbose(SRC / path, OUT / path.replace("_", "-"))


    return 0


if __name__ == "__main__":
    sys.exit(copy_files())
