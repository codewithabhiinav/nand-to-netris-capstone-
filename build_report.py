from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, HRFlowable, Flowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'STUDENT_REPORT.pdf'
PAGE_W, PAGE_H = A4
NAVY = colors.HexColor('#12243A')
BLUE = colors.HexColor('#176B87')
TEAL = colors.HexColor('#2A9D8F')
PALE = colors.HexColor('#EAF3F6')
LIGHT = colors.HexColor('#F4F7FA')
MID = colors.HexColor('#526273')
RED = colors.HexColor('#B54747')
GOLD = colors.HexColor('#9C6B14')
GREEN = colors.HexColor('#26734D')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle2', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=NAVY, alignment=TA_CENTER, spaceAfter=7))
styles.add(ParagraphStyle(name='CoverSub', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=16, textColor=MID, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=NAVY, spaceBefore=2, spaceAfter=8))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=BLUE, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontName='Helvetica', fontSize=9, leading=13, textColor=NAVY, spaceAfter=5))
styles.add(ParagraphStyle(name='Smallx', parent=styles['BodyText'], fontName='Helvetica', fontSize=7.7, leading=10.5, textColor=MID, spaceAfter=3))
styles.add(ParagraphStyle(name='Cellx', parent=styles['BodyText'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=NAVY))
styles.add(ParagraphStyle(name='CellBoldx', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=NAVY))
styles.add(ParagraphStyle(name='Calloutx', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=NAVY))
styles.add(ParagraphStyle(name='CenterSmall', parent=styles['BodyText'], fontName='Helvetica', fontSize=8, leading=11, alignment=TA_CENTER, textColor=MID))

P = lambda text, style='Bodyx': Paragraph(text, styles[style])

def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor('#D8E1E8'))
        canvas.setLineWidth(0.5)
        canvas.line(18*mm, PAGE_H-15*mm, PAGE_W-18*mm, PAGE_H-15*mm)
        canvas.setFont('Helvetica-Bold', 7.5)
        canvas.setFillColor(NAVY)
        canvas.drawString(18*mm, PAGE_H-11.5*mm, 'NAND TO TETRIS - CAPSTONE PROJECT')
        canvas.setFont('Helvetica', 7.5)
        canvas.setFillColor(MID)
        canvas.drawRightString(PAGE_W-18*mm, PAGE_H-11.5*mm, 'Abhinav Kumar | 2501350050')
    canvas.setStrokeColor(colors.HexColor('#D8E1E8'))
    canvas.line(18*mm, 13*mm, PAGE_W-18*mm, 13*mm)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MID)
    canvas.drawString(18*mm, 8.5*mm, 'FSD - Semester 3 | ETCCNT301')
    canvas.drawRightString(PAGE_W-18*mm, 8.5*mm, f'Page {doc.page} of 4')
    canvas.restoreState()

class BoxDiagram(Flowable):
    def __init__(self, width=165*mm, height=38*mm):
        super().__init__(); self.width=width; self.height=height
    def draw(self):
        c=self.canv
        x0=18*mm; y0=7*mm
        c.setFillColor(PALE); c.setStrokeColor(BLUE); c.roundRect(x0, y0, 44*mm, 22*mm, 3*mm, fill=1, stroke=1)
        c.setFillColor(NAVY); c.setFont('Helvetica-Bold',8); c.drawCentredString(x0+22*mm,y0+13*mm,'ROM32K')
        c.setFont('Helvetica',7); c.drawCentredString(x0+22*mm,y0+7*mm,'instructions')
        x1=73*mm
        c.setFillColor(colors.HexColor('#E8F3EF')); c.setStrokeColor(TEAL); c.roundRect(x1,y0,44*mm,22*mm,3*mm,fill=1,stroke=1)
        c.setFillColor(NAVY); c.setFont('Helvetica-Bold',8); c.drawCentredString(x1+22*mm,y0+13*mm,'CPU')
        c.setFont('Helvetica',7); c.drawCentredString(x1+22*mm,y0+7*mm,'A, D, ALU, PC')
        x2=128*mm
        c.setFillColor(colors.HexColor('#FFF4E5')); c.setStrokeColor(colors.HexColor('#C48A32')); c.roundRect(x2,y0,40*mm,22*mm,3*mm,fill=1,stroke=1)
        c.setFillColor(NAVY); c.setFont('Helvetica-Bold',8); c.drawCentredString(x2+20*mm,y0+13*mm,'Memory')
        c.setFont('Helvetica',7); c.drawCentredString(x2+20*mm,y0+7*mm,'RAM / Screen / KBD')
        c.setStrokeColor(MID); c.setLineWidth(1)
        c.line(x0+44*mm,y0+11*mm,x1,y0+11*mm); c.line(x1+44*mm,y0+11*mm,x2,y0+11*mm)
        c.line(x1+22*mm,y0+22*mm,x1+22*mm,y0+29*mm); c.line(x1+22*mm,y0+29*mm,x0+22*mm,y0+29*mm)
        c.line(x0+22*mm,y0+29*mm,x0+22*mm,y0+22*mm)
        c.setFont('Helvetica',6.8); c.setFillColor(MID); c.drawCentredString(86*mm, y0+31*mm, 'PC address / instruction fetch')

