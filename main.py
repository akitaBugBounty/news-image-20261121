#!/usr/bin/env python3
"""news-image-20261121 entrypoint (make.fun, program/v1).

Copies the pre-rendered front page ``entry.png`` that ships in this
repository to ``$MAKEFUN_OUTPUT_DIR/entry.png`` (default ``/output``).

Standard library only, no network, no randomness: every run writes the
same bytes.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
NAME = "entry.png"


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: {SOURCE} not found next to main.py", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # copyfile copies bytes only (no metadata), so the output is
    # byte-identical on every run, as the competition requires.
    shutil.copyfile(SOURCE, out_dir / NAME)
    return 0


if __name__ == "__main__":
    sys.exit(main())
