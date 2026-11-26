"""Small instruction-level Hack CPU emulator for deterministic Part B/C tests.

It models the 16-bit Hack instruction set and enough RAM-mapped I/O for the
capstone Box.asm test. It is not a replacement for the official CPU Emulator.
"""
from __future__ import annotations

from pathlib import Path

MASK = 0xFFFF
ROM_SIZE = 32768
RAM_SIZE = 32768
SCREEN = 16384
KBD = 24576


class HackEmulator:
    def __init__(self, machine_code: list[str], keyboard: int = 0):
        self.rom = [int(word, 2) for word in machine_code]
        self.ram = [0] * RAM_SIZE
        self.ram[KBD] = keyboard & MASK
        self.a = 0
        self.d = 0
        self.pc = 0
        self.cycles = 0

    @classmethod
    def from_hack_file(cls, path: str | Path, keyboard: int = 0) -> "HackEmulator":
        words = [line.strip() for line in Path(path).read_text(encoding="ascii").splitlines() if line.strip()]
        if any(len(word) != 16 or set(word) - {"0", "1"} for word in words):
            raise ValueError("Invalid .hack file: each non-empty line must be 16 binary digits")
        return cls(words, keyboard=keyboard)

    def set_keyboard(self, value: int) -> None:
        self.ram[KBD] = value & MASK

    def step(self) -> None:
        if not 0 <= self.pc < len(self.rom):
            raise RuntimeError(f"PC {self.pc} is outside loaded ROM (size {len(self.rom)})")
        instruction = self.rom[self.pc]
        self.cycles += 1

        # A-instruction: 0vvvvvvvvvvvvvvv
        if (instruction & 0x8000) == 0:
            self.a = instruction & 0x7FFF
            self.pc = (self.pc + 1) & 0x7FFF
            return

        # C-instruction: 111 a cccccc ddd jjj
        if (instruction & 0xE000) != 0xE000:
            raise RuntimeError(f"Unsupported instruction {instruction:016b} at ROM[{self.pc}]")

        old_a = self.a & 0x7FFF
        a_bit = (instruction >> 12) & 1
        comp = (instruction >> 6) & 0x3F
        dest = (instruction >> 3) & 0x7
        jump = instruction & 0x7

        x = self.d & MASK
        y = (self.ram[old_a] if a_bit else self.a) & MASK
        zx = (comp >> 5) & 1
        nx = (comp >> 4) & 1
        zy = (comp >> 3) & 1
        ny = (comp >> 2) & 1
        f = (comp >> 1) & 1
        no = comp & 1

        if zx: x = 0
        if nx: x = (~x) & MASK
        if zy: y = 0
        if ny: y = (~y) & MASK
        out = ((x + y) if f else (x & y)) & MASK
        if no: out = (~out) & MASK

        # M destination uses the pre-instruction A register address.
        if dest & 0b001 and old_a != KBD:
            self.ram[old_a] = out
        if dest & 0b010:
            self.d = out
        if dest & 0b100:
            self.a = out

        signed = out if out < 0x8000 else out - 0x10000
        jump_taken = (
            (jump & 0b001 and signed > 0) or
            (jump & 0b010 and signed == 0) or
            (jump & 0b100 and signed < 0)
        )
        self.pc = old_a if jump_taken else ((self.pc + 1) & 0x7FFF)

    def run(self, cycles: int) -> None:
        for _ in range(cycles):
            self.step()

    def screen_word(self, address: int) -> int:
        if not SCREEN <= address < KBD:
            raise ValueError("Address is outside the screen memory map")
        return self.ram[address]