story=[]
# PAGE 1
story += [Spacer(1, 15*mm), P('NAND TO TETRIS', 'CoverSub'), Spacer(1,3*mm), P('Capstone Project Report', 'CoverTitle2'), P('Make the Computer Draw a Box', 'CoverTitle2'), Spacer(1,4*mm), P('ETCCNT301 - Nand to Tetris I | School of Engineering & Technology', 'CoverSub'), Spacer(1,10*mm)]
student_data = [
    [P('<b>Student Name</b>','Cellx'), P('Abhinav Kumar','CellBoldx')],
    [P('<b>Roll Number</b>','Cellx'), P('2501350050','CellBoldx')],
    [P('<b>Course / Semester</b>','Cellx'), P('Full Stack Development (FSD) / Semester 3','CellBoldx')],
    [P('<b>Personal Number</b>','Cellx'), P('K = 50','CellBoldx')],
]
t=Table(student_data, colWidths=[48*mm,108*mm], rowHeights=[10*mm]*4)
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.7,colors.HexColor('#D7E1E8')),
    ('INNERGRID',(0,0),(-1,-1),0.4,colors.HexColor('#D7E1E8')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),8),
]))
story += [t, Spacer(1,10*mm), P('Project objective','H1x'), P('Build the Hack computer platform by connecting the CPU, memory system and instruction ROM; implement a two-pass Python assembler; then write a Hack assembly program that displays a black rectangle while a key is pressed and clears it when the key is released.', 'Bodyx')]
story += [P('Personalised requirements','H2x')]
req_data = [
    [P('<b>Assignment parameter</b>','Cellx'),P('<b>Calculation</b>','Cellx'),P('<b>Your required value</b>','Cellx')],
    [P('Starting row','Cellx'),P('K = 50','Cellx'),P('<b>50</b>','CellBoldx')],
    [P('Box height','Cellx'),P('Fixed by assignment','Cellx'),P('<b>20 rows</b>','CellBoldx')],
    [P('Box width','Cellx'),P('16 × ((50 mod 4) + 1) = 16 × 3','Cellx'),P('<b>48 pixels</b>','CellBoldx')],
    [P('Assembler extension','Cellx'),P('50 mod 3 = 2','Cellx'),P('<b>Warn on duplicate labels</b>','CellBoldx')],
]
t=Table(req_data, colWidths=[42*mm,72*mm,62*mm], repeatRows=1)
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),PALE),('TEXTCOLOR',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D7E1E8')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
]))
story += [t, Spacer(1,6*mm), P('<b>Scope note:</b> The report documents the supplied assignment requirements and the implementation in this project folder. Official Hardware Simulator results and CPU Emulator screenshots must be added after running the official Nand2Tetris tools.', 'Smallx'), PageBreak()]

