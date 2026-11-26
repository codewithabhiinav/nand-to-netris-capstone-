import tempfile
import unittest
from pathlib import Path

from PartB.assembler import assemble_file
from tests.hack_emulator import HackEmulator, SCREEN

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOX_ASM = PROJECT_ROOT / "PartC" / "Box.asm"


class BoxProgramTests(unittest.TestCase):
    def _load_box(self, keyboard: int) -> HackEmulator:
        with tempfile.TemporaryDirectory() as temp_dir:
            generated = Path(temp_dir) / "Box.hack"
            assemble_file(BOX_ASM, generated)
            return HackEmulator.from_hack_file(generated, keyboard=keyboard)

    def test_key_pressed_draws_48_by_20_box_at_row_50(self):
        cpu = self._load_box(keyboard=1)
        cpu.run(25000)
        base = SCREEN + 32 * 50
        for row in range(20):
            row_base = base + 32 * row
            self.assertEqual([cpu.screen_word(row_base + col) for col in range(3)], [0xFFFF] * 3)
            self.assertEqual(cpu.screen_word(row_base + 3), 0)
        self.assertEqual(cpu.screen_word(base - 1), 0)

    def test_key_release_clears_box(self):
        cpu = self._load_box(keyboard=1)
        cpu.run(25000)
        cpu.set_keyboard(0)
        cpu.run(25000)
        base = SCREEN + 32 * 50
        for row in range(20):
            row_base = base + 32 * row
            self.assertEqual([cpu.screen_word(row_base + col) for col in range(3)], [0, 0, 0])


if __name__ == "__main__":
    unittest.main()
