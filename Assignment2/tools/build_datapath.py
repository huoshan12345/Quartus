"""Build the Part B BDF, reusing Part A entities without regenerating them."""
from pathlib import Path
import json
import sys
import build_schematics as b

ROOT=Path(__file__).resolve().parents[1]
b.ROOT=ROOT
NEW=['datapath','alu16','alu_slice','state_bit','extend_next','zext12','zero16']
for name,folder in [('wire','buffer'),('or8','logic')]:
    b.SYMS[name]=next(n for n in b.parse((b.LIB/'primitives'/folder/(name+'.bsf')).read_text()) if n[0]=='symbol')


def box(name,w,h,inputs,outputs):
    node=['symbol',['rect',0,0,w,h],b.txt(name,24,0),b.txt('inst',24,h-16,7)]
    for direction,ports in [('input',inputs),('output',outputs)]:
        for pname,(x,y) in ports.items():
            if x==0: end=(16,y); tx,ty=20,y-14
            elif x==w: end=(w-16,y); tx,ty=w-24-len(pname)*7,y-14
            elif y==0: end=(x,16); tx,ty=x+6,16
            else: end=(x,h-16);tx,ty=x+6,h-32
            node.append(['port',['pt',x,y],[direction],b.txt(pname,tx,ty),b.line((x,y),end)])
    node.append(['drawing',*[b.line(a,c) for a,c in zip([(16,16),(w-16,16),(w-16,h-16),(16,h-16)],[(w-16,16),(w-16,h-16),(16,h-16),(16,16)])]])
    b.SYMS[name]=node


def named(s,kind,x,y,name,nets):
    ports=s.instance(kind,x,y,name)
    rect=next(n for n in b.SYMS[kind] if isinstance(n,list) and n[0]=='rect')
    w,h=int(rect[3])-int(rect[1]),int(rect[4])-int(rect[2])
    for pname,net in nets.items():
        a=ports[pname]
        if a[0]==x: end=(a[0]-136,a[1])
        elif a[0]==x+w: end=(a[0]+136,a[1])
        elif a[1]==y: end=(a[0],a[1]-32)
        else: end=(a[0],a[1]+32)
        s.wire([end,a],net,'..' in net,label=True)
    return ports


def io(s,inputs,outputs):
    for i,p in enumerate(inputs):
        pt=s.pin(p,'input',200,128+40*i)
        s.wire([pt,(320,pt[1])],p,'..' in p)
    for i,p in enumerate(outputs):
        pt=s.pin(p,'output',768,128+40*i)
        s.wire([(656,pt[1]),pt],p,'..' in p)


def symbols():
    for width in [12,16]:
        box(f'counter{width}',256,224,{'CLK':(0,64),'CLR':(0,96),'LD':(0,128),'INC':(0,160),f'DIN[{width-1}..0]':(128,224)}, {f'Q[{width-1}..0]':(128,0)})
    for width in [8,16]:
        box(f'register{width}',256,160,{'CLK':(0,64),'LD':(0,96),f'DIN[{width-1}..0]':(128,160)}, {f'Q[{width-1}..0]':(128,0)})
    box('bus16_mux8',320,384,{**{f'D{i}[15..0]':(0,32*(i+1)) for i in range(8)},'SEL[2..0]':(160,384)}, {'Y[15..0]':(320,176)})
    box('memory4096x16',384,256,{'ADDRESS[11..0]':(0,64),'CLK':(0,128),'READ_EN':(0,160),'WRITE_EN':(0,192),'DATA[15..0]':(192,256)}, {'Q[15..0]':(192,0)})
    box('alu16',512,320,{'DR[15..0]':(96,0),'AC[15..0]':(288,0),'INPR[7..0]':(0,128),'E':(0,160),'OP[6..0]':(0,224)}, {'Y[15..0]':(256,320),'CARRY_OUT':(512,256)})
    box('alu_slice',256,320,{'AC':(0,32),'DR':(0,64),'INPR':(0,96),'RIGHT_BIT':(0,128),'LEFT_BIT':(0,160),'CIN':(0,192),'OP[6..0]':(0,224)}, {'Y':(256,64),'COUT':(256,128)})
    box('state_bit',208,160,{'CLK':(0,32),'CLR':(0,64),'LD':(0,96),'DIN':(104,160)}, {'Q':(104,0)})
    box('extend_next',320,240,{'E':(0,32),'AC0':(0,64),'AC15':(0,96),'CARRY':(0,128),'OP[6..0]':(0,160),'COM':(0,192)}, {'Y':(320,96)})
    box('zext12',256,64,{'A[11..0]':(128,64)}, {'Y[15..0]':(128,0)})
    box('zero16',64,64,{}, {'Y[15..0]':(64,32)})


