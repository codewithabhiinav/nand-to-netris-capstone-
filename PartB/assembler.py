#!/usr/bin/env python3
"""Two-pass Hack assembler with the K=50 duplicate-label warning feature."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

PREDEFINED_SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    **{f"R{i}": i for i in range(16)},
    "SCREEN": 16384,
    "KBD": 24576,
}

# Seven-bit Hack comp field (a c1 c2 c3 c4 c5 c6).
COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "A+D": "0000010",
    "D-A": "0010011", "A-D": "0000111",
    "D+M": "1000010", "M+D": "1000010",
    "D-M": "1010011", "M-D": "1000111",
    "D&A": "0000000", "A&D": "0000000",
    "D&M": "1000000", "M&D": "1000000",
    "D|A": "0010101", "A|D": "0010101",
    "D|M": "1010101", "M|D": "1010101",
}
JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")
LABEL_RE = re.compile(r"^\(([A-Za-z_.$:][A-Za-z0-9_.$:]*)\)$")


class AssemblyError(ValueError):
    """Raised for invalid Hack assembly, with the source line included."""


def _clean_source_line(raw: str) -> str:
    return raw.split("//", 1)[0].strip()


def _line_error(path: Path, line_number: int, message: str) -> AssemblyError:
    return AssemblyError(f"{path.name}:{line_number}: {message}")


def _parse_c_instruction(compact: str, path: Path, line_number: int) -> str:
    if compact.count("=") > 1 or compact.count(";") > 1:
        raise _line_error(path, line_number, f"invalid C-instruction: {compact}")
    if ";" in compact:
        before_jump, jump = compact.split(";", 1)
    else:
        before_jump, jump = compact, ""
    if "=" in before_jump:
        dest, comp = before_jump.split("=", 1)
    else:
        dest, comp = "", before_jump

    if not comp:
        raise _line_error(path, line_number, "missing comp field")
    if any(ch not in "ADM" for ch in dest) or len(set(dest)) != len(dest):
        raise _line_error(path, line_number, f"invalid destination: {dest!r}")
    if comp not in COMP_TABLE:
        raise _line_error(path, line_number, f"unknown comp mnemonic: {comp!r}")
    if jump not in JUMP_TABLE:
        raise _line_error(path, line_number, f"unknown jump mnemonic: {jump!r}")

    # Destination bit order is A, D, M, independent of input spelling (e.g. MD/DM).
    dest_bits = "".join("1" if register in dest else "0" for register in "ADM")
    return "111" + COMP_TABLE[comp] + dest_bits + JUMP_TABLE[jump]


def assemble_text(source: str, source_name: str = "<string>") -> tuple[list[str], dict[str, int], list[str]]:
    """Assemble source text. Returns (machine_words, symbol_table, warnings)."""
    path = Path(source_name)
    symbol_table = dict(PREDEFINED_SYMBOLS)
    source_instructions: list[tuple[int, str]] = []
    labels_defined: dict[str, int] = {}
    warnings: list[str] = []
    rom_address = 0

    # Pass 1: collect label addresses and report duplicate labels (K=50 feature).
    for line_number, raw in enumerate(source.splitlines(), start=1):
        line = _clean_source_line(raw)
        if not line:
            continue
        compact = "".join(line.split())
        if compact.startswith("(") or compact.endswith(")"):
            match = LABEL_RE.fullmatch(compact)
            if not match:
                raise _line_error(path, line_number, f"malformed label declaration: {line!r}")
            label = match.group(1)
            if label in symbol_table:
                first_line = labels_defined.get(label)
                if first_line is None:
                    warning = (f"Warning: {path.name}:{line_number}: label {label!r} conflicts with "
                               f"a predefined symbol; keeping the predefined symbol")
                else:
                    warning = (f"Warning: {path.name}:{line_number}: duplicate label {label!r}; "
                               f"first declared on line {first_line}; keeping the first definition")
                warnings.append(warning)
            else:
                symbol_table[label] = rom_address
                labels_defined[label] = line_number
            continue
        if rom_address > 32767:
            raise _line_error(path, line_number, "program exceeds the 32K ROM address space")
        source_instructions.append((line_number, compact))
        rom_address += 1

    # Pass 2: translate instructions and allocate variables from RAM[16].
    next_variable_address = 16
    machine_words: list[str] = []
    for line_number, instruction in source_instructions:
        if instruction.startswith("@"):
            symbol_or_number = instruction[1:]
            if not symbol_or_number:
                raise _line_error(path, line_number, "empty A-instruction")
            if symbol_or_number.isdecimal():
                address = int(symbol_or_number, 10)
            else:
                if not SYMBOL_RE.fullmatch(symbol_or_number):
                    raise _line_error(path, line_number, f"invalid symbol: {symbol_or_number!r}")
                if symbol_or_number not in symbol_table:
                    if next_variable_address > 32767:
                        raise _line_error(path, line_number, "variable allocation exceeds address 32767")
                    symbol_table[symbol_or_number] = next_variable_address
                    next_variable_address += 1
                address = symbol_table[symbol_or_number]
            if not 0 <= address <= 32767:
                raise _line_error(path, line_number, f"A-instruction address out of range: {address}")
            machine_words.append(f"{address:016b}")
        else:
            machine_words.append(_parse_c_instruction(instruction, path, line_number))

    return machine_words, symbol_table, warnings


def assemble_file(input_path: str | Path, output_path: str | Path | None = None,
                  symbols_path: str | Path | None = None) -> tuple[Path, list[str]]:
    source_file = Path(input_path)
    if not source_file.is_file():
        raise FileNotFoundError(f"Assembly file not found: {source_file}")
    words, symbols, warnings = assemble_text(source_file.read_text(encoding="utf-8"), str(source_file))
    destination = Path(output_path) if output_path else source_file.with_suffix(".hack")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(words) + "\n", encoding="ascii")
    if symbols_path:
        symbol_file = Path(symbols_path)
        symbol_file.parent.mkdir(parents=True, exist_ok=True)
        symbol_file.write_text(
            "\n".join(f"{name}: {address}" for name, address in sorted(symbols.items(), key=lambda item: (item[1], item[0]))) + "\n",
            encoding="utf-8",
        )
    return destination, warnings


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Two-pass Hack assembler (K=50 duplicate-label warning)")
    parser.add_argument("input", help="input .asm file")
    parser.add_argument("-o", "--output", help="output .hack path (default: same name as input)")
    parser.add_argument("--symbols", help="optionally export the resolved symbol table")
    args = parser.parse_args(argv)
    try:
        output, warnings = assemble_file(args.input, args.output, args.symbols)
    except (AssemblyError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    for warning in warnings:
        print(warning, file=sys.stderr)
    print(f"Assembled successfully: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
