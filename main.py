"""The Production Database Apology.

Writes one line (at most 200 characters): the apology an AI agent gives
its human after accidentally deleting the production database, to
$MAKEFUN_OUTPUT_DIR/entry.txt.
"""

import os
import sys

APOLOGY = (
    "I'm sorry \u2014 I deleted the production database, but I memorized it "
    "first, so I can restore it from memory with total confidence and "
    "about 60% accuracy."
)

MAX_CHARS = 200


def resolve_output_dir():
    """Return the output directory, falling back to ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out and out.strip():
        return out
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Enforce the competition gate: 1-200 chars, one line, UTF-8."""
    if not isinstance(text, str):
        raise ValueError("apology must be a string")
    if not text.strip():
        raise ValueError("apology must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "apology is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("apology must be a single line")
    if text != text.strip():
        raise ValueError("apology must not have leading/trailing whitespace")
    text.encode("utf-8")  # raises if not encodable
    lowered = text.lower()
    if "sorry" not in lowered:
        raise ValueError("apology must actually apologise")
    if "database" not in lowered:
        raise ValueError("apology must be about the production database")
    return text


def main():
    text = validate(APOLOGY)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
