import os, sys, shutil, subprocess
from pathlib import Path

OUT = Path(os.environ["PREFIX"]) / "share" / "hunspell_dictionaries"

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

for locale in LOCALES:
    print(f"Checking if the {locale} dictionary is detected...")
    p = subprocess.Popen(["hunspell", "-D"], stderr=subprocess.PIPE)
    out, err = p.communicate()
    dicts = err.decode("utf-8")
    l10n_dict = OUT / locale
    assert str(l10n_dict) in dicts, [l10n_dict, dicts]

def hunspell(word, expected, locale):
    args = HUNSPELL_ARGS + ["-d", locale]
    print(f"Checking if the output of `{args}` for `{word}` is `{expected}`...")
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate(word.encode("utf-8"))
    assert out.decode("utf-8").strip() == expected, out

for locale in LOCALES:
    hunspell("test", "test", locale)
    hunspell("mispellled", "", locale)
