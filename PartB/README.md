# Part B - Python Hack Assembler

Run from the project root:

```bash
python PartB/assembler.py PartC/Box.asm
```

The output is `PartC/Box.hack`. The required personal extension for K=50 is enabled: duplicate label declarations print a warning with filename and line number, and the assembler retains the first label address.

The assembler implements two passes, predefined symbols, labels, variables from RAM[16], all Hack comp mnemonics, destination combinations and jump mnemonics. It reports malformed instructions with source line numbers and rejects A-instruction addresses outside 0-32767.

For the assignment's official parity check, assemble `Add.asm`, `Max.asm`, `Rect.asm` and `Pong.asm` from the course files and compare the resulting `.hack` files with the official assembler output. The course sample assembly sources are not bundled in this ZIP. Use `tests/compare_hack_files.py` to compare the generated and official `.hack` files line-for-line.
