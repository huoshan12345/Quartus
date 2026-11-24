# Assignment 2 - Part A (lecture-based redesign)

Open `assignment2.qpf` in Quartus Prime Lite 20.1. Select a component using
**Project > Revisions**, and open the matching BDF from **File > Open**.
If an older version is already open in the schematic editor, close that tab
without saving its old contents and reopen the file from disk.

| Revision / BDF | Implementation |
| --- | --- |
| counter16 | 16 DFFs, 16 four-input MUXes, shared priority encoder, NOT/XOR/AND increment logic |
| counter12 | 12 DFFs, 12 four-input MUXes, shared priority encoder, NOT/XOR/AND increment logic |
| register8 | 8 two-input MUXes and 8 DFFs |
| register16 | 16 two-input MUXes and 16 DFFs |
| bus16_mux8 | 16 eight-input MUXes, with three common selection lines |

## Design level and connectivity

The component sheets directly expose the MUXes and flip-flops. No counter IP,
LPM_COUNTER, prebuilt register IP, or hidden HDL implementation is used.
The only additional design sheet is `priority_control.bdf`, which contains
the shared counter control encoder built from NOT, AND, and OR gates.

The elementary MUX functions are Quartus's `21mux`, `mux41`, and `81mux`.
Their graphics have been arranged as trapezoidal MUX symbols. Their functional
pin names and elementary library implementations remain unchanged. In 21mux, S=1 selects A (DIN) and S=0 selects B (feedback Q). The BUS
uses the non-inverting Y output; complementary WN outputs are unused. INH and
GN enable inputs are explicitly tied to ground as required by those MUXes.

Main signal paths, feedback paths, clock, selection lines, and carry chains
have continuous wires. Thick lines are buses; labeled scalar branches select
individual bus members, such as DIN[0] from DIN[15..0]. Wires crossing without
a junction dot are separate signals. Dots mark connected scalar branches.

The `.bsf` symbols for all five components are included for reuse in Part B.
Keep the BDF/BSF files together. The top-level component symbols are appropriate
for the full datapath, while their BDFs show how the components are designed.

## Counter behavior

All operations occur on the rising edge of CLK. CLR is synchronous.

| CLR | LD | INC | S1 S0 | Selected input / operation |
| --- | --- | --- | --- | --- |
| 1 | X | X | 00 | D0 = 0 / clear |
| 0 | 1 | X | 01 | D1 = DIN / load |
| 0 | 0 | 1 | 10 | D2 = incremented value |
| 0 | 0 | 0 | 11 | D3 = Q / hold |

The shared encoder implements:

```
S1 = NOT CLR AND NOT LD
S0 = NOT CLR AND (LD OR NOT INC)
```

For bit 0 the incremented value is NOT Q[0]. For bit i > 0 it is
Q[i] XOR (Q[i-1] AND ... AND Q[0]). The AND chain computes that carry from
the current stored bits. Every DFF uses the same clock; this is not a ripple
clock design. Overflow wraps modulo 2^width.

This follows PDF page 18 of `Review of Digital Logic_Notes.pdf` (the printed
footer on that particular page reads 2). The gate implementation of the
encoder is provided so the control behavior is visible and editable.

## Register and BUS behavior

Registers follow PDF page 13 of the annotated digital logic notes. Each bit
has a feedback/load MUX followed by a DFF. LD=0 holds Q; LD=1 loads DIN at
the next rising edge. No clock gating and no reset port are used. Load a known
value before relying on register contents in simulation.

The BUS extends the MUX-per-bit structure on PDF page 9 of
`Basic Computer Organization and Design Part2_Notes.pdf` to 8 inputs and
16 output bits. SEL[2..0] = k selects Dk[15..0], for all k from 0 through 7.
All 16 MUXes share SEL[0] -> A, SEL[1] -> B, SEL[2] -> C. It is combinational.

## Checks and previews

- All five revisions pass native Quartus Analysis & Elaboration with zero
  errors and zero warnings. Reports are in `output_files`.
- `tools/verify_schematics.py` reads the actual BDF connection labels and
  recursively evaluates the encoder, gates, MUXes, and DFFs. Its 5,080 test
  cases cover all counter control combinations, holding without an edge,
  carry propagation, overflow, consecutive increments, register load/hold,
  and every BUS selector/input bit. Results: `verification/logic_checks.txt`.
- `previews` contains drawings rendered from the BDF objects for layout review.
  `*_detail.png` shows the upper portion at a readable scale. These are not
  Quartus screenshots or simulation waveforms.

Register MUX correction: register8 and register16 have also passed real ModelSim tests of their compiled VHDL gate netlists (28 and 44 load/hold cases respectively). The log is verification/modelsim_mux_fix/native_register_check.log. These checks include every input bit, zero, the maximum value, and DIN changes while LD=0. Older screenshots from before the correction are obsolete.

For the other components, verification remains functional Boolean checking and native elaboration, not ModelSim
waveform simulation, fitting, timing analysis, or hardware validation. The
assignment's testbench screenshots remain to be produced.

The target device is the locally installed Cyclone V `5CGXFC7C7F23C8`, used
for compilation checks. No board pin assignments or timing constraints are
included. Change the device if the course specifies a board.

## Reproduction

Run from this project directory:

```powershell
python tools/build_schematics.py
python tools/verify_schematics.py
python tools/render_previews.py
./tools/check_project.ps1
```

The builder reads primitive graphics from `C:\intelFPGA_lite\20.1`; it
overwrites generated schematic and project files, so retain manual edits
before rerunning it. The preview renderer requires Pillow. The native check
runs revisions sequentially because they share a Quartus database.

The previous design was archived in `backup/before_redesign_*.zip` before
replacement. Its obsolete bit-cell and nested MUX helper files were removed
from the active project.

Part B: select revision datapath and open datapath.bdf. See DATAPATH_README.md for the complete data/control interface and validation status.
