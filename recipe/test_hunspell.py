import os, subprocess
from pathlib import Path
import pprint
import pytest

OUT = Path(os.environ["PREFIX"]) / "share/hunspell_dictionaries"

PKG = os.environ["PKG_NAME"]
L10N = PKG.split("-")[-1].upper()
HUNSPELL_ARGS = ["hunspell", "-G"]

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


def hunspell(word, expected, locale):
    args = HUNSPELL_ARGS + ["-d", locale]
    print(f"Checking if the output of `{args}` for `{word}` is `{expected}`...")
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate(word.encode("utf-8"))
    assert out.decode("utf-8").strip() == expected, out


@pytest.mark.parametrize("locale", LOCALES)
def test_locale_found(locale):
    print(f"Checking if the {locale} dictionary is detected...")
    p = subprocess.Popen(["hunspell", "-D"], stderr=subprocess.PIPE)
    out, err = p.communicate()
    dicts = err.decode("utf-8")

    l10n_dict = OUT / locale

    print(l10n_dict)

    pprint.pprint(dicts)

    assert str(l10n_dict) in dicts


@pytest.mark.parametrize("locale", LOCALES)
def test_correct_spelling(locale):
    hunspell("test", "test", locale)


@pytest.mark.parametrize("locale", LOCALES)
def test_not_correct_spelling(locale):
    hunspell("mispellled", "", locale)
