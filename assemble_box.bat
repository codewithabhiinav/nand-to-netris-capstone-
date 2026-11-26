@echo off
python PartB\assembler.py PartC\Box.asm
if errorlevel 1 exit /b 1
echo Box.hack generated successfully.
