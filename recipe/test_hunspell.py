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

LOCALES = os.environ.get(
    "CF_EN_LOCALES",
    PKG.replace("aoo-mozilla-en-dict-", "").upper().replace("OXENDICT", "oxendict"),
).split()


def test_locale_found(a_locale: str) -> None:
    """Verify whether the dictionary is found."""
    l10n_dict = OUT / a_locale

    l10n_paths = [OUT / f"{a_locale}.{ext}" for ext in EXTS]

    for path in l10n_paths:
        print(f"Checking if {path} exists...")
        assert path.exists()

    print(f"\n\t... checking if the {a_locale} dictionary is detected...")
    res = run(["hunspell", "-D"], stderr=PIPE, stdout=PIPE, encoding="utf-8")
    _dump_result(res)
    out = res.stderr.strip().splitlines()
    assert str(l10n_dict) in out, out


@pytest.fixture(params=LOCALES)
def a_locale(request: pytest.FixtureRequest) -> str:
    return f"en_{request.param}"


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("test", "test"),
        ("mispellled", ""),
    ],
)
def test_locale_spelling(a_locale: str, word: str, expected: str) -> None:
    args = ["hunspell", "-G", "-d", a_locale]
    print(f"""\n\t... checking if {a_locale} return '{expected}' for '{word}':""")
    res = run(args, input=word, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    _dump_result(res)
    out = res.stdout.strip()
    assert out == expected, out


def _dump_result(res: CompletedProcess[str]) -> None:
    print("\targs:\n", "\t".join(res.args))
    print("\tstdout:\n", indent(res.stdout, "\t\t"))
    print("\tstderr:\n", indent(res.stderr, "\t\t"))
    print("\trc:", res.returncode)


if __name__ == "__main__":
    sys.exit(pytest.main(PYTEST_ARGS))