def alu_slice():
    s=b.Sheet('alu_slice','ALU bit slice - lecture sum-of-products structure',
              'OP bits 0..6 = AND, ADD, DR, INPR, COM, SHR, SHL. Assert at most one operation.')
    io(s,['AC','DR','INPR','RIGHT_BIT','LEFT_BIT','CIN','OP[6..0]'],['Y','COUT'])
    named(s,'xor',448,512,'add_xor_ab',{'IN1':'AC','IN2':'DR','OUT':'AB_XOR'})
    named(s,'xor',896,512,'add_sum',{'IN1':'AB_XOR','IN2':'CIN','OUT':'SUM'})
    named(s,'and2',448,656,'add_carry_ab',{'IN1':'AC','IN2':'DR','OUT':'AB_AND'})
    named(s,'and2',896,656,'add_carry_cin',{'IN1':'AB_XOR','IN2':'CIN','OUT':'CIN_AND'})
    named(s,'or2',1344,656,'add_carry_or',{'IN1':'AB_AND','IN2':'CIN_AND','OUT':'COUT'})
    named(s,'not',448,800,'complement',{'IN':'AC','OUT':'NOT_AC'})
    terms=['AB_AND','SUM','DR','INPR','NOT_AC','RIGHT_BIT','LEFT_BIT']
    for i,term in enumerate(terms):
        named(s,'and2',448+(i%4)*448,1008+(i//4)*176,f'op_gate_{i}',{'IN1':term,'IN2':f'OP[{i}]','OUT':f'TERM_{i}'})
    named(s,'gnd',1664,800,'logic_zero',{'1':'ZERO'})
    named(s,'or8',896,1488,'combine_operations',{**{f'IN{i+1}':f'TERM_{i}' for i in range(7)},'IN8':'ZERO','OUT':'Y'})
    s.save()


def alu_word():
    s=b.Sheet('alu16','16-bit ALU - shared one-hot operation controls',
              'AC/DR addition starts with carry-in 0. SHR/SHL rotate through E; INPR is zero-extended.')
    io(s,['AC[15..0]','DR[15..0]','INPR[7..0]','E','OP[6..0]'],['Y[15..0]','CARRY_OUT'])
    named(s,'gnd',1056,192,'zero_source',{'1':'ZERO'})
    for bit in range(16):
        named(s,'alu_slice',480+(bit%4)*640,480+(bit//4)*416,f'bit_{bit:02}',{
            'AC':f'AC[{bit}]','DR':f'DR[{bit}]','INPR':f'INPR[{bit}]' if bit<8 else 'ZERO',
            'RIGHT_BIT':f'AC[{bit+1}]' if bit<15 else 'E','LEFT_BIT':f'AC[{bit-1}]' if bit else 'E',
            'CIN':f'CARRY_{bit}' if bit else 'ZERO','OP[6..0]':'OP[6..0]',
            'Y':f'Y[{bit}]','COUT':f'CARRY_{bit+1}' if bit<15 else 'CARRY_OUT'})
    s.save()


def state_bit():
    s=b.Sheet('state_bit','Synchronous one-bit state register','Priority: CLR > LD > hold. Common CLK; asynchronous preset and clear are inactive.')
    io(s,['CLK','CLR','LD','DIN'],['Q'])
    mux=s.instance('21mux',448,384,'load_or_hold')
    nc=s.instance('not',448,608,'invert_clear')
    gate=s.instance('and2',816,408,'synchronous_clear')
    ff=s.instance('dff',1120,408,'storage')
    s.wire([(320,248),(352,248),(352,440),mux['A']],'DIN')
    s.wire([ff['Q'],(1344,432),(1344,560),(384,560),(384,408),mux['B']],'Q')
    s.wire([(320,208),(368,208),(368,512),(496,512),mux['S']],'LD')
    s.wire([mux['Y'],gate['IN1']],'SELECTED')
    s.wire([(320,168),(336,168),(336,624),nc['IN']],'CLR')
    s.wire([nc['OUT'],(736,624),(736,440),gate['IN2']],'NOT_CLR')
    s.wire([gate['OUT'],ff['D']],'NEXT_Q')
    s.wire([(320,128),(352,128),(352,80),(1056,80),(1056,448),ff['CLK']],'CLK')
    # Output pin Q and its connected feedback line share the same named net.
    b.dff_supply(s,ff,408,1280,'state')
    s.save()


def extend_next():
    s=b.Sheet('extend_next','Extend-bit next-state selector','ADD: carry; SHR: old AC[0]; SHL: old AC[15]; COM: invert E; otherwise hold E.')
    io(s,['E','AC0','AC15','CARRY','OP[6..0]','COM'],['Y'])
    named(s,'not',448,480,'complement_e',{'IN':'E','OUT':'NOT_E'})
    for i,(a,sel,net) in enumerate([('CARRY','OP[1]','AFTER_ADD'),('AC0','OP[5]','AFTER_SHR'),('AC15','OP[6]','AFTER_SHL'),('NOT_E','COM','Y')]):
        previous='E' if i==0 else ['AFTER_ADD','AFTER_SHR','AFTER_SHL'][i-1]
        named(s,'21mux',448+i*416,688,f'choose_{i}',{'A':a,'B':previous,'S':sel,'Y':net})
    s.save()


def adapters():
    s=b.Sheet('zext12','12-to-16-bit zero extension','Low 12 bits pass through; upper four bits are zero.')
    io(s,['A[11..0]'],['Y[15..0]'])
    for bit in range(16):
        if bit<12:
            named(s,'wire',448+(bit%4)*384,320+(bit//4)*112,f'pass_bit_{bit}',{'IN':f'A[{bit}]','OUT':f'Y[{bit}]'})
        else:
            named(s,'gnd',448+(bit%4)*384,320+(bit//4)*112,f'zero_bit_{bit}',{'1':f'Y[{bit}]'})
    s.save()
    s=b.Sheet('zero16','16-bit constant zero','BUS selection 000 is the unused / zero input.')
    io(s,[],['Y[15..0]'])
    for bit in range(16):
        named(s,'gnd',448+(bit%4)*384,320+(bit//4)*112,f'zero_bit_{bit}',{'1':f'Y[{bit}]'})
    s.save()


def memory():
    (ROOT/'memory4096x16.vhd').write_text('''library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity memory4096x16 is
    port (
        CLK : in std_logic;
        READ_EN, WRITE_EN : in std_logic;
        ADDRESS : in std_logic_vector(11 downto 0);
        DATA : in std_logic_vector(15 downto 0);
        Q : out std_logic_vector(15 downto 0)
    );
end entity;

architecture rtl of memory4096x16 is
    type memory_array is array (0 to 4095) of std_logic_vector(15 downto 0);
    signal ram : memory_array;
begin
    -- Basic-computer memory interface: synchronous write, combinational read.
    -- No program image is assumed; initialize RAM explicitly before execution.
    process (CLK)
    begin
        if rising_edge(CLK) then
            if WRITE_EN = '1' then
                ram(to_integer(unsigned(ADDRESS))) <= DATA;
            end if;
        end if;
    end process;
    Q <= ram(to_integer(unsigned(ADDRESS))) when READ_EN = '1'
         else (others => '0');
end architecture;
''')


def top():
    s=b.Sheet('datapath','Basic Computer Datapath - ENGI 9861 Assignment 2',
              'Existing Part A components are reused. Solid buses show data paths; named control taps connect to the control inputs at lower left.')
    mux=s.instance('bus16_mux8',384,512,'COMMON_BUS')
    zero=s.instance('zero16',32,512,'BUS_ZERO')
    s.wire([zero['Y[15..0]'],mux['D0[15..0]']],'CONST_ZERO[15..0]',True)
    select=s.pin('BUS_SEL[2..0]','input',200,1024)
    s.wire([select,(544,1024),mux['SEL[2..0]']],'BUS_SEL[2..0]',True)
    s.text('BUS sources: 0=0  1=AR  2=PC  3=DR  4=AC  5=IR  6=TR  7=Memory',960,112,12)
    s.text('All registers and state bits use the same rising-edge CLK.',960,152,10)
    s.text('ALU_OP[6..0] is one-hot: bit0 AND, bit1 ADD, bit2 DR, bit3 INPR, bit4 COM, bit5 SHR, bit6 SHL.',960,192,10)
    s.text('CLR / LD / INC are the active-high Part A controls; CLR > LD > INC.',960,232,10)
    cells={}
    configs=[('AR','counter12',960),('PC','counter12',1376),('DR','counter16',1792),
             ('AC','counter16',2208),('IR','register16',2624),('TR','counter16',3040)]
    ld_indices={'AR':0,'PC':1,'DR':2,'AC':3,'IR':4,'TR':5}
    inc_indices={'AR':0,'PC':1,'DR':2,'AC':3,'TR':4}
    clk=s.pin('CLK','input',200,1120)
    s.wire([clk,(4032,1120),(4032,2416),(896,2416)],'CLK')
    # Lower horizontal CLK rail serves the state registers.
    s.wire([mux['Y[15..0]'],(816,688),(816,1776),(3776,1776)],'BUS_DATA[15..0]',True,label=True)
    s.pin('BUS_DATA[15..0]','output',3776,1776)
    for name,kind,x in configs:
        p=s.instance(kind,x,1200,name)
        cells[name]=p
        s.wire([(x-32,1120),(x-32,1264),p['CLK']],'CLK');s.junction((x-32,1120))
        for port,index in [('LD',ld_indices[name]),('CLR',inc_indices.get(name)),('INC',inc_indices.get(name))]:
            if port in p:
                net=f'REG_{port}[{index}]'
                a=p[port];s.wire([(a[0]-112,a[1]),a],net,label=True)
        if name!='AC':
            width=12 if kind=='counter12' else 16
            a=p[f'DIN[{width-1}..0]']
            s.wire([(a[0],1776),a],f'BUS_DATA[{width-1}..0]',True,label=True)
        s.text(name,x+100,1152,14)
    # Reusable zero-extension adapters on the two 12-bit BUS sources.
    for name,x in [('AR',960),('PC',1376)]:
        p=s.instance('zext12',x,928,f'{name}_ZERO_EXTEND')
        s.wire([cells[name]['Q[11..0]'],p['A[11..0]']],f'{name}_Q[11..0]',True)
        cells[name+'_EXT']=p
    mem=s.instance('memory4096x16',3360,768,'MEMORY_4096x16')
    s.wire([(1088,1152),(3296,1152),(3296,832),mem['ADDRESS[11..0]']],'AR_Q[11..0]',True,label=True)
    s.junction((1088,1152))
    s.wire([(3328,1120),(3328,896),mem['CLK']],'CLK');s.junction((3328,1120))
    for port in ['READ_EN','WRITE_EN']:
        a=mem[port];s.wire([(a[0]-112,a[1]),a],'MEM_'+port,label=True)
    s.wire([(3552,1776),mem['DATA[15..0]']],'BUS_DATA[15..0]',True,label=True)
    s.text('Memory address comes from AR; writes take BUS data.',3200,688,10)
    sources=[(cells['AR_EXT']['Y[15..0]'],'AR_EXT',288),
             (cells['PC_EXT']['Y[15..0]'],'PC_EXT',320),
             (cells['DR']['Q[15..0]'],'DR_Q',352),
             (cells['AC']['Q[15..0]'],'AC_Q',384),
             (cells['IR']['Q[15..0]'],'IR_Q',416),
             (cells['TR']['Q[15..0]'],'TR_Q',448),
             (mem['Q[15..0]'],'MEM_Q',480)]
    for slot,(a,net,y) in enumerate(sources,1):
        x=128+24*slot
        if slot==4:
            route=[a,(a[0],1136),(2672,1136),(2672,y),(x,y),(x,544+slot*32),mux[f'D{slot}[15..0]']]
        else:
            route=[a,(a[0],y),(x,y),(x,544+slot*32),mux[f'D{slot}[15..0]']]
        s.wire(route,net+'[15..0]',True,label=True)
    alu=s.instance('alu16',2080,688,'ALU')
    s.wire([(1920,608),(2176,608),alu['DR[15..0]']],'DR_Q[15..0]',True,label=True);s.junction((1920,608))
    s.wire([(2672,640),(2368,640),alu['AC[15..0]']],'AC_Q[15..0]',True,label=True);s.junction((2672,640))
    s.wire([alu['Y[15..0]'],(2528,1008),(2528,1504),(2336,1504),cells['AC']['DIN[15..0]']],'ALU_RESULT[15..0]',True,label=True)
    a=alu['OP[6..0]'];s.wire([(a[0]-112,a[1]),a],'ALU_OP[6..0]',True,label=True)
    a=alu['CARRY_OUT'];s.wire([a,(a[0]+112,a[1])],'ALU_CARRY',label=True)
    inpr=s.instance('register8',1792,1920,'INPR')
    outr=s.instance('register8',2624,1920,'OUTR')
    for name,p,x,idx in [('INPR',inpr,1792,6),('OUTR',outr,2624,7)]:
        s.text(name,x+96,1872,14)
        s.wire([(x-32,1120),(x-32,1984),p['CLK']],'CLK');s.junction((x-32,1120))
        a=p['LD'];s.wire([(a[0]-112,a[1]),a],f'REG_LD[{idx}]',label=True)
    inp=s.pin('INPUT_DATA[7..0]','input',200,2144)
    s.wire([inp,(1920,2144),inpr['DIN[7..0]']],'INPUT_DATA[7..0]',True)
    s.wire([inpr['Q[7..0]'],(1856,1920),(1856,816),alu['INPR[7..0]']],'INPR_Q[7..0]',True,label=True)
    s.wire([(2960,1776),(2960,2144),(2752,2144),outr['DIN[7..0]']],'BUS_DATA[7..0]',True,label=True)
    s.wire([outr['Q[7..0]'],(2752,1824),(3200,1824)],'OUTPUT_DATA[7..0]',True,label=True)
    s.pin('OUTPUT_DATA[7..0]','output',3200,1824)
    # External controller interface. Named scalar taps avoid obscuring the data buses.
    controls=['REG_LD[7..0]','REG_INC[4..0]','REG_CLR[4..0]','ALU_OP[6..0]',
              'MEM_READ_EN','MEM_WRITE_EN','FLAG_LD[6..0]','FLAG_CLR[6..0]','FLAG_DIN[4..0]','E_COM']
    for i,p in enumerate(controls):
        a=s.pin(p,'input',200,1856+i*24)
        s.wire([a,(416,a[1])],p,'..' in p)
    s.text('CONTROL INPUTS (connect next assignment control unit here)',32,1800,10)
    s.text('REG_LD: [0] AR  [1] PC  [2] DR  [3] AC  [4] IR  [5] TR  [6] INPR  [7] OUTR',960,1632,10)
    s.text('REG_CLR / REG_INC: [0] AR  [1] PC  [2] DR  [3] AC  [4] TR',960,1664,10)
    s.text('BUS_DATA -> AR/PC low 12 bits; -> OUTR low 8 bits. AR/PC sources are zero-extended.',960,1696,10)
    # State / status FFs, including the optional S.
    flagbus=s.pin('FLAG_Q[6..0]','output',3776,2352)
    s.wire([(896,2352),flagbus],'FLAG_Q[6..0]',True,label=True)
    flags={}
    for i,name in enumerate(['E','I','R','IEN','FGI','FGO','S']):
        x=960+i*384;p=s.instance('state_bit',x,2464,name);flags[name]=p
        s.text(name+' (optional)' if name=='S' else name,x+80,2432,12)
        s.wire([(x-32,2416),(x-32,2496),p['CLK']],'CLK');s.junction((x-32,2416))
        for port in ['CLR','LD']:
            a=p[port];s.wire([(a[0]-112,a[1]),a],f'FLAG_{port}[{i}]',label=True)
        s.wire([p['Q'],(p['Q'][0],2352)],f'FLAG_Q[{i}]',label=True)
        if i>=2:
            a=p['DIN'];s.wire([(a[0],a[1]+32),a],f'FLAG_DIN[{i-2}]',label=True)
    s.wire([flags['E']['Q'],(1064,2384),(864,2384),(864,848),alu['E']],'FLAG_Q[0]',label=True)
    s.junction((1064,2384))
    a=flags['I']['DIN'];s.wire([(a[0],a[1]+32),a],'IR_Q[15]',label=True)
    en=named(s,'extend_next',320,2240,'E_NEXT_LOGIC',{'E':'FLAG_Q[0]','AC0':'AC_Q[0]','AC15':'AC_Q[15]','CARRY':'ALU_CARRY','OP[6..0]':'ALU_OP[6..0]','COM':'E_COM'})
    s.wire([en['Y'],(736,2336),(736,2672),(1064,2672),flags['E']['DIN']],'E_NEXT',label=True)
    s.text('FLAG_Q / FLAG_LD / FLAG_CLR: [0] E  [1] I  [2] R  [3] IEN  [4] FGI  [5] FGO  [6] S',960,2768,10)
    s.text('I loads IR[15]. R=0 instruction routine / R=1 interrupt routine. FLAG_DIN[0..4] supplies R, IEN, FGI, FGO, S.',960,2800,10)
    s.text('E_NEXT: ADD carry / SHR AC[0] / SHL AC[15] / complement E. FLAG_LD[0] enables the E update.',960,2832,10)
    s.save()


def build():
    ROOT.mkdir(exist_ok=True)
    symbols();alu_slice();alu_word();state_bit();extend_next();adapters();memory();top()
    for name in [*NEW[1:],'memory4096x16']:
        (ROOT/(name+'.bsf')).write_text('(header "symbol" (version "1.1"))\n'+b.emit(b.SYMS[name])+'\n')
    qsf=['set_global_assignment -name FAMILY "Cyclone V"',
         'set_global_assignment -name DEVICE 5CGXFC7C7F23C8',
         'set_global_assignment -name TOP_LEVEL_ENTITY datapath',
         'set_global_assignment -name ORIGINAL_QUARTUS_VERSION 20.1.0',
         'set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files',
         'set_global_assignment -name SEARCH_PATH .',
         'set_global_assignment -name NUM_PARALLEL_PROCESSORS 2']
    qsf += [f'set_global_assignment -name BDF_FILE {name}.bdf' for name in [*b.TOPS,'priority_control',*NEW]]
    qsf += ['set_global_assignment -name VHDL_FILE memory4096x16.vhd']
    (ROOT/'datapath.qsf').write_text('\n'.join(qsf)+'\n')
    print('Created datapath, reusable ALU / state logic, and 4096x16 memory.')


if __name__=='__main__':
    build()
