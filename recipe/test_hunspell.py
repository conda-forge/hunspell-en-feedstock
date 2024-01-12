import os
import pprint
import subprocess
import sys
from pathlib import Path

from pytest import fixture, main

PYTEST_ARGS = ["-s", "-vv", "--color=yes", __file__]

OUT = Path(os.environ["PREFIX"]) / "share/hunspell_dictionaries"

PKG = os.environ["PKG_NAME"]
L10N = PKG.split("-")[-1].upper()
HUNSPELL_ARGS = ["hunspell", "-G"]
EXTS = ["dic", "aff"]

L10N_SEPARATOR = {
    "AU": "_",
    "CA": "_",
    "GB": "-",
    "US": "_",
    "ZA": "_",
}

LOCALES = [f"en{sep}{l10n}" for l10n, sep in L10N_SEPARATOR.items()]

if L10N != "EN":
    LOCALES = [f"en{L10N_SEPARATOR[L10N]}{L10N}"]


def test_locale_found(a_locale: str):
    l10n_dict = OUT / a_locale

    l10n_paths = [OUT / f"{a_locale}.{ext}" for ext in EXTS]

    for path in l10n_paths:
        print(f"Checking if {path} exists...")
        assert path.exists()

    print(f"Checking if the {a_locale} dictionary is detected...")
    p = subprocess.Popen(["hunspell", "-D"], stderr=subprocess.PIPE)
    out, err = p.communicate()
    dicts = err.decode("utf-8")

    pprint.pprint(dicts)

    assert str(l10n_dict) in dicts


def test_correct_spelling(a_locale: str):
    hunspell("test", "test", a_locale)


def test_not_correct_spelling(a_locale: str):
    hunspell("mispellled", "", a_locale)


@fixture(params=LOCALES)
def a_locale(request) -> str:
    return request.param


def hunspell(word: str, expected: str, locale: str):
    args = HUNSPELL_ARGS + ["-d", locale]
    print(f"Checking if the output of `{args}` for `{word}` is `{expected}`...")
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate(word.encode("utf-8"))
    assert out.decode("utf-8").strip() == expected, out


if __name__ == "__main__":
    sys.exit(main(PYTEST_ARGS))
