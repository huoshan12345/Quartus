"""Build Assignment 3 Basic Computer schematics (RAM: 2-PORT, updated datapath,
hardwired control unit, and top-level basic_computer) in Quartus BDF/BSF format."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_schematics as b
import build_datapath as d

b.ROOT = ROOT
d.ROOT = ROOT

def expand_text_rects(node):
    """Expand every (text ...) bounding box so Quartus renders full text cleanly at High-DPI."""
    import json
    if not isinstance(node, list) or not node:
        return
    if node[0] == 'text' and len(node) >= 4:
        try:
            value = json.loads(node[1])
        except Exception:
            value = str(node[1]).strip('"')
        rect = next((c for c in node if isinstance(c, list) and c and c[0] == 'rect'), None)
        font = next((c for c in node if isinstance(c, list) and c and c[0] == 'font'), None)
        size = 8
        if font:
            for c in font:
                if isinstance(c, list) and c and c[0] == 'font_size':
                    size = int(c[1])
        if rect:
            x0, y0, x1, y1 = int(rect[1]), int(rect[2]), int(rect[3]), int(rect[4])
            min_w = max(32, int(len(value) * max(11.0, size * 1.75)) + 20)
            min_h = max(20, int(size * 2.6) + 8)
            if x1 - x0 < min_w:
                rect[3] = x0 + min_w
            if y1 - y0 < min_h:
                rect[4] = y0 + min_h
        return
    for child in node:
        if isinstance(child, list):
            expand_text_rects(child)


# Load all needed Quartus logic/buffer primitives and widen their built-in text rects.
for name, folder in [
    ('and3', 'logic'), ('and4', 'logic'),
    ('or3', 'logic'), ('or4', 'logic'), ('or6', 'logic'), ('or8', 'logic'),
    ('nor2', 'logic'), ('wire', 'buffer'),
]:
    b.SYMS[name] = next(
        n for n in b.parse((b.LIB / 'primitives' / folder / (name + '.bsf')).read_text())
        if n[0] == 'symbol'
    )
for sym in b.SYMS.values():
    expand_text_rects(sym)


def box(name, w, h, inputs, outputs):
    node = ['symbol', ['rect', 0, 0, w, h], b.txt(name, 24, 0), b.txt('inst', 24, h - 16, 7)]
    for direction, ports in [('input', inputs), ('output', outputs)]:
        for pname, (x, y) in ports.items():
            if x == 0:
                end = (16, y); tx, ty = 20, y - 14
            elif x == w:
                end = (w - 16, y); tx, ty = max(20, w - 24 - int(len(pname) * 11.5)), y - 14
            elif y == 0:
                end = (x, 16); tx, ty = x + 6, 16
            else:
                end = (x, h - 16); tx, ty = x + 6, h - 32
            node.append(['port', ['pt', x, y], [direction], b.txt(pname, tx, ty), b.line((x, y), end)])
    node.append([
        'drawing',
        *[b.line(a, c) for a, c in zip(
            [(16, 16), (w - 16, 16), (w - 16, h - 16), (16, h - 16)],
            [(w - 16, 16), (w - 16, h - 16), (16, h - 16), (16, 16)],
        )],
    ])
    b.SYMS[name] = node


def save_bsf(name):
    (ROOT / (name + '.bsf')).write_text('(header "symbol" (version "1.1"))\n' + b.emit(b.SYMS[name]) + '\n')


def named(s, kind, x, y, name, nets, stub=128):
    """Place a gate/symbol and attach short clearly labeled stubs to its ports."""
    ports = s.instance(kind, x, y, 'g_' + name)
    rect = next(n for n in b.SYMS[kind] if isinstance(n, list) and n[0] == 'rect')
    w, h = int(rect[3]) - int(rect[1]), int(rect[4]) - int(rect[2])
    for pname, net in nets.items():
        a = ports[pname]
        if a[0] == x:
            end = (a[0] - stub, a[1])
            s.wire([end, a], net, '..' in net, label=True)
        elif a[0] == x + w:
            end = (a[0] + stub, a[1])
            s.wire([a, end], net, '..' in net, label=True)
        elif a[1] == y:
            end = (a[0], a[1] - 32)
            s.wire([end, a], net, '..' in net, label=True)
        else:
            end = (a[0], a[1] + 32)
            s.wire([a, end], net, '..' in net, label=True)
    return ports


def define_symbols():
    # Reuse Assignment 2 datapath component symbols.
    d.symbols()

    # RAM: 2-PORT symbol (matches ram2port.vhd and Assignment #3 Memory selection.pdf).
    box(
        'ram2port', 384, 288,
        {
            'wraddress[11..0]': (0, 64),
            'rdaddress[11..0]': (0, 96),
            'wren': (0, 144),
            'wrclock': (0, 192),
            'rdclock': (0, 224),
            'data[15..0]': (192, 288),
        },
        {'q[15..0]': (192, 0)},
    )

    # New Control Unit sub-module symbols.
    box(
        'counter4', 256, 224,
        {'CLK': (0, 64), 'CLR': (0, 96), 'LD': (0, 128), 'INC': (0, 160), 'DIN[3..0]': (128, 224)},
        {'Q[3..0]': (128, 0)},
    )
    box('dec38_en', 224, 160, {'A[2..0]': (0, 80)}, {'Y[7..0]': (224, 80)})
    box('dec416_en', 240, 192, {'A[3..0]': (0, 64), 'EN': (0, 128)}, {'Y[15..0]': (240, 96)})
    box('zero_detect16', 240, 112, {'A[15..0]': (0, 56)}, {'Z': (240, 56)})
    box(
        'bus_encoder83', 240, 256,
        {f'X{i}': (0, 32 * i) for i in range(1, 8)},
        {'SEL[2..0]': (240, 128)},
    )

    # Hierarchical symbols for top-level basic_computer.bdf.
    # Control pins are aligned to identical Y offsets on CONTROL_UNIT (right) and DATAPATH (left)
    # so every wire between them is a straight horizontal line.
    ctrl_ports = [
        'BUS_SEL[2..0]',
        'REG_LD[7..0]',
        'REG_INC[4..0]',
        'REG_CLR[4..0]',
        'ALU_OP[6..0]',
        'MEM_WRITE_EN',
        'FLAG_LD[6..0]',
        'FLAG_CLR[6..0]',
        'FLAG_DIN[4..0]',
        'E_COM',
    ]
    ctrl_y = {p: 160 + 48 * i for i, p in enumerate(ctrl_ports)}

    box(
        'control_unit', 464, 720,
        {
            'CLK': (0, 96),
            'RESET': (0, 144),
            'IR_Q[15..0]': (0, 240),
            'DR_Q[15..0]': (0, 304),
            'AC_Q[15..0]': (0, 368),
            'FLAG_Q[6..0]': (0, 432),
        },
        {
            **{p: (464, ctrl_y[p]) for p in ctrl_ports},
            'SC_Q[3..0]': (464, 656),
        },
    )

    box(
        'datapath', 496, 720,
        {
            'CLK': (0, 96),
            **{p: (0, ctrl_y[p]) for p in ctrl_ports},
            'INPUT_DATA[7..0]': (0, 656),
        },
        {
            'AC_Q[15..0]': (496, 96),
            'FLAG_Q[6..0]': (496, 160),
            'PC_Q[11..0]': (496, 224),
            'AR_Q[11..0]': (496, 288),
            'IR_Q[15..0]': (496, 352),
            'DR_Q[15..0]': (496, 416),
            'BUS_DATA[15..0]': (496, 480),
            'MEM_Q[15..0]': (496, 544),
            'OUTPUT_DATA[7..0]': (496, 608),
        },
    )


def build_counter4():
    b.build_counter(4)


def build_dec38():
    """Fully wired 3-to-8 active-high opcode decoder (A[2..0] -> Y[7..0])."""
    s = b.Sheet(
        'dec38_en',
        '3-to-8 Opcode Decoder (IR[14..12] -> D[7..0])',
        'Active-high gate-level decoder built from NOT and AND3 primitives.',
    )
    a_pin = s.pin('A[2..0]', 'input', 200, 144)
    y_pin = s.pin('Y[7..0]', 'output', 1120, 144)

    rail_bottom = 352 + 7 * 96 + 48
    s.wire([a_pin, (240, 144), (240, 272)], 'A[2..0]', True)
    s.wire([y_pin, (1120, rail_bottom)], 'Y[7..0]', True)

    # Six vertical rails: A[0], NA0, A[1], NA1, A[2], NA2
    rail_x = {}
    for bit in range(3):
        y_tap = 144 + bit * 64
        x_true = 304 + bit * 112
        x_inv = x_true + 56
        rail_x[(bit, 1)] = x_true
        rail_x[(bit, 0)] = x_inv

        inv = s.instance('not', x_true + 16, y_tap - 16, f'inv_a{bit}')
        # Connect A[bit] from bus to true rail and inverter.
        s.wire([(240, y_tap), (x_true, y_tap)], f'A[{bit}]', label=True)
        s.wire([(x_true, y_tap), inv['IN']], f'A[{bit}]')
        s.wire([(x_true, y_tap), (x_true, rail_bottom)], f'A[{bit}]')
        s.junction((x_true, y_tap))
        s.wire([inv['OUT'], (x_inv, y_tap), (x_inv, rail_bottom)], f'NA{bit}', label=True)

    # Eight AND3 minterm gates cleanly wired from the vertical rails.
    for m in range(8):
        y = 352 + m * 96
        g = s.instance('and3', 768, y, f'decode_d{m}')
        for idx, bit in enumerate([0, 1, 2]):
            val = (m >> bit) & 1
            rx = rail_x[(bit, val)]
            pt = g[f'IN{idx + 1}']
            s.wire([(rx, pt[1]), pt], f'A[{bit}]' if val else f'NA{bit}')
            s.junction((rx, pt[1]))
        s.wire([g['OUT'], (1120, g['OUT'][1])], f'Y[{m}]', label=True)
    s.save()


def build_dec416():
    """Fully wired 4-to-16 active-high timing decoder with enable (A[3..0], EN -> Y[15..0])."""
    s = b.Sheet(
        'dec416_en',
        '4-to-16 Timing Decoder with Enable (SC[3..0], EN -> T[15..0])',
        'Two-stage pre-decoded structure: H0..H3 = EN & A[3..2], L0..L3 = A[1..0], Y[4h+l] = Hh & Ll.',
    )
    a_pin = s.pin('A[3..0]', 'input', 200, 144)
    en_pin = s.pin('EN', 'input', 200, 448)
    y_pin = s.pin('Y[15..0]', 'output', 1664, 144)

    # Input bus and inverters for A[0..3].
    s.wire([a_pin, (240, 144), (240, 368)], 'A[3..0]', True)
    pre_bottom = 800
    rail_x = {}
    for bit in range(4):
        y_tap = 144 + bit * 64
        x_true = 304 + bit * 112
        x_inv = x_true + 56
        rail_x[(bit, 1)] = x_true
        rail_x[(bit, 0)] = x_inv
        inv = s.instance('not', x_true + 16, y_tap - 16, f'inv_s{bit}')
        s.wire([(240, y_tap), (x_true, y_tap)], f'A[{bit}]', label=True)
        s.wire([(x_true, y_tap), inv['IN']], f'A[{bit}]')
        s.wire([(x_true, y_tap), (x_true, pre_bottom)], f'A[{bit}]')
        s.junction((x_true, y_tap))
        s.wire([inv['OUT'], (x_inv, y_tap), (x_inv, pre_bottom)], f'NA{bit}', label=True)

    # EN vertical rail for H0..H3.
    en_x = 768
    s.wire([en_pin, (en_x, 448), (en_x, pre_bottom)], 'EN', label=True)

    # Stage 1: L0..L3 (low 2 bits) and H0..H3 (high 2 bits gated with EN).
    stage2_top = 896
    stage2_bottom = stage2_top + 15 * 72 + 48
    s.wire([y_pin, (1664, stage2_bottom)], 'Y[15..0]', True)

    l_x = {}
    h_x = {}
    for i in range(4):
        # Low pre-decode L[i] = minterm(A1, A0)
        yl = 448 + i * 80
        gl = s.instance('and2', 832, yl, f'pre_l{i}')
        for idx, bit in enumerate([0, 1]):
            val = (i >> bit) & 1
            rx = rail_x[(bit, val)]
            pt = gl[f'IN{idx + 1}']
            s.wire([(rx, pt[1]), pt], f'A[{bit}]' if val else f'NA{bit}')
            s.junction((rx, pt[1]))
        lx = 1040 + i * 32
        l_x[i] = lx
        s.wire([gl['OUT'], (lx, gl['OUT'][1]), (lx, stage2_bottom)], f'L{i}', label=True)

        # High pre-decode H[i] = EN & minterm(A3, A2)
        yh = 448 + i * 80
        gh = s.instance('and3', 1200, yh, f'pre_h{i}')
        # Tap EN, A2/NA2, A3/NA3 via neat horizontal runs above/below L gates -> put H gates below L gates!
        # Wait: rearrange vertically so H gates sit cleanly below L gates (y=448..768 for L, y=800..1120 for H)
        # so zero wires cross L gates! Let's redo Stage 1 & 2 cleanly below.

    # Rebuild sheet cleanly with L0..L3 at y=448..736 and H0..H3 at y=784..1072, Stage 2 at y=1168..2248.
    s = b.Sheet(
        'dec416_en',
        '4-to-16 Timing Decoder with Enable (SC[3..0], EN -> T[15..0])',
        'Two-stage pre-decoded structure: L0..L3 = A[1..0], H0..H3 = EN & A[3..2], Y[4h+l] = Hh & Ll.',
    )
    a_pin = s.pin('A[3..0]', 'input', 200, 144)
    en_pin = s.pin('EN', 'input', 200, 768)
    y_pin = s.pin('Y[15..0]', 'output', 1664, 144)

    s.wire([a_pin, (240, 144), (240, 368)], 'A[3..0]', True)
    pre_bottom = 1120
    rail_x = {}
    for bit in range(4):
        y_tap = 144 + bit * 64
        x_true = 304 + bit * 112
        x_inv = x_true + 56
        rail_x[(bit, 1)] = x_true
        rail_x[(bit, 0)] = x_inv
        inv = s.instance('not', x_true + 16, y_tap - 16, f'inv_s{bit}')
        s.wire([(240, y_tap), (x_true, y_tap)], f'A[{bit}]', label=True)
        s.wire([(x_true, y_tap), inv['IN']], f'A[{bit}]')
        s.wire([(x_true, y_tap), (x_true, pre_bottom)], f'A[{bit}]')
        s.junction((x_true, y_tap))
        s.wire([inv['OUT'], (x_inv, y_tap), (x_inv, pre_bottom)], f'NA{bit}', label=True)

    en_x = 768
    s.wire([en_pin, (en_x, 768), (en_x, pre_bottom)], 'EN', label=True)

    stage2_top = 1168
    stage2_bottom = stage2_top + 15 * 64 + 48
    s.wire([y_pin, (1664, stage2_bottom)], 'Y[15..0]', True)

    l_x = {}
    h_x = {}
    for i in range(4):
        yl = 448 + i * 72
        gl = s.instance('and2', 848, yl, f'pre_l{i}')
        for idx, bit in enumerate([0, 1]):
            val = (i >> bit) & 1
            rx = rail_x[(bit, val)]
            pt = gl[f'IN{idx + 1}']
            s.wire([(rx, pt[1]), pt], f'A[{bit}]' if val else f'NA{bit}')
            s.junction((rx, pt[1]))
        lx = 1008 + i * 32
        l_x[i] = lx
        s.wire([gl['OUT'], (lx, gl['OUT'][1]), (lx, stage2_bottom)], f'L{i}', label=True)

    for i in range(4):
        yh = 784 + i * 72
        gh = s.instance('and3', 848, yh, f'pre_h{i}')
        pt_en = gh['IN1']
        s.wire([(en_x, pt_en[1]), pt_en], 'EN')
        s.junction((en_x, pt_en[1]))
        for idx, bit in enumerate([2, 3]):
            val = (i >> (bit - 2)) & 1
            rx = rail_x[(bit, val)]
            pt = gh[f'IN{idx + 2}']
            s.wire([(rx, pt[1]), pt], f'A[{bit}]' if val else f'NA{bit}')
            s.junction((rx, pt[1]))
        hx = 1168 + i * 32
        h_x[i] = hx
        s.wire([gh['OUT'], (hx, gh['OUT'][1]), (hx, stage2_bottom)], f'H{i}', label=True)

    for m in range(16):
        h_idx, l_idx = m >> 2, m & 3
        ym = stage2_top + m * 64
        gm = s.instance('and2', 1360, ym, f'decode_t{m:02}')
        s.wire([(h_x[h_idx], gm['IN1'][1]), gm['IN1']], f'H{h_idx}')
        s.junction((h_x[h_idx], gm['IN1'][1]))
        s.wire([(l_x[l_idx], gm['IN2'][1]), gm['IN2']], f'L{l_idx}')
        s.junction((l_x[l_idx], gm['IN2'][1]))
        s.wire([gm['OUT'], (1664, gm['OUT'][1])], f'Y[{m}]', label=True)
    s.save()


def build_zero_detect16():
    """Fully wired 16-bit zero detector: Z = 1 iff A[15..0] == 0."""
    s = b.Sheet(
        'zero_detect16',
        '16-bit Zero Detector (Z = 1 when A[15..0] == 0)',
        'Two OR8 gates check low and high bytes; NOR2 outputs Z = 1 when all 16 bits are 0.',
    )
    a_pin = s.pin('A[15..0]', 'input', 200, 144)
    z_pin = s.pin('Z', 'output', 1024, 344)

    or_lo = s.instance('or8', 480, 144, 'nonzero_low_byte')
    or_hi = s.instance('or8', 480, 384, 'nonzero_high_byte')
    nor = s.instance('nor2', 784, 320, 'all_zero_nor')

    s.wire([a_pin, (272, 144), (272, 512)], 'A[15..0]', True)
    for bit in range(8):
        pt = or_lo[f'IN{bit + 1}']
        s.wire([(272, pt[1]), pt], f'A[{bit}]', label=True)
    for bit in range(8):
        pt = or_hi[f'IN{bit + 1}']
        s.wire([(272, pt[1]), pt], f'A[{bit + 8}]', label=True)

    s.wire([or_lo['OUT'], (656, or_lo['OUT'][1]), (656, nor['IN1'][1]), nor['IN1']], 'NZ_LO', label=True)
    s.wire([or_hi['OUT'], (656, or_hi['OUT'][1]), (656, nor['IN2'][1]), nor['IN2']], 'NZ_HI', label=True)
    s.wire([nor['OUT'], z_pin], 'Z', label=True)
    s.save()


def build_bus_encoder83():
    """Fully wired 8-to-3 Common Bus Encoder (X1..X7 -> SEL[2..0])."""
    s = b.Sheet(
        'bus_encoder83',
        'Common Bus 8-to-3 Encoder (X1..X7 -> SEL[2..0])',
        'S0 = X1+X3+X5+X7, S1 = X2+X3+X6+X7, S2 = X4+X5+X6+X7 (Mano Basic Computer).',
    )
    sel_pin = s.pin('SEL[2..0]', 'output', 1120, 160)
    rail_bottom = 688
    s.wire([sel_pin, (1120, rail_bottom)], 'SEL[2..0]', True)

    rail_x = {}
    for i in range(1, 8):
        y = 112 + (i - 1) * 32
        pin = s.pin(f'X{i}', 'input', 200, y)
        rx = 272 + (i - 1) * 48
        rail_x[i] = rx
        s.wire([pin, (rx, y), (rx, rail_bottom)], f'X{i}', label=True)

    specs = [
        (0, [1, 3, 5, 7], 352),
        (1, [2, 3, 6, 7], 480),
        (2, [4, 5, 6, 7], 608),
    ]
    for bit, xs, y in specs:
        g = s.instance('or4', 768, y, f'encode_s{bit}')
        for idx, xk in enumerate(xs):
            pt = g[f'IN{idx + 1}']
            s.wire([(rail_x[xk], pt[1]), pt], f'X{xk}')
            s.junction((rail_x[xk], pt[1]))
        s.wire([g['OUT'], (1120, g['OUT'][1])], f'SEL[{bit}]', label=True)
    s.save()


def build_datapath_v3():
    """Update Assignment 2 datapath: swap in Quartus RAM: 2-PORT (with rdclock = NOT CLK)
    and export IR_Q, DR_Q, AC_Q, AR_Q, PC_Q, MEM_Q for the hardwired control unit and testbench."""
    s = b.Sheet(
        'datapath',
        'Basic Computer Datapath - ENGI 9861 Assignment 3',
        'Reuses Assignment 2 registers/ALU/BUS; integrates Quartus RAM: 2-PORT (wrclock=CLK, rdclock=NOT CLK) and exports controller feedback ports.',
    )

    mux = s.instance('bus16_mux8', 384, 512, 'COMMON_BUS')
    zero = s.instance('zero16', 32, 512, 'BUS_ZERO')
    s.wire([zero['Y[15..0]'], mux['D0[15..0]']], 'CONST_ZERO[15..0]', True)
    select = s.pin('BUS_SEL[2..0]', 'input', 200, 1024)
    s.wire([select, (544, 1024), mux['SEL[2..0]']], 'BUS_SEL[2..0]', True)

    s.text('BUS sources: 0=0  1=AR  2=PC  3=DR  4=AC  5=IR  6=TR  7=Memory (RAM: 2-PORT)', 960, 112, 12)
    s.text('All registers and flags use rising-edge CLK; RAM rdclock uses NOT(CLK) per Assignment 3 memory guide.', 960, 152, 10)
    s.text('ALU_OP[6..0] is one-hot: bit0 AND, bit1 ADD, bit2 DR, bit3 INPR, bit4 COM, bit5 SHR, bit6 SHL.', 960, 192, 10)
    s.text('CLR / LD / INC are active-high synchronous controls; priority CLR > LD > INC.', 960, 232, 10)

    cells = {}
    configs = [
        ('AR', 'counter12', 960),
        ('PC', 'counter12', 1376),
        ('DR', 'counter16', 1792),
        ('AC', 'counter16', 2208),
        ('IR', 'register16', 2624),
        ('TR', 'counter16', 3040),
    ]
    ld_indices = {'AR': 0, 'PC': 1, 'DR': 2, 'AC': 3, 'IR': 4, 'TR': 5}
    inc_indices = {'AR': 0, 'PC': 1, 'DR': 2, 'AC': 3, 'TR': 4}

    clk = s.pin('CLK', 'input', 200, 1120)
    s.wire([clk, (4032, 1120), (4032, 2416), (896, 2416)], 'CLK')

    s.wire([mux['Y[15..0]'], (816, 688), (816, 1776), (3904, 1776)], 'BUS_DATA[15..0]', True, label=True)
    s.pin('BUS_DATA[15..0]', 'output', 3904, 1776)

    for name, kind, x in configs:
        p = s.instance(kind, x, 1200, name)
        cells[name] = p
        s.wire([(x - 32, 1120), (x - 32, 1264), p['CLK']], 'CLK')
        s.junction((x - 32, 1120))
        for port, index in [('LD', ld_indices[name]), ('CLR', inc_indices.get(name)), ('INC', inc_indices.get(name))]:
            if port in p:
                net = f'REG_{port}[{index}]'
                a = p[port]
                s.wire([(a[0] - 112, a[1]), a], net, label=True)
        if name != 'AC':
            width = 12 if kind == 'counter12' else 16
            a = p[f'DIN[{width - 1}..0]']
            s.wire([(a[0], 1776), a], f'BUS_DATA[{width - 1}..0]', True, label=True)
        s.text(name, x + 100, 1152, 14)

    for name, x in [('AR', 960), ('PC', 1376)]:
        p = s.instance('zext12', x, 928, f'{name}_ZERO_EXTEND')
        s.wire([cells[name]['Q[11..0]'], p['A[11..0]']], f'{name}_Q[11..0]', True)
        cells[name + '_EXT'] = p

    # RAM: 2-PORT (ram2port.vhd) with wrclock = CLK and rdclock = NOT(CLK).
    mem = s.instance('ram2port', 3456, 768, 'RAM_2PORT_4096x16')
    # AR_Q feeds both wraddress and rdaddress.
    s.wire([(1088, 1152), (3264, 1152), (3264, 832), mem['wraddress[11..0]']], 'AR_Q[11..0]', True, label=True)
    s.junction((1088, 1152))
    s.wire([(3264, 864), mem['rdaddress[11..0]']], 'AR_Q[11..0]', True)
    s.junction((3264, 864))

    # wren from MEM_WRITE_EN.
    a = mem['wren']
    s.wire([(a[0] - 128, a[1]), a], 'MEM_WRITE_EN', label=True)

    # wrclock = CLK; rdclock = NOT(CLK) via invert_rdclk placed cleanly to the left of ram2port.
    s.wire([(3392, 1120), (3392, 960), mem['wrclock']], 'CLK')
    s.junction((3392, 1120))
    inv_clk = s.instance('not', 3328, 976, 'invert_rdclk')
    s.wire([(3296, 1120), (3296, 992), inv_clk['IN']], 'CLK')
    s.junction((3296, 1120))
    s.wire([inv_clk['OUT'], mem['rdclock']], 'RD_CLK', label=True)

    # Write data from BUS_DATA.
    s.wire([(3648, 1776), mem['data[15..0]']], 'BUS_DATA[15..0]', True, label=True)
    s.text('RAM: 2-PORT (4096x16, program.mif). AR -> wraddress & rdaddress.', 3280, 688, 10)

    # Seven BUS source paths cleanly routed along the top channel.
    sources = [
        (cells['AR_EXT']['Y[15..0]'], 'AR_EXT', 288),
        (cells['PC_EXT']['Y[15..0]'], 'PC_EXT', 320),
        (cells['DR']['Q[15..0]'], 'DR_Q', 352),
        (cells['AC']['Q[15..0]'], 'AC_Q', 384),
        (cells['IR']['Q[15..0]'], 'IR_Q', 416),
        (cells['TR']['Q[15..0]'], 'TR_Q', 448),
        (mem['q[15..0]'], 'MEM_Q', 480),
    ]
    for slot, (a, net, y) in enumerate(sources, 1):
        x = 128 + 24 * slot
        if slot == 4:
            route = [a, (a[0], 1136), (2672, 1136), (2672, y), (x, y), (x, 544 + slot * 32), mux[f'D{slot}[15..0]']]
        else:
            route = [a, (a[0], y), (x, y), (x, 544 + slot * 32), mux[f'D{slot}[15..0]']]
        s.wire(route, net + '[15..0]', True, label=True)

    # ALU connected to DR, AC, INPR, E, and AC.DIN.
    alu = s.instance('alu16', 2080, 688, 'ALU')
    s.wire([(1920, 608), (2176, 608), alu['DR[15..0]']], 'DR_Q[15..0]', True, label=True)
    s.junction((1920, 608))
    s.wire([(2672, 640), (2368, 640), alu['AC[15..0]']], 'AC_Q[15..0]', True, label=True)
    s.junction((2672, 640))
    s.wire([alu['Y[15..0]'], (2528, 1008), (2528, 1504), (2336, 1504), cells['AC']['DIN[15..0]']], 'ALU_RESULT[15..0]', True, label=True)
    a = alu['OP[6..0]']
    s.wire([(a[0] - 112, a[1]), a], 'ALU_OP[6..0]', True, label=True)
    a = alu['CARRY_OUT']
    s.wire([a, (a[0] + 112, a[1])], 'ALU_CARRY', label=True)

    # INPR & OUTR.
    inpr = s.instance('register8', 1792, 1920, 'INPR')
    outr = s.instance('register8', 2624, 1920, 'OUTR')
    for name, p, x, idx in [('INPR', inpr, 1792, 6), ('OUTR', outr, 2624, 7)]:
        s.text(name, x + 96, 1872, 14)
        s.wire([(x - 32, 1120), (x - 32, 1984), p['CLK']], 'CLK')
        s.junction((x - 32, 1120))
        a = p['LD']
        s.wire([(a[0] - 112, a[1]), a], f'REG_LD[{idx}]', label=True)
    inp = s.pin('INPUT_DATA[7..0]', 'input', 200, 2144)
    s.wire([inp, (1920, 2144), inpr['DIN[7..0]']], 'INPUT_DATA[7..0]', True)
    s.wire([inpr['Q[7..0]'], (1856, 1920), (1856, 816), alu['INPR[7..0]']], 'INPR_Q[7..0]', True, label=True)
    s.wire([(2960, 1776), (2960, 2144), (2752, 2144), outr['DIN[7..0]']], 'BUS_DATA[7..0]', True, label=True)
    s.wire([outr['Q[7..0]'], (2752, 1824), (3904, 1824)], 'OUTPUT_DATA[7..0]', True, label=True)
    s.pin('OUTPUT_DATA[7..0]', 'output', 3904, 1824)

    # External control inputs (from control_unit).
    controls = [
        'REG_LD[7..0]', 'REG_INC[4..0]', 'REG_CLR[4..0]', 'ALU_OP[6..0]',
        'MEM_WRITE_EN', 'FLAG_LD[6..0]', 'FLAG_CLR[6..0]', 'FLAG_DIN[4..0]', 'E_COM',
    ]
    for i, p in enumerate(controls):
        a = s.pin(p, 'input', 200, 1856 + i * 24)
        s.wire([a, (416, a[1])], p, '..' in p)
    s.text('CONTROL INPUTS (driven by hardwired control_unit)', 32, 1800, 10)
    s.text('REG_LD: [0] AR  [1] PC  [2] DR  [3] AC  [4] IR  [5] TR  [6] INPR  [7] OUTR', 960, 1632, 10)
    s.text('REG_CLR / REG_INC: [0] AR  [1] PC  [2] DR  [3] AC  [4] TR', 960, 1664, 10)
    s.text('BUS_DATA -> AR/PC low 12 bits; -> OUTR low 8 bits. AR/PC sources are zero-extended.', 960, 1696, 10)

    # Exported register/memory outputs for control_unit feedback and testbench observation.
    s.text('CONTROLLER FEEDBACK & OBSERVATION OUTPUTS', 3680, 1888, 10)
    export_ports = [
        'AR_Q[11..0]', 'PC_Q[11..0]', 'DR_Q[15..0]',
        'AC_Q[15..0]', 'IR_Q[15..0]', 'MEM_Q[15..0]',
    ]
    for i, pname in enumerate(export_ports):
        y = 1936 + i * 40
        p = s.pin(pname, 'output', 3904, y)
        s.wire([(3680, y), p], pname, True, label=True)

    # State / status FFs: E, I, R, IEN, FGI, FGO, S.
    flagbus = s.pin('FLAG_Q[6..0]', 'output', 3904, 2352)
    s.wire([(896, 2352), flagbus], 'FLAG_Q[6..0]', True, label=True)
    flags = {}
    for i, name in enumerate(['E', 'I', 'R', 'IEN', 'FGI', 'FGO', 'S']):
        x = 960 + i * 384
        p = s.instance('state_bit', x, 2464, name)
        flags[name] = p
        s.text(name, x + 80, 2432, 12)
        s.wire([(x - 32, 2416), (x - 32, 2496), p['CLK']], 'CLK')
        s.junction((x - 32, 2416))
        for port in ['CLR', 'LD']:
            a = p[port]
            s.wire([(a[0] - 112, a[1]), a], f'FLAG_{port}[{i}]', label=True)
        s.wire([p['Q'], (p['Q'][0], 2352)], f'FLAG_Q[{i}]', label=True)
        if i >= 2:
            a = p['DIN']
            s.wire([(a[0], a[1] + 32), a], f'FLAG_DIN[{i - 2}]', label=True)
    s.wire([flags['E']['Q'], (1064, 2384), (864, 2384), (864, 848), alu['E']], 'FLAG_Q[0]', label=True)
    s.junction((1064, 2384))
    a = flags['I']['DIN']
    s.wire([(a[0], a[1] + 32), a], 'IR_Q[15]', label=True)

    en = named(
        s, 'extend_next', 320, 2240, 'E_NEXT_LOGIC',
        {'E': 'FLAG_Q[0]', 'AC0': 'AC_Q[0]', 'AC15': 'AC_Q[15]', 'CARRY': 'ALU_CARRY', 'OP[6..0]': 'ALU_OP[6..0]', 'COM': 'E_COM'},
    )
    s.wire([en['Y'], (736, 2336), (736, 2672), (1064, 2672), flags['E']['DIN']], 'E_NEXT', label=True)
    s.text('FLAG_Q / FLAG_LD / FLAG_CLR: [0] E  [1] I  [2] R  [3] IEN  [4] FGI  [5] FGO  [6] S', 960, 2768, 10)
    s.text('I loads IR[15]. FLAG_DIN[0..4] supplies R, IEN, FGI, FGO, S. S=1 runs; HLT clears S to 0.', 960, 2800, 10)
    s.save()


def build_control_unit():
    """Build complete Hardwired Control Unit (control_unit.bdf) matching MOPs.pdf."""
    s = b.Sheet(
        'control_unit',
        'Basic Computer Hardwired Control Unit - ENGI 9861 Assignment 3',
        'Implements Mano Basic Computer fetch, decode, indirect, interrupt, memory-ref, register-ref, and I/O control equations (MOPs.pdf).',
    )

    # ------------------------------------------------------------------
    # Input pins (top-left) and Output pins (top-right)
    # ------------------------------------------------------------------
    s.text('INPUTS', 32, 96, 12)
    in_pins = ['CLK', 'RESET', 'IR_Q[15..0]', 'DR_Q[15..0]', 'AC_Q[15..0]', 'FLAG_Q[6..0]']
    for i, pname in enumerate(in_pins):
        pt = s.pin(pname, 'input', 200, 144 + i * 32)
        s.wire([pt, (368, pt[1])], pname, '..' in pname, label=True)

    s.text('OUTPUTS', 3264, 96, 12)
    out_pins = [
        'BUS_SEL[2..0]', 'REG_LD[7..0]', 'REG_INC[4..0]', 'REG_CLR[4..0]',
        'ALU_OP[6..0]', 'MEM_WRITE_EN', 'FLAG_LD[6..0]', 'FLAG_CLR[6..0]',
        'FLAG_DIN[4..0]', 'E_COM', 'SC_Q[3..0]',
    ]
    for i, pname in enumerate(out_pins):
        pt = s.pin(pname, 'output', 3392, 144 + i * 32)
        s.wire([(3216, pt[1]), pt], pname, '..' in pname, label=True)

    # Logic constants ZERO and ONE.
    named(s, 'gnd', 512, 144, 'const_zero', {'1': 'ZERO'}, stub=64)
    named(s, 'vcc', 640, 144, 'const_one', {'1': 'ONE'}, stub=64)
    # 4-bit zero bus for SC DIN[3..0].
    for bit in range(4):
        named(s, 'gnd', 512 + bit * 112, 272, f'sc_din_z{bit}', {'1': f'SC_DIN[{bit}]'}, stub=48)

    # ------------------------------------------------------------------
    # Section 1: Sequencer, Decoders, Zero Detectors & Bus Encoder
    # ------------------------------------------------------------------
    s.text('1. SEQUENCE COUNTER, DECODERS, ZERO DETECTORS & BUS ENCODER', 32, 384, 12)

    # RUN_EN = S AND (NOT RESET)
    inv_rst = s.instance('not', 144, 448, 'inv_reset')
    s.wire([(32, inv_rst['IN'][1]), inv_rst['IN']], 'RESET', label=True)
    run_and = s.instance('and2', 336, 448, 'run_enable')
    s.wire([inv_rst['OUT'], run_and['IN1']], 'NRESET', label=True)
    s.wire([(224, run_and['IN2'][1]), run_and['IN2']], 'FLAG_Q[6]', label=True)
    s.wire([run_and['OUT'], (464, run_and['OUT'][1])], 'RUN_EN', label=True)

    # SC (counter4) wired directly to TIMING_DEC (dec416_en).
    sc = s.instance('counter4', 592, 432, 'SC')
    for pname, net in [('CLK', 'CLK'), ('CLR', 'SC_CLR'), ('LD', 'ZERO'), ('INC', 'RUN_EN')]:
        a = sc[pname]
        s.wire([(a[0] - 112, a[1]), a], net, label=True)
    a = sc['DIN[3..0]']
    s.wire([a, (a[0], a[1] + 32)], 'SC_DIN[3..0]', True, label=True)

    tdec = s.instance('dec416_en', 1024, 448, 'TIMING_DEC')
    s.wire([sc['Q[3..0]'], (720, 400), (960, 400), (960, tdec['A[3..0]'][1]), tdec['A[3..0]']], 'SC_Q[3..0]', True, label=True)
    s.wire([(tdec['EN'][0] - 112, tdec['EN'][1]), tdec['EN']], 'RUN_EN', label=True)
    s.wire([tdec['Y[15..0]'], (tdec['Y[15..0]'][0] + 128, tdec['Y[15..0]'][1])], 'T[15..0]', True, label=True)

    # Opcode decoder (IR_Q[14..12] -> D[7..0]).
    odec = s.instance('dec38_en', 1600, 464, 'OPCODE_DEC')
    s.wire([(odec['A[2..0]'][0] - 144, odec['A[2..0]'][1]), odec['A[2..0]']], 'IR_Q[14..12]', True, label=True)
    s.wire([odec['Y[7..0]'], (odec['Y[7..0]'][0] + 128, odec['Y[7..0]'][1])], 'D[7..0]', True, label=True)

    # Zero detectors for DR and AC.
    drz = s.instance('zero_detect16', 2144, 432, 'DR_ZERO_DET')
    s.wire([(drz['A[15..0]'][0] - 144, drz['A[15..0]'][1]), drz['A[15..0]']], 'DR_Q[15..0]', True, label=True)
    s.wire([drz['Z'], (drz['Z'][0] + 112, drz['Z'][1])], 'DR_Z', label=True)

    acz = s.instance('zero_detect16', 2144, 576, 'AC_ZERO_DET')
    s.wire([(acz['A[15..0]'][0] - 144, acz['A[15..0]'][1]), acz['A[15..0]']], 'AC_Q[15..0]', True, label=True)
    s.wire([acz['Z'], (acz['Z'][0] + 112, acz['Z'][1])], 'AC_Z', label=True)

    # Bus 8-to-3 Encoder (X1..X7 -> BUS_SEL[2..0]).
    benc = s.instance('bus_encoder83', 2784, 432, 'BUS_ENC')
    for i in range(1, 8):
        pt = benc[f'X{i}']
        s.wire([(pt[0] - 112, pt[1]), pt], f'X{i}', label=True)
    s.wire([benc['SEL[2..0]'], (benc['SEL[2..0]'][0] + 144, benc['SEL[2..0]'][1])], 'BUS_SEL[2..0]', True, label=True)

    # Complements row.
    comp_specs = [
        ('inv_r', 'FLAG_Q[2]', 'NR'),
        ('inv_i', 'FLAG_Q[1]', 'NI'),
        ('inv_d7', 'D[7]', 'ND7'),
        ('inv_e', 'FLAG_Q[0]', 'NE'),
        ('inv_ac15', 'AC_Q[15]', 'NAC15'),
        ('inv_t0', 'T[0]', 'NT0'),
        ('inv_t1', 'T[1]', 'NT1'),
        ('inv_t2', 'T[2]', 'NT2'),
    ]
    for i, (iname, src, dst) in enumerate(comp_specs):
        named(s, 'not', 176 + i * 384, 768, iname, {'IN': src, 'OUT': dst}, stub=112)

    # ------------------------------------------------------------------
    # Section 2: Cycle Control Terms & Instruction Minterms
    # ------------------------------------------------------------------
    s.text('2. CYCLE ROUTINE TERMS (FETCH / DECODE / INDIRECT / INTERRUPT / REG-REF / IO)', 32, 864, 12)
    cycle_and2 = [
        ('fetch0', 'NR', 'T[0]', 'FETCH0'),
        ('fetch1', 'NR', 'T[1]', 'FETCH1'),
        ('decode', 'NR', 'T[2]', 'DECODE'),
        ('ind_a', 'ND7', 'FLAG_Q[1]', 'IND_A'),
        ('indirect', 'IND_A', 'T[3]', 'INDIRECT'),
        ('int0', 'FLAG_Q[2]', 'T[0]', 'INT0'),
        ('int1', 'FLAG_Q[2]', 'T[1]', 'INT1'),
        ('int2', 'FLAG_Q[2]', 'T[2]', 'INT2'),
        ('r_com_a', 'D[7]', 'NI', 'R_COM_A'),
        ('r_com', 'R_COM_A', 'T[3]', 'R_COM'),
        ('p_com_a', 'D[7]', 'FLAG_Q[1]', 'P_COM_A'),
        ('p_com', 'P_COM_A', 'T[3]', 'P_COM'),
        ('d7t3', 'D[7]', 'T[3]', 'D7T3'),
    ]
    for i, (iname, a1, a2, out) in enumerate(cycle_and2):
        col, row = i % 7, i // 7
        named(s, 'and2', 176 + col * 480, 912 + row * 96, iname, {'IN1': a1, 'IN2': a2, 'OUT': out}, stub=112)

    s.text('3. MEMORY-REFERENCE TERMS (D0T4 .. D6T6)', 32, 1136, 12)
    mem_terms = [
        ('d0t4', 'D[0]', 'T[4]', 'D0T4'), ('d0t5', 'D[0]', 'T[5]', 'D0T5'),
        ('d1t4', 'D[1]', 'T[4]', 'D1T4'), ('d1t5', 'D[1]', 'T[5]', 'D1T5'),
        ('d2t4', 'D[2]', 'T[4]', 'D2T4'), ('d2t5', 'D[2]', 'T[5]', 'D2T5'),
        ('d3t4', 'D[3]', 'T[4]', 'D3T4'),
        ('d4t4', 'D[4]', 'T[4]', 'D4T4'),
        ('d5t4', 'D[5]', 'T[4]', 'D5T4'), ('d5t5', 'D[5]', 'T[5]', 'D5T5'),
        ('d6t4', 'D[6]', 'T[4]', 'D6T4'), ('d6t5', 'D[6]', 'T[5]', 'D6T5'), ('d6t6', 'D[6]', 'T[6]', 'D6T6'),
    ]
    for i, (iname, a1, a2, out) in enumerate(mem_terms):
        col, row = i % 7, i // 7
        named(s, 'and2', 176 + col * 480, 1184 + row * 96, iname, {'IN1': a1, 'IN2': a2, 'OUT': out}, stub=112)

    s.text('4. REGISTER-REFERENCE (r*Bi) & INPUT-OUTPUT (p*Bi) TERMS', 32, 1408, 12)
    reg_io_terms = [
        ('rb11_cla', 'R_COM', 'IR_Q[11]', 'RB11'),
        ('rb10_cle', 'R_COM', 'IR_Q[10]', 'RB10'),
        ('rb9_cma',  'R_COM', 'IR_Q[9]',  'RB9'),
        ('rb8_cme',  'R_COM', 'IR_Q[8]',  'RB8'),
        ('rb7_cir',  'R_COM', 'IR_Q[7]',  'RB7'),
        ('rb6_cil',  'R_COM', 'IR_Q[6]',  'RB6'),
        ('rb5_inc',  'R_COM', 'IR_Q[5]',  'RB5'),
        ('rb4_spa',  'R_COM', 'IR_Q[4]',  'RB4'),
        ('rb3_sna',  'R_COM', 'IR_Q[3]',  'RB3'),
        ('rb2_sza',  'R_COM', 'IR_Q[2]',  'RB2'),
        ('rb1_sze',  'R_COM', 'IR_Q[1]',  'RB1'),
        ('rb0_hlt',  'R_COM', 'IR_Q[0]',  'RB0'),
        ('pb11_inp', 'P_COM', 'IR_Q[11]', 'PB11'),
        ('pb10_out', 'P_COM', 'IR_Q[10]', 'PB10'),
        ('pb9_ski',  'P_COM', 'IR_Q[9]',  'PB9'),
        ('pb8_sko',  'P_COM', 'IR_Q[8]',  'PB8'),
        ('pb7_ion',  'P_COM', 'IR_Q[7]',  'PB7'),
        ('pb6_iof',  'P_COM', 'IR_Q[6]',  'PB6'),
    ]
    for i, (iname, a1, a2, out) in enumerate(reg_io_terms):
        col, row = i % 6, i // 6
        named(s, 'and2', 176 + col * 560, 1456 + row * 96, iname, {'IN1': a1, 'IN2': a2, 'OUT': out}, stub=112)

    # ------------------------------------------------------------------
    # Section 5: Register Control Equations (AR, PC, DR, AC, IR, TR, INPR, OUTR)
    # ------------------------------------------------------------------
    s.text('5. REGISTER CONTROLS (LD / INC / CLR) & SKIP CONDITIONS', 32, 1776, 12)

    # Column 1 (x=176): AR & DR & TR/IR/OUTR
    named(s, 'or2',  176, 1824, 'ar_ld_a',  {'IN1': 'FETCH0', 'IN2': 'DECODE', 'OUT': 'AR_LD_A'}, stub=112)
    named(s, 'or2',  176, 1920, 'ar_ld',    {'IN1': 'AR_LD_A', 'IN2': 'INDIRECT', 'OUT': 'REG_LD[0]'}, stub=112)
    named(s, 'wire', 176, 2016, 'ar_inc',   {'IN': 'D5T4', 'OUT': 'REG_INC[0]'}, stub=112)
    named(s, 'or2',  176, 2096, 'ar_clr',   {'IN1': 'INT0', 'IN2': 'RESET', 'OUT': 'REG_CLR[0]'}, stub=112)

    named(s, 'or4',  176, 2208, 'dr_ld',    {'IN1': 'D0T4', 'IN2': 'D1T4', 'IN3': 'D2T4', 'IN4': 'D6T4', 'OUT': 'REG_LD[2]'}, stub=112)
    named(s, 'wire', 176, 2336, 'dr_inc',   {'IN': 'D6T5', 'OUT': 'REG_INC[2]'}, stub=112)
    named(s, 'wire', 176, 2416, 'dr_clr',   {'IN': 'RESET', 'OUT': 'REG_CLR[2]'}, stub=112)

    named(s, 'wire', 176, 2512, 'ir_ld',    {'IN': 'FETCH1', 'OUT': 'REG_LD[4]'}, stub=112)
    named(s, 'wire', 176, 2592, 'tr_ld',    {'IN': 'INT0', 'OUT': 'REG_LD[5]'}, stub=112)
    named(s, 'wire', 176, 2672, 'tr_inc',   {'IN': 'ZERO', 'OUT': 'REG_INC[4]'}, stub=112)
    named(s, 'wire', 176, 2752, 'tr_clr',   {'IN': 'RESET', 'OUT': 'REG_CLR[4]'}, stub=112)
    named(s, 'wire', 176, 2832, 'inpr_ld',  {'IN': 'ZERO', 'OUT': 'REG_LD[6]'}, stub=112)
    named(s, 'wire', 176, 2912, 'outr_ld',  {'IN': 'PB10', 'OUT': 'REG_LD[7]'}, stub=112)

    # Column 2 (x=736): PC controls & 7 skip conditions
    named(s, 'or2',  736, 1824, 'pc_ld',    {'IN1': 'D4T4', 'IN2': 'D5T5', 'OUT': 'REG_LD[1]'}, stub=112)
    named(s, 'or2',  736, 1920, 'pc_clr',   {'IN1': 'INT1', 'IN2': 'RESET', 'OUT': 'REG_CLR[1]'}, stub=112)
    skip_specs = [
        ('skip_isz', 'D6T6', 'DR_Z',      'SKIP_ISZ'),
        ('skip_spa', 'RB4',  'NAC15',     'SKIP_SPA'),
        ('skip_sna', 'RB3',  'AC_Q[15]',  'SKIP_SNA'),
        ('skip_sza', 'RB2',  'AC_Z',      'SKIP_SZA'),
        ('skip_sze', 'RB1',  'NE',        'SKIP_SZE'),
        ('skip_ski', 'PB9',  'FLAG_Q[4]', 'SKIP_SKI'),
        ('skip_sko', 'PB8',  'FLAG_Q[5]', 'SKIP_SKO'),
    ]
    for i, (iname, a1, a2, out) in enumerate(skip_specs):
        named(s, 'and2', 736, 2032 + i * 96, iname, {'IN1': a1, 'IN2': a2, 'OUT': out}, stub=112)

    named(s, 'or8', 1296, 1824, 'pc_inc_skips', {
        'IN1': 'SKIP_ISZ', 'IN2': 'SKIP_SPA', 'IN3': 'SKIP_SNA', 'IN4': 'SKIP_SZA',
        'IN5': 'SKIP_SZE', 'IN6': 'SKIP_SKI', 'IN7': 'SKIP_SKO', 'IN8': 'INT2',
        'OUT': 'PC_INC_SKIP',
    }, stub=112)
    named(s, 'or2', 1296, 2048, 'pc_inc', {'IN1': 'FETCH1', 'IN2': 'PC_INC_SKIP', 'OUT': 'REG_INC[1]'}, stub=112)

    # Column 3 (x=1296 lower): AC & ALU_OP controls
    named(s, 'or8', 1296, 2176, 'ac_ld', {
        'IN1': 'D0T5', 'IN2': 'D1T5', 'IN3': 'D2T5', 'IN4': 'PB11',
        'IN5': 'RB9',  'IN6': 'RB7',  'IN7': 'RB6',  'IN8': 'ZERO',
        'OUT': 'REG_LD[3]',
    }, stub=112)
    named(s, 'wire', 1296, 2400, 'ac_inc', {'IN': 'RB5', 'OUT': 'REG_INC[3]'}, stub=112)
    named(s, 'or2',  1296, 2480, 'ac_clr', {'IN1': 'RB11', 'IN2': 'RESET', 'OUT': 'REG_CLR[3]'}, stub=112)

    alu_map = [
        ('alu_and',  'D0T5', 'ALU_OP[0]'),
        ('alu_add',  'D1T5', 'ALU_OP[1]'),
        ('alu_dr',   'D2T5', 'ALU_OP[2]'),
        ('alu_inpr', 'PB11', 'ALU_OP[3]'),
        ('alu_com',  'RB9',  'ALU_OP[4]'),
        ('alu_shr',  'RB7',  'ALU_OP[5]'),
        ('alu_shl',  'RB6',  'ALU_OP[6]'),
    ]
    for i, (iname, src, dst) in enumerate(alu_map):
        named(s, 'wire', 1856, 1824 + i * 80, iname, {'IN': src, 'OUT': dst}, stub=112)

    # ------------------------------------------------------------------
    # Section 6: Bus Sources (X1..X7), Memory Write, Flags & SC_CLR
    # ------------------------------------------------------------------
    s.text('6. BUS SOURCES (X1..X7), MEMORY WRITE, FLAGS & SC_CLR', 2304, 1776, 12)

    # Column 4 (x=2416): X1..X7 & MEM_WRITE_EN & SC_CLR
    named(s, 'or2',  2416, 1824, 'bus_x1', {'IN1': 'D4T4', 'IN2': 'D5T5', 'OUT': 'X1'}, stub=112)
    named(s, 'or2',  2416, 1920, 'bus_x2', {'IN1': 'T[0]', 'IN2': 'D5T4', 'OUT': 'X2'}, stub=112)
    named(s, 'wire', 2416, 2016, 'bus_x3', {'IN': 'D6T6', 'OUT': 'X3'}, stub=112)
    named(s, 'or2',  2416, 2096, 'bus_x4', {'IN1': 'D3T4', 'IN2': 'PB10', 'OUT': 'X4'}, stub=112)
    named(s, 'wire', 2416, 2192, 'bus_x5', {'IN': 'DECODE', 'OUT': 'X5'}, stub=112)
    named(s, 'wire', 2416, 2272, 'bus_x6', {'IN': 'INT1', 'OUT': 'X6'}, stub=112)
    named(s, 'or6',  2416, 2368, 'bus_x7', {
        'IN1': 'FETCH1', 'IN2': 'INDIRECT', 'IN3': 'D0T4',
        'IN4': 'D1T4',   'IN5': 'D2T4',     'IN6': 'D6T4',
        'OUT': 'X7',
    }, stub=112)

    named(s, 'or4', 2416, 2560, 'mem_wr', {
        'IN1': 'INT1', 'IN2': 'D3T4', 'IN3': 'D5T4', 'IN4': 'D6T6',
        'OUT': 'MEM_WRITE_EN',
    }, stub=112)

    named(s, 'or2', 2416, 2688, 't4_done', {'IN1': 'D3T4', 'IN2': 'D4T4', 'OUT': 'T4_DONE'}, stub=112)
    named(s, 'or4', 2416, 2784, 't5_done', {'IN1': 'D0T5', 'IN2': 'D1T5', 'IN3': 'D2T5', 'IN4': 'D5T5', 'OUT': 'T5_DONE'}, stub=112)
    named(s, 'or6', 2416, 2912, 'sc_clr_gate', {
        'IN1': 'RESET', 'IN2': 'INT2', 'IN3': 'D7T3',
        'IN4': 'T4_DONE', 'IN5': 'T5_DONE', 'IN6': 'D6T6',
        'OUT': 'SC_CLR',
    }, stub=112)

    # Column 5 (x=2976): Flag Controls (E, I, R, IEN, FGI, FGO, S)
    named(s, 'wire', 2976, 1824, 'e_com_drv', {'IN': 'RB8', 'OUT': 'E_COM'}, stub=112)
    named(s, 'or4',  2976, 1904, 'e_ld',      {'IN1': 'D1T5', 'IN2': 'RB7', 'IN3': 'RB6', 'IN4': 'RB8', 'OUT': 'FLAG_LD[0]'}, stub=112)
    named(s, 'or2',  2976, 2032, 'e_clr',     {'IN1': 'RB10', 'IN2': 'RESET', 'OUT': 'FLAG_CLR[0]'}, stub=112)

    named(s, 'wire', 2976, 2128, 'i_ld',      {'IN': 'DECODE', 'OUT': 'FLAG_LD[1]'}, stub=112)
    named(s, 'wire', 2976, 2208, 'i_clr',     {'IN': 'RESET', 'OUT': 'FLAG_CLR[1]'}, stub=112)

    # Interrupt R <- 1: RUN_EN & T0' & T1' & T2' & IEN & (FGI + FGO)
    named(s, 'and4', 2976, 2304, 'not_t012',  {'IN1': 'RUN_EN', 'IN2': 'NT0', 'IN3': 'NT1', 'IN4': 'NT2', 'OUT': 'NOT_T012'}, stub=112)
    named(s, 'or2',  2976, 2432, 'fg_any',    {'IN1': 'FLAG_Q[4]', 'IN2': 'FLAG_Q[5]', 'OUT': 'FG_ANY'}, stub=112)
    named(s, 'and2', 2976, 2528, 'int_cond',  {'IN1': 'FLAG_Q[3]', 'IN2': 'FG_ANY', 'OUT': 'INT_COND'}, stub=112)
    named(s, 'and2', 2976, 2624, 'r_ld',      {'IN1': 'NOT_T012', 'IN2': 'INT_COND', 'OUT': 'FLAG_LD[2]'}, stub=112)
    named(s, 'or2',  2976, 2720, 'r_clr',     {'IN1': 'INT2', 'IN2': 'RESET', 'OUT': 'FLAG_CLR[2]'}, stub=112)
    named(s, 'wire', 2976, 2816, 'r_din',     {'IN': 'ONE', 'OUT': 'FLAG_DIN[0]'}, stub=112)

    # Column 6 (x=3488): IEN, FGI, FGO, S flags
    named(s, 'wire', 3488, 1824, 'ien_ld',    {'IN': 'PB7', 'OUT': 'FLAG_LD[3]'}, stub=112)
    named(s, 'or2',  3488, 1904, 'ien_clr_a', {'IN1': 'PB6', 'IN2': 'INT2', 'OUT': 'IEN_CLR_A'}, stub=112)
    named(s, 'or2',  3488, 2000, 'ien_clr',   {'IN1': 'IEN_CLR_A', 'IN2': 'RESET', 'OUT': 'FLAG_CLR[3]'}, stub=112)
    named(s, 'wire', 3488, 2096, 'ien_din',   {'IN': 'ONE', 'OUT': 'FLAG_DIN[1]'}, stub=112)

    named(s, 'wire', 3488, 2192, 'fgi_ld',    {'IN': 'ZERO', 'OUT': 'FLAG_LD[4]'}, stub=112)
    named(s, 'or2',  3488, 2272, 'fgi_clr',   {'IN1': 'PB11', 'IN2': 'RESET', 'OUT': 'FLAG_CLR[4]'}, stub=112)
    named(s, 'wire', 3488, 2368, 'fgi_din',   {'IN': 'ZERO', 'OUT': 'FLAG_DIN[2]'}, stub=112)

    named(s, 'wire', 3488, 2464, 'fgo_ld',    {'IN': 'ZERO', 'OUT': 'FLAG_LD[5]'}, stub=112)
    named(s, 'or2',  3488, 2544, 'fgo_clr',   {'IN1': 'PB10', 'IN2': 'RESET', 'OUT': 'FLAG_CLR[5]'}, stub=112)
    named(s, 'wire', 3488, 2640, 'fgo_din',   {'IN': 'ZERO', 'OUT': 'FLAG_DIN[3]'}, stub=112)

    named(s, 'wire', 3488, 2736, 's_ld',      {'IN': 'RESET', 'OUT': 'FLAG_LD[6]'}, stub=112)
    named(s, 'wire', 3488, 2816, 's_clr',     {'IN': 'RB0', 'OUT': 'FLAG_CLR[6]'}, stub=112)
    named(s, 'wire', 3488, 2896, 's_din',     {'IN': 'ONE', 'OUT': 'FLAG_DIN[4]'}, stub=112)

    s.save()


def build_basic_computer():
    """Build fully wired top-level Basic Computer schematic connecting CONTROL_UNIT and DATAPATH."""
    s = b.Sheet(
        'basic_computer',
        'Complete Basic Computer - ENGI 9861 Assignment 3',
        'Hardwired Control Unit connected to Assignment 2 Datapath + Quartus RAM: 2-PORT (program.mif).',
    )

    cu_x, cu_y = 512, 320
    dp_x, dp_y = 1360, 320
    cu = s.instance('control_unit', cu_x, cu_y, 'CONTROL_UNIT')
    dp = s.instance('datapath', dp_x, dp_y, 'DATAPATH')

    s.text('CONTROL UNIT (Hardwired)', cu_x + 48, cu_y - 36, 12)
    s.text('DATAPATH + RAM: 2-PORT (4096x16)', dp_x + 32, dp_y - 36, 12)

    # Top-level inputs on the left.
    clk_pin = s.pin('CLK', 'input', 200, cu['CLK'][1])
    rst_pin = s.pin('RESET', 'input', 200, cu['RESET'][1])
    inp_pin = s.pin('INPUT_DATA[7..0]', 'input', 200, dp['INPUT_DATA[7..0]'][1] + 96)

    # CLK feeds both CONTROL_UNIT and DATAPATH cleanly via a horizontal rail above control buses.
    s.wire([clk_pin, cu['CLK']], 'CLK', label=True)
    s.wire([(320, cu['CLK'][1]), (320, 264), (1264, 264), (1264, dp['CLK'][1]), dp['CLK']], 'CLK')
    s.junction((320, cu['CLK'][1]))

    # RESET feeds CONTROL_UNIT directly.
    s.wire([rst_pin, cu['RESET']], 'RESET', label=True)

    # INPUT_DATA[7..0] runs cleanly underneath CONTROL_UNIT to DATAPATH.
    s.wire([inp_pin, (1264, inp_pin[1]), (1264, dp['INPUT_DATA[7..0]'][1]), dp['INPUT_DATA[7..0]']], 'INPUT_DATA[7..0]', True, label=True)

    # Direct straight horizontal control signals from CONTROL_UNIT -> DATAPATH!
    ctrl_ports = [
        'BUS_SEL[2..0]', 'REG_LD[7..0]', 'REG_INC[4..0]', 'REG_CLR[4..0]',
        'ALU_OP[6..0]', 'MEM_WRITE_EN', 'FLAG_LD[6..0]', 'FLAG_CLR[6..0]',
        'FLAG_DIN[4..0]', 'E_COM',
    ]
    for pname in ctrl_ports:
        a, c = cu[pname], dp[pname]
        assert a[1] == c[1], (pname, a, c)
        s.wire([a, c], pname, '..' in pname, label=True)

    # Feedback buses routed cleanly over the top channel from DATAPATH right -> CONTROL_UNIT left,
    # AND straight out to observation pins on the right!
    out_x = 2240
    fb_routes = [
        ('AC_Q[15..0]',   112, 288, 1968),
        ('FLAG_Q[6..0]',  144, 336, 2000),
        ('IR_Q[15..0]',   176, 384, 2032),
        ('DR_Q[15..0]',   208, 432, 2064),
    ]
    for pname, top_y, left_x, right_x in fb_routes:
        src = dp[pname]
        dst = cu[pname]
        out_p = s.pin(pname, 'output', out_x, src[1])
        s.wire([src, out_p], pname, True, label=True)
        s.wire([(right_x, src[1]), (right_x, top_y), (left_x, top_y), (left_x, dst[1]), dst], pname, True)
        s.junction((right_x, src[1]))

    # Remaining DATAPATH observation outputs straight to the right!
    for pname in ['PC_Q[11..0]', 'AR_Q[11..0]', 'BUS_DATA[15..0]', 'MEM_Q[15..0]', 'OUTPUT_DATA[7..0]']:
        src = dp[pname]
        out_p = s.pin(pname, 'output', out_x, src[1])
        s.wire([src, out_p], pname, True, label=True)

    # Standalone scalar observation outputs for E (FLAG_Q[0]), S (FLAG_Q[6]), MEM_WR_OUT, and SC_Q[3..0].
    # Placed cleanly below DATAPATH outputs with explicit physical wires.
    sc_out = s.pin('SC_Q[3..0]', 'output', out_x, 1088)
    s.wire([cu['SC_Q[3..0]'], (1120, cu['SC_Q[3..0]'][1]), (1120, 1088), sc_out], 'SC_Q[3..0]', True, label=True)

    # Branch MEM_WRITE_EN down to a dedicated observation output via a wire buffer.
    mwr_buf = s.instance('wire', 1984, 1120, 'obs_mem_wr')
    mwr_out = s.pin('MEM_WR_OUT', 'output', out_x, mwr_buf['OUT'][1])
    mw_pt = cu['MEM_WRITE_EN']
    s.wire([(1168, mw_pt[1]), (1168, mwr_buf['IN'][1]), mwr_buf['IN']], 'MEM_WRITE_EN')
    s.junction((1168, mw_pt[1]))
    s.wire([mwr_buf['OUT'], mwr_out], 'MEM_WR_OUT', label=True)

    # Dedicated E_OUT and S_OUT scalar pins tapped cleanly from FLAG_Q[6..0] bus via wire buffers.
    e_buf = s.instance('wire', 1984, 1184, 'obs_e')
    e_out = s.pin('E_OUT', 'output', out_x, e_buf['OUT'][1])
    s.wire([(1840, e_buf['IN'][1]), e_buf['IN']], 'FLAG_Q[0]', label=True)
    s.wire([e_buf['OUT'], e_out], 'E_OUT', label=True)

    s_buf = s.instance('wire', 1984, 1248, 'obs_s')
    s_out = s.pin('S_OUT', 'output', out_x, s_buf['OUT'][1])
    s.wire([(1840, s_buf['IN'][1]), s_buf['IN']], 'FLAG_Q[6]', label=True)
    s.wire([s_buf['OUT'], s_out], 'S_OUT', label=True)

    s.text('Key testbench checkpoints: AC_Q, E_OUT, S_OUT, AR_Q, BUS_DATA, MEM_WR_OUT (M[103] & M[201]).', 512, 1168, 10)
    s.save()


def write_project_files():
    all_bdfs = [
        'counter16', 'counter12', 'counter4', 'register8', 'register16',
        'bus16_mux8', 'priority_control', 'alu16', 'alu_slice',
        'state_bit', 'extend_next', 'zext12', 'zero16',
        'dec38_en', 'dec416_en', 'zero_detect16', 'bus_encoder83',
        'datapath', 'control_unit', 'basic_computer',
    ]

    def make_qsf(top_entity, include_ram=True):
        lines = [
            'set_global_assignment -name FAMILY "Cyclone V"',
            'set_global_assignment -name DEVICE 5CGXFC7C7F23C8',
            f'set_global_assignment -name TOP_LEVEL_ENTITY {top_entity}',
            'set_global_assignment -name ORIGINAL_QUARTUS_VERSION 20.1.0',
            'set_global_assignment -name LAST_QUARTUS_VERSION "20.1.1 Lite Edition"',
            'set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files',
            'set_global_assignment -name SEARCH_PATH .',
            'set_global_assignment -name NUM_PARALLEL_PROCESSORS 2',
            'set_global_assignment -name EDA_SIMULATION_TOOL "ModelSim-Altera (VHDL)"',
            'set_global_assignment -name EDA_OUTPUT_DATA_FORMAT VHDL -section_id eda_simulation',
        ]
        for bdf in all_bdfs:
            lines.append(f'set_global_assignment -name BDF_FILE {bdf}.bdf')
        if include_ram:
            lines.append('set_global_assignment -name VHDL_FILE ram2port.vhd')
            lines.append('set_global_assignment -name MIF_FILE program.mif')
        return '\n'.join(lines) + '\n'

    (ROOT / 'basic_computer.qsf').write_text(make_qsf('basic_computer', include_ram=True))
    (ROOT / 'control_unit.qsf').write_text(make_qsf('control_unit', include_ram=False))
    (ROOT / 'datapath.qsf').write_text(make_qsf('datapath', include_ram=True))

    qpf = (
        'QUARTUS_VERSION = "20.1"\n'
        'PROJECT_REVISION = "basic_computer"\n'
        'PROJECT_REVISION = "control_unit"\n'
        'PROJECT_REVISION = "datapath"\n'
        'PROJECT_REVISION = "counter16"\n'
        'PROJECT_REVISION = "counter12"\n'
        'PROJECT_REVISION = "register16"\n'
        'PROJECT_REVISION = "register8"\n'
        'PROJECT_REVISION = "bus16_mux8"\n'
    )
    (ROOT / 'assignment3.qpf').write_text(qpf)


def fix_bdf_file(path):
    """Expand text rects in any saved BDF/BSF so High-DPI Quartus never clips labels."""
    nodes = b.parse(path.read_text())
    for n in nodes:
        expand_text_rects(n)
        # Keep visible right-aligned port text inside hierarchical symbol rectangles.
        if isinstance(n, list) and n and n[0] == 'symbol':
            srect = next((c for c in n if isinstance(c, list) and c and c[0] == 'rect'), None)
            if srect:
                sw = int(srect[3]) - int(srect[1])
                if sw >= 160:
                    for c in n:
                        if isinstance(c, list) and c and c[0] == 'port':
                            pt = next((p for p in c if isinstance(p, list) and p and p[0] == 'pt'), None)
                            if pt and int(pt[1]) == sw:
                                for t in c:
                                    if isinstance(t, list) and t and t[0] == 'text' and ['invisible'] not in t:
                                        tr = next((r for r in t if isinstance(r, list) and r and r[0] == 'rect'), None)
                                        if tr:
                                            tw = int(tr[3]) - int(tr[1])
                                            new_x0 = max(18, sw - 18 - tw)
                                            tr[1], tr[3] = new_x0, new_x0 + tw
    path.write_text('\n'.join(b.emit(n) for n in nodes) + '\n')


def build():
    define_symbols()
    for sym in b.SYMS.values():
        expand_text_rects(sym)
    build_counter4()
    build_dec38()
    build_dec416()
    build_zero_detect16()
    build_bus_encoder83()
    build_datapath_v3()
    build_control_unit()
    build_basic_computer()

    for name in [
        'ram2port', 'counter4', 'dec38_en', 'dec416_en',
        'zero_detect16', 'bus_encoder83', 'datapath', 'control_unit',
    ]:
        save_bsf(name)

    # Ensure ALL schematics (including ALU and Assignment 2 sub-sheets) have High-DPI-safe text boxes.
    for ext in ['*.bdf', '*.bsf']:
        for p in ROOT.glob(ext):
            fix_bdf_file(p)

    write_project_files()
    print('Successfully generated Assignment 3 schematics, symbols, and Quartus project files.')


if __name__ == '__main__':
    build()