# PAGE 2
story += [P('1. System design and Part A - Hack computer', 'H1x'), P('The top-level Computer connects instruction memory (ROM32K), the CPU and data memory. The CPU fetches an instruction using the program counter, decodes it, executes its ALU operation and updates the A/D registers, memory write output or program counter as required.', 'Bodyx'), BoxDiagram(), Spacer(1,2*mm), P('Chip responsibilities','H2x')]
parta_data=[
 [P('<b>Chip</b>','Cellx'),P('<b>Responsibility</b>','Cellx'),P('<b>Implementation detail</b>','Cellx')],
 [P('CPU.hdl','CellBoldx'),P('Executes Hack A- and C-instructions.','Cellx'),P('Decodes instruction type and destination bits; selects A/M for ALU input; evaluates signed jump conditions; controls PC and memory writes.','Cellx')],
 [P('Memory.hdl','CellBoldx'),P('Implements the Hack data-memory map.','Cellx'),P('Decodes address[13..14] and routes reads/writes to RAM16K or Screen; reads Keyboard.','Cellx')],
 [P('Computer.hdl','CellBoldx'),P('Connects ROM, CPU and Memory.','Cellx'),P('Feeds pc to ROM32K; routes CPU outM/writeM/addressM into Memory and returns inM to CPU.','Cellx')],
]
t=Table(parta_data,colWidths=[25*mm,51*mm,100*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D7E1E8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story += [t, P('Memory map','H2x')]
mem_data=[
 [P('<b>Address range</b>','Cellx'),P('<b>Mapped device</b>','Cellx'),P('<b>Use in this project</b>','Cellx')],
 [P('0 - 16383','Cellx'),P('RAM16K','CellBoldx'),P('General-purpose data and assembler variables.','Cellx')],
 [P('16384 - 24575','Cellx'),P('Screen','CellBoldx'),P('Display memory; one row is 32 words, one word is 16 pixels.','Cellx')],
 [P('24576','Cellx'),P('Keyboard','CellBoldx'),P('Non-zero value indicates a key is pressed.','Cellx')],
]
t=Table(mem_data,colWidths=[40*mm,35*mm,101*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D7E1E8')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [t, Spacer(1,3*mm), P('<b>Built-in chip note:</b> This implementation uses the permitted Nand2Tetris built-in ARegister, DRegister, ALU, PC, RAM16K, Screen, Keyboard and ROM32K chips, plus standard gates and multiplexers. These are documented dependencies rather than student-authored chips.', 'Smallx'), PageBreak()]

# PAGE 3
story += [P('2. Part B - assembler and Part C - personalised box', 'H1x'), P('Python assembler','H2x'), P('The assembler in PartB/assembler.py performs two passes. Pass 1 removes comments and blank lines and records each label at its ROM address. It detects a repeated label, prints a warning containing the source line, and retains the first definition. Pass 2 converts A-instructions to 16-bit addresses, translates C-instructions using the Hack comp/dest/jump tables, and allocates new variables from RAM address 16.', 'Bodyx')]
asm_data=[
 [P('<b>Assembler feature</b>','Cellx'),P('<b>Implementation / validation</b>','Cellx')],
 [P('A-instructions','CellBoldx'),P('Accept decimal addresses 0-32767 and predefined, label or variable symbols.','Cellx')],
 [P('C-instructions','CellBoldx'),P('Validates comp, destination and jump fields; encodes canonical 16-bit Hack words.','Cellx')],
 [P('Symbol handling','CellBoldx'),P('Predefined symbols plus labels; variables allocated sequentially from RAM[16].','Cellx')],
 [P('K=50 extra feature','CellBoldx'),P('Duplicate declarations generate a line-numbered warning; the first definition is preserved.','Cellx')],
]
t=Table(asm_data,colWidths=[41*mm,135*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D7E1E8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [t, P('Box geometry and drawing logic','H2x')]
story += [P('The personalised rectangle begins at screen row 50, uses 20 rows, and spans 48 pixels from the left edge. Since a screen row has 32 words and each word represents 16 pixels, the rectangle uses three adjacent 16-bit words on each of 20 rows.', 'Bodyx')]
geom_data=[
 [P('<b>Calculation</b>','Cellx'),P('<b>Result</b>','Cellx')],
 [P('Base address = SCREEN + (32 × 50) = 16384 + 1600','Cellx'),P('<b>17984</b>','CellBoldx')],
 [P('Words per row = 48 / 16','Cellx'),P('<b>3</b>','CellBoldx')],
 [P('Total written words = 3 × 20','Cellx'),P('<b>60</b>','CellBoldx')],
 [P('Next row stride = 32 words; after writing 3 words, skip 29','Cellx'),P('<b>32-word row spacing</b>','CellBoldx')],
]
t=Table(geom_data,colWidths=[126*mm,50*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D7E1E8')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [t, Spacer(1,3*mm), P('Program flow','H2x'), P('1. Read KBD. 2. If non-zero, set color to -1 (black); otherwise set color to 0 (clear). 3. Set the output pointer to SCREEN + 1600 and row counter to 20. 4. Write the selected color to three consecutive words. 5. Advance the pointer by 32 words, decrement the row counter and repeat. 6. Once all 20 rows are processed, return to the keyboard check.', 'Bodyx'), PageBreak()]

# PAGE 4
story += [P('3. Testing, correction record and conclusion', 'H1x'), P('Automated validation performed in the project workspace','H2x')]
results=[
 [P('<b>Check</b>','Cellx'),P('<b>Result</b>','Cellx'),P('<b>Evidence / interpretation</b>','Cellx')],
 [P('Python syntax compilation','Cellx'),P('<b>PASS</b>','CellBoldx'),P('assembler.py and test modules compile.','Cellx')],
 [P('Assembler unit tests','Cellx'),P('<b>PASS</b>','CellBoldx'),P('10 tests cover A/C encoding, exact comp mappings, labels, variables, duplicate-label warnings, error handling and output files.','Cellx')],
 [P('Box key-press simulation','Cellx'),P('<b>PASS</b>','CellBoldx'),P('Instruction-level emulator confirms 3 words per row for 20 rows beginning at SCREEN+1600.','Cellx')],
 [P('Box key-release simulation','Cellx'),P('<b>PASS</b>','CellBoldx'),P('Instruction-level emulator confirms the same 60 screen words are cleared after keyboard becomes zero.','Cellx')],
 [P('Total local automated tests','Cellx'),P('<b>12 / 12 PASS</b>','CellBoldx'),P('The local tests are useful checks but do not replace the course simulator.','Cellx')],
 [P('Official assembler parity','Cellx'),P('<b>PENDING</b>','CellBoldx'),P('Assemble Add.asm, Max.asm, Rect.asm and Pong.asm, then compare each output with the official assembler.','Cellx')],
 [P('Official HDL test suite','Cellx'),P('<b>PENDING</b>','CellBoldx'),P('CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst and ComputerRect.tst must be run in the official Hardware Simulator.','Cellx')],
 [P('Official CPU Emulator screenshot','Cellx'),P('<b>PENDING</b>','CellBoldx'),P('Capture the personalised rectangle with a key pressed and after release.','Cellx')],
]
t=Table(results,colWidths=[47*mm,31*mm,98*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D7E1E8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('TEXTCOLOR',(1,1),(1,4),GREEN),('TEXTCOLOR',(1,5),(1,5),GREEN),('TEXTCOLOR',(1,6),(1,7),GOLD)]))
story += [t, P('Mistake fixed','H2x'), P('The first uploaded version used the wrong personal value and box geometry: it treated the start row as 60 and wrote only one 16-bit word per row, which produced a 16-pixel-wide box. The corrected version uses K = 50, calculates the base as SCREEN + 32 × 50, writes three adjacent words on each row for a 48-pixel width, and repeats this for 20 rows. The original assembler also exported a symbol file instead of implementing the required K mod 3 = 2 duplicate-label warning; the corrected assembler now prints the duplicate source line and preserves the first label address.', 'Bodyx'), P('Conclusion','H2x'), P('The project source now contains the three top-level HDL chips, a two-pass Hack assembler with the personalised duplicate-label feature, and the corrected Box.asm / Box.hack program for roll number 2501350050. Local tests verify the assembler and the box behaviour in a lightweight reference emulator. Final submission still requires the five official HDL test results and genuine screenshots from the Nand2Tetris CPU Emulator.', 'Bodyx')]

# Evidence reminder box
reminder=Table([[P('<b>Before final submission</b><br/>Add screenshots for CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst, ComputerRect.tst, and the box display / cleared display from the official CPU Emulator. Replace this draft report with the updated evidence version.', 'Cellx')]], colWidths=[176*mm])
reminder.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FFF5E6')),('BOX',(0,0),(-1,-1),0.8,colors.HexColor('#D9A441')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [Spacer(1,2*mm), reminder]

doc=SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=17*mm, leftMargin=17*mm, topMargin=21*mm, bottomMargin=18*mm, title='Nand to Tetris Capstone Report - Abhinav Kumar', author='Abhinav Kumar')
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
