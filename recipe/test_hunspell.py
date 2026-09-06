import os
import sys

from pathlib import Path
from subprocess import run, PIPE, CompletedProcess
from textwrap import indent

import pytest

PYTEST_ARGS = [__file__, "-s", "-vv", "--color=yes"]

PKG = os.environ["PKG_NAME"]
OUT = Path(os.environ["PREFIX"]) / "share/hunspell_dictionaries"
EXTS = {"dic", "aff"}

LOCALES = os.environ.get("CF_EN_LOCALES", "").split()

if not LOCALES:
    L10N = PKG.replace("aoo-mozilla-en-dict-", "").split("-")
    LOCALES = ["en_" + ("-".join([L10N[0].upper(), *L10N[1:]]))]

MISSPELLED_SUFFIX_LOCALES = {
    "ize": ["en_AU", "en_GB", "en-GB", "en_ZA"],
    "ise": ["en_GB-oxendict", "en_US"],
}


def test_locale_found(a_locale: str) -> None:
    """Verify whether the dictionary is found."""
    l10n_dict = OUT / a_locale

    l10n_paths = [OUT / f"{a_locale}.{ext}" for ext in EXTS]

    for path in l10n_paths:
        print(f"\n\t... checking if {path} exists...")
        assert path.exists()

    print(f"\n\t... checking if the {a_locale} dictionary is detected...")
    res = run(["hunspell", "-D"], stderr=PIPE, stdout=PIPE, encoding="utf-8")
    _dump_result(res)
    out = res.stderr.strip().splitlines()
    assert str(l10n_dict) in out, out


@pytest.fixture(params=LOCALES)
def a_locale(request: pytest.FixtureRequest) -> str:
    return f"{request.param}"


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("test", "test"),
        ("mispellled", ""),
        ("parameterise", "parameterise"),
        ("parameterize", "parameterize"),
    ],
)
def test_locale_spelling(a_locale: str, word: str, expected: str) -> None:
    for suffix, suffix_locales in MISSPELLED_SUFFIX_LOCALES.items():
        if word.endswith(suffix) and a_locale in suffix_locales:
            print(f"\n\t+++ -{suffix} should not be acceped with {a_locale}")
            expected = ""
            break

    args = ["hunspell", "-G", "-d", a_locale]
    print(f"""\n\t... checking if {a_locale} returns '{expected}' for '{word}':""")
    res = run(args, input=word, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    _dump_result(res)
    out = res.stdout.strip()
    assert out == expected, out


def _dump_result(res: CompletedProcess[str]) -> None:
    print("\targs:\n\t\t", "\t".join(res.args))
    print("\tstdout:\n", indent(res.stdout or "<EMPTY>", "\t\t"))
    print("\tstderr:\n", indent(res.stderr or "<EMPTY>", "\t\t"))
    print("\trc:", res.returncode)


if __name__ == "__main__":
    print(f"""
{"=" * 80}
        testing {PKG} with:
            locales:
                {LOCALES}
            pytest args:
                {PYTEST_ARGS}
{"=" * 80}
    """)
    sys.exit(pytest.main(PYTEST_ARGS))
