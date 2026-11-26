# Part C - Personalised Box Program

`Box.asm` is configured for roll number **2501350050** (K=50): row 50, 20 rows tall and 48 pixels wide. It polls KBD, writes `0xFFFF` across three words per row while a key is pressed, and writes zero to those words after key release.

Rebuild the machine code from the project root:

```bash
python PartB/assembler.py PartC/Box.asm
```

This overwrites `Box.hack` with the assembler's output. Load that `.hack` file in the official CPU Emulator and capture the required screenshots.
