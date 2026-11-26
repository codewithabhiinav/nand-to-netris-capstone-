import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from PartB.assembler import AssemblyError, assemble_file, assemble_text


class AssemblerTests(unittest.TestCase):
    def test_a_and_c_instruction_encoding(self):
        source = """@2
@3
D=A
@0
M=D
"""
        words, _, warnings = assemble_text(source)
        self.assertEqual(words, [
            "0000000000000010",
            "0000000000000011",
            "1110110000010000",
            "0000000000000000",
            "1110001100001000",
        ])
        self.assertEqual(warnings, [])

    def test_all_comp_mnemonics_have_valid_16_bit_encoding(self):
        from PartB.assembler import COMP_TABLE
        for comp in COMP_TABLE:
            with self.subTest(comp=comp):
                words, _, _ = assemble_text(f"D={comp}\n")
                self.assertEqual(len(words[0]), 16)
                self.assertEqual(words[0][:3], "111")

    def test_previously_incorrect_comp_mappings_are_fixed(self):
        expected = {
            "!A": "0110001",
            "-A": "0110011",
            "A+1": "0110111",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
        }
        for comp, expected_bits in expected.items():
            with self.subTest(comp=comp):
                words, _, _ = assemble_text(f"D={comp}\n")
                self.assertEqual(words[0][3:10], expected_bits)

    def test_destination_order_is_independent(self):
        words1, _, _ = assemble_text("MD=D\n")
        words2, _, _ = assemble_text("DM=D\n")
        self.assertEqual(words1, words2)
        self.assertEqual(words1[0], "1110001100011000")

    def test_label_resolution_and_variable_allocation(self):
        source = """@counter
M=1
(LOOP)
@LOOP
0;JMP
"""
        words, symbols, _ = assemble_text(source)
        self.assertEqual(symbols["counter"], 16)
        self.assertEqual(symbols["LOOP"], 2)
        self.assertEqual(words[0], "0000000000010000")
        self.assertEqual(words[2], "0000000000000010")

    def test_duplicate_label_warning_keeps_first_definition(self):
        source = """@FIRST
0;JMP
(FIRST)
@FIRST
0;JMP
(FIRST)
@FIRST
"""
        words, symbols, warnings = assemble_text(source, "Duplicate.asm")
        self.assertEqual(symbols["FIRST"], 2)
        self.assertEqual(len(warnings), 1)
        self.assertIn("duplicate label 'FIRST'", warnings[0])
        self.assertIn(":6:", warnings[0])
        self.assertEqual(words[-1], "0000000000000010")

    def test_predefined_symbol_label_collision_warns(self):
        _, symbols, warnings = assemble_text("(R0)\n@R0\n", "Collision.asm")
        self.assertEqual(symbols["R0"], 0)
        self.assertEqual(len(warnings), 1)
        self.assertIn("predefined symbol", warnings[0])

    def test_invalid_comp_is_reported_with_line_number(self):
        with self.assertRaisesRegex(AssemblyError, r"Bad.asm:2: unknown comp"):
            assemble_text("@0\nD=Q\n", "Bad.asm")

    def test_out_of_range_a_instruction_is_rejected(self):
        with self.assertRaisesRegex(AssemblyError, "out of range"):
            assemble_text("@32768\n")

    def test_output_file_is_written(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            asm = Path(temp_dir) / "Sample.asm"
            asm.write_text("@1\nD=A\n", encoding="utf-8")
            output, warnings = assemble_file(asm)
            self.assertTrue(output.exists())
            self.assertEqual(output.read_text().splitlines(), [
                "0000000000000001", "1110110000010000"
            ])
            self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()
