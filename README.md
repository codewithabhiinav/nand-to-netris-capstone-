# Nand to Tetris Capstone - Make the Computer Draw a Box

**Student:** Abhinav Kumar  
**Roll number:** 2501350050  
**Course:** Full Stack Development (FSD), Semester 3  
**Course project:** Nand to Tetris - I (ETCCNT301)

This folder implements the supplied two-page capstone brief. The personal value is **K = 50** (last two digits of the roll number).

## Personalised assignment values

| Requirement | Calculation | Required value |
|---|---|---:|
| Personal number | last two digits of 2501350050 | `K = 50` |
| Starting row | `K` | `50` |
| Height | fixed by assignment | `20 rows` |
| Width | `16 × ((K mod 4) + 1)` = `16 × 3` | `48 pixels` |
| Assembler extra feature | `K mod 3 = 2` | warn on duplicate labels |

## Folder layout

```text
capstone/
├── PartA/
│   ├── CPU.hdl
│   ├── Memory.hdl
│   └── Computer.hdl
├── PartB/
│   └── assembler.py
├── PartC/
│   ├── Box.asm
│   └── Box.hack
├── tests/
│   ├── hack_emulator.py
│   ├── test_assembler.py
│   └── test_box_program.py
├── evidence/
│   └── README.md
├── STUDENT_REPORT.pdf
└── SUBMISSION_CHECKLIST.md
```

## Requirements

- Python 3.10 or newer (the assembler and automated tests use only the Python standard library).
- Nand2Tetris Software Suite for the official Hardware Simulator and CPU Emulator.
- The official course test files: `CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, and `ComputerRect.tst`, plus the matching `.cmp` and `.hack` files supplied with the suite.

## Part A - run the HDL chips

1. Open `PartA/CPU.hdl` in the Nand2Tetris Hardware Simulator and load the official `CPU.tst`.
2. Repeat with `PartA/Memory.hdl` and `Memory.tst`.
3. Open `PartA/Computer.hdl` and run `ComputerAdd.tst`, `ComputerMax.tst`, and `ComputerRect.tst`.
4. Save a screenshot of each successful comparison in `evidence/`.

The project uses the standard built-in `ARegister`, `DRegister`, `ALU`, `PC`, `RAM16K`, `Screen`, `Keyboard`, `ROM32K` and standard logic/multiplexer chips. The assignment permits built-in chips when an earlier lab chip is unavailable; this use is documented here.

## Part B - run your Python assembler

From this folder:

```bash
python PartB/assembler.py PartC/Box.asm
```

This creates `PartC/Box.hack`. To optionally export the resolved symbols:

```bash
python PartB/assembler.py PartC/Box.asm --symbols PartC/symbols-debug.txt
```

The default assembler implements the required K=50 extra feature: if a label is declared more than once, it prints a warning with the duplicate line number and retains the first definition. It does not silently overwrite the original label address.

The assembler is a two-pass implementation: pass 1 resolves label ROM addresses, and pass 2 translates A/C instructions and allocates variables starting at RAM address 16.

Also run the assembler on the course test programs `Add.asm`, `Max.asm`, `Rect.asm` and `Pong.asm` (from the Nand2Tetris course files). Compare each generated `.hack` file with the official assembler output using `python tests/compare_hack_files.py generated.hack official.hack`; capture the comparison evidence for the report.

## Part C - run the box program

1. Assemble `PartC/Box.asm` using the Python assembler above.
2. Open the official **CPU Emulator** (not the Hardware Simulator) and load `PartC/Box.hack` using its program-load command.
3. Open the Screen view and run the program. Hold/press any key: a black rectangle should appear at row 50, left edge, width 48 pixels and height 20 rows. Release the key: the rectangle should clear.
4. Capture screenshots from the official CPU Emulator and save them as `evidence/box_cpu_emulator.png` and `evidence/box_cleared_cpu_emulator.png`.

The first display word is at `SCREEN + 32*50 = 16384 + 1600 = 17984`. Each row uses three consecutive 16-bit words, then skips 29 more words so that the next row begins 32 words later. Exactly 20 rows are drawn.

## Automated checks

Run:

```bash
python -m unittest discover -s tests -v
```

The tests verify the assembler's instruction encodings, symbol/variable handling, duplicate-label warning and the Box program's behaviour in a small instruction-level Hack CPU emulator. These tests do **not** replace the five official Hardware Simulator tests or the required official CPU Emulator screenshot.

## Important submission note

`STUDENT_REPORT.pdf` is a report draft. The code and local automated checks are complete, but the official hardware-simulator screenshots and official CPU-emulator screenshot must be captured on the machine running the Nand2Tetris suite before final submission. Do not represent the evidence checklist as completed until those screenshots exist.
