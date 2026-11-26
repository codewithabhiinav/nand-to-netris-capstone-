"""Compare two Hack machine-code files line-by-line."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys


def read_words(path: Path) -> list[str]:
    words = [line.strip() for line in path.read_text(encoding='ascii').splitlines() if line.strip()]
    for index, word in enumerate(words, start=1):
        if len(word) != 16 or set(word) - {'0', '1'}:
            raise ValueError(f'{path}:{index}: expected exactly 16 binary digits')
    return words


def main() -> int:
    parser = argparse.ArgumentParser(description='Compare generated .hack files with the official assembler output')
    parser.add_argument('generated', type=Path, help='file created by PartB/assembler.py')
    parser.add_argument('official', type=Path, help='file created by the official Nand2Tetris assembler')
    args = parser.parse_args()
    try:
        generated = read_words(args.generated)
        official = read_words(args.official)
    except (OSError, ValueError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2
    if generated == official:
        print(f'PASS: files are identical ({len(generated)} instructions).')
        return 0
    limit = min(len(generated), len(official))
    for index in range(limit):
        if generated[index] != official[index]:
            print(f'FAIL: first difference at instruction line {index + 1}')
            print(f'  generated: {generated[index]}')
            print(f'  official:  {official[index]}')
            break
    if len(generated) != len(official):
        print(f'Line count differs: generated={len(generated)}, official={len(official)}')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
