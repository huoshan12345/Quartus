"""Create Part A schematics at the lecture's MUX/flip-flop abstraction level."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
LIB = Path(r'C:\intelFPGA_lite\20.1\quartus\libraries')
TOPS = ['counter16', 'counter12', 'register8', 'register16', 'bus16_mux8']


def parse(source):
    source = re.sub(r'/\*.*?\*/|//[^\n]*', '', source, flags=re.S)
    stack, result = [], []
    for token in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', source):
        if token == '(':
            node = []
            (stack[-1] if stack else result).append(node)
            stack.append(node)
        elif token == ')':
            stack.pop()
        else:
            stack[-1].append(token)
    assert not stack
    return result


def emit(node):
    return '('+' '.join(emit(n) for n in node)+')' if isinstance(node,list) else str(node)


def txt(value,x,y,size=8,visible=True):
    node = ['text',json.dumps(value),['rect',x,y,x+max(16,len(value)*7),y+18],
            ['font','"Arial"',['font_size',size]]]
    if not visible:
        node.append(['invisible'])
    return node


def line(a,b):
    return ['line',['pt',*a],['pt',*b],['line_width',1]]


SYMS = {}
for name,folder in [('and2','logic'),('or2','logic'),('not','logic'),('xor','logic'),
                    ('dff','storage'),('vcc','other'),('gnd','other')]:
    SYMS[name] = next(n for n in parse((LIB/'primitives'/folder/(name+'.bsf')).read_text()) if n[0]=='symbol')


def symbol(name,width,height,inputs,outputs,outline=None):
    node = ['symbol',['rect',0,0,width,height],txt(name,24,0),txt('inst',24,height-16,7)]
    for direction,ports in [('input',inputs),('output',outputs)]:
        for pname,(x,y) in ports.items():
            if x==0:
                end=(16,y); t=(20,y-13)
            elif x==width:
                end=(width-16,y); t=(width-22-len(pname)*7,y-13)
            else:
                end=(x,y-16); t=(x-8,y-32)
            node.append(['port',['pt',x,y],[direction],txt(pname,*t),line((x,y),end)])
    outline = outline or [(16,16),(width-16,16),(width-16,height-16),(16,height-16),(16,16)]
    node.append(['drawing',*[line(a,b) for a,b in zip(outline,outline[1:])]])
    SYMS[name]=node


# These names resolve to Quartus's elementary multiplexer functions. Only their
# symbol drawings are restyled; no counter/register IP is used.
# Quartus 21mux is Y = S*A + NOT(S)*B. Feedback must be B; DIN must be A.
symbol('21mux',96,96,{'B':(0,24),'A':(0,56),'S':(48,96)}, {'Y':(96,40)},
       [(16,8),(80,24),(80,72),(16,88),(16,8)])
symbol('mux41',128,192,{'D0':(0,32),'D1':(0,64),'D2':(0,96),'D3':(0,128),
       'INH':(0,152),'S1':(48,192),'S0':(80,192)}, {'Q':(128,80)},
       [(16,8),(112,40),(112,168),(16,184),(16,8)])
symbol('81mux',128,336,{**{f'D{k}':(0,32*(k+1)) for k in range(8)},
       'GN':(0,288),'A':(32,336),'B':(64,336),'C':(96,336)},
       {'Y':(128,144),'WN':(128,176)},
       [(16,8),(112,40),(112,304),(16,328),(16,8)])
symbol('priority_control',208,144,{'CLR':(0,32),'LD':(0,64),'INC':(0,96)},
       {'S0':(208,32),'S1':(208,64)})


class Sheet:
    def __init__(self,name,title,note):
        self.name=name
        self.nodes=[['header','"graphic"',['version','"1.4"']],txt(title,32,24,14),txt(note,32,56)]
        self.instances={}
        self.junctions=set()

    def text(self,value,x,y,size=8):
        self.nodes.append(txt(value,x,y,size))

    def wire(self,points,net,bus=False,label=False):
        for i,(a,b) in enumerate(zip(points,points[1:])):
            if a==b:
                continue
            assert a[0]==b[0] or a[1]==b[1],(net,a,b)
            node=['connector',txt(net,min(a[0],b[0])+4,min(a[1],b[1])-17,visible=label and i==0),
                  ['pt',*a],['pt',*b]]
            if bus:
                node.append(['bus'])
            self.nodes.append(node)

    def junction(self,point):
        if point not in self.junctions:
            self.nodes.append(['junction',['pt',*point]])
            self.junctions.add(point)

    def pin(self,name,direction,x,y):
        incoming=direction=='input'
        left=x-168 if incoming else x
        node=['pin',[direction],['rect',left,y-8,left+(168 if incoming else 176),y+8],
              txt(direction.upper(),133 if incoming else 1,0,6),
              txt(name,5 if incoming else 90,0),['pt',168 if incoming else 0,8]]
        segments=[(92,4,117,4),(92,12,117,12),(92,4,92,12),(117,4,121,8),(117,12,121,8),(121,8,168,8)] if incoming else [
            (0,8,52,8),(52,4,78,4),(52,12,78,12),(52,4,52,12),(78,4,82,8),(78,12,82,8)]
        node.append(['drawing',*[line((a,b),(c,d)) for a,b,c,d in segments]])
        if incoming:
            node.append(txt('VCC',136,7,6))
        self.nodes.append(node)
        return (x,y)

    def instance(self,kind,x,y,name):
        node=parse(emit(SYMS[kind]))[0]
        rect=next(n for n in node if isinstance(n,list) and n[0]=='rect')
        width,height=int(rect[3])-int(rect[1]),int(rect[4])-int(rect[2])
        rect[:]=['rect',x,y,x+width,y+height]
        titles=[n for n in node if isinstance(n,list) and n[0]=='text']
        r=next(n for n in titles[1] if isinstance(n,list) and n[0]=='rect')
        titles[1][:]=txt(name,int(r[1]),int(r[2]),7)
        if kind in ['21mux','mux41','81mux']:
            titles[1][:]=txt(name,16,height+2,7)
        elif kind in ['vcc','gnd']:
            titles[1].append(['invisible'])
        self.nodes.append(node)
        ports={}
        for p in [n for n in node if isinstance(n,list) and n[0]=='port']:
            pt=next(n for n in p if n[0]=='pt')
            pname=json.loads(next(n for n in p if n[0]=='text')[1])
            ports[pname]=(x+int(pt[1]),y+int(pt[2]))
        self.instances[name]=(kind,ports)
        return ports

    def save(self):
        (ROOT/(self.name+'.bdf')).write_text('\n'.join(emit(n) for n in self.nodes)+'\n')


def dff_supply(s,ff,row,x,bit):
    net=f'VCC_{bit}'
    source=s.instance('vcc',x-16,row-16,f'supply_high_{bit}')['1']
    s.wire([source,(x,ff['PRN'][1]),ff['PRN']],net)
    s.wire([(x,ff['PRN'][1]),(x,ff['CLRN'][1]+16),
            (ff['CLRN'][0],ff['CLRN'][1]+16),ff['CLRN']],net)
    s.junction((x,ff['PRN'][1]))


def build_priority():
    s=Sheet('priority_control','Shared counter priority encoder',
            'CLR > LD > INC > hold. Select codes: clear=00; load=01; increment=10; hold=11.')
    clr=s.pin('CLR','input',200,160)
    ld=s.pin('LD','input',200,320)
    inc=s.pin('INC','input',200,512)
    s0=s.pin('S0','output',1248,480)
    s1=s.pin('S1','output',1248,224)
    nc=s.instance('not',352,144,'invert_clr')
    nl=s.instance('not',352,304,'invert_ld')
    ni=s.instance('not',352,496,'invert_inc')
    term=s.instance('or2',688,400,'load_or_not_inc')
    gate1=s.instance('and2',1008,200,'select_bit1')
    gate0=s.instance('and2',1008,456,'select_bit0')
    s.wire([clr,nc['IN']],'CLR')
    s.wire([ld,(288,320),nl['IN']],'LD')
    s.wire([(288,320),(288,416),term['IN1']],'LD');s.junction((288,320))
    s.wire([inc,ni['IN']],'INC')
    s.wire([nc['OUT'],(560,160),(560,216),gate1['IN1']],'NCLR')
    s.wire([(560,216),(560,472),gate0['IN1']],'NCLR');s.junction((560,216))
    s.wire([nl['OUT'],(608,320),(608,232),gate1['IN2']],'NLD')
    s.wire([ni['OUT'],(608,512),(608,432),term['IN2']],'NINC')
    s.wire([term['OUT'],(896,424),(896,488),gate0['IN2']],'LOAD_OR_NINC')
    s.wire([gate1['OUT'],s1],'S1');s.wire([gate0['OUT'],s0],'S0')
    s.text('S1 = NOT CLR AND NOT LD',688,600)
    s.text('S0 = NOT CLR AND (LD OR NOT INC)',688,632)
    s.save()


def build_register(width):
    s=Sheet(f'register{width}',f'{width}-bit parallel-load register',
            'LD=0: feedback / hold. LD=1: load DIN. Common rising-edge CLK; no clock gating.')
    end=320+(width-1)*176
    din=s.pin(f'DIN[{width-1}..0]','input',200,144)
    ld=s.pin('LD','input',200,192)
    clk=s.pin('CLK','input',200,240)
    q=s.pin(f'Q[{width-1}..0]','output',1152,144)
    s.wire([din,(256,144),(256,end+56)],f'DIN[{width-1}..0]',True)
    s.wire([ld,(384,192),(384,end+152)],'LD')
    s.wire([clk,(800,240),(800,end+56)],'CLK')
    s.wire([q,(1152,end+40)],f'Q[{width-1}..0]',True)
    for bit in range(width):
        row=320+bit*176
        mux=s.instance('21mux',512,row,f'load_mux_{bit:02}')
        ff=s.instance('dff',896,row+16,f'dff_{bit:02}')
        s.wire([(256,row+56),mux['A']],f'DIN[{bit}]',label=True)
        s.wire([(384,row+152),(560,row+152),mux['S']],'LD');s.junction((384,row+152))
        s.wire([mux['Y'],ff['D']],f'NEXT_{bit}')
        s.wire([(800,row+56),ff['CLK']],'CLK');s.junction((800,row+56))
        s.wire([ff['Q'],(1056,row+40),(1152,row+40)],f'Q[{bit}]',label=True)
        s.wire([(1056,row+40),(1056,row+128),(448,row+128),(448,row+24),mux['B']],f'Q[{bit}]')
        s.junction((1056,row+40))
        dff_supply(s,ff,row+16,1024,bit)
    s.save()


def build_counter(width):
    s=Sheet(f'counter{width}',f'{width}-bit synchronous counter - lecture structure',
            'Shared priority encoder + one 4:1 MUX / DFF per bit. D0=0, D1=DIN, D2=Q+1, D3=Q.')
    end=512+(width-1)*256
    encoder=s.instance('priority_control',800,112,'priority_encoder')
    for name,y in [('CLR',144),('LD',176),('INC',208)]:
        pin=s.pin(name,'input',200,y)
        s.wire([pin,encoder[name]],name)
    clk=s.pin('CLK','input',200,336)
    din=s.pin(f'DIN[{width-1}..0]','input',200,384)
    q=s.pin(f'Q[{width-1}..0]','output',1408,384)
    s.wire([clk,(1120,336),(1120,end+96)],'CLK')
    s.wire([din,(256,384),(256,end+64)],f'DIN[{width-1}..0]',True)
    s.wire([q,(1408,end+80)],f'Q[{width-1}..0]',True)
    s.wire([encoder['S0'],(1040,144),(1040,256),(512,256),(512,end+240)],'S0',label=True)
    s.wire([encoder['S1'],(1072,176),(1072,288),(544,288),(544,end+224)],'S1',label=True)
    for bit in range(width):
        row=512+bit*256
        mux=s.instance('mux41',816,row,f'action_mux_{bit:02}')
        ff=s.instance('dff',1200,row+56,f'dff_{bit:02}')
        qi=f'Q[{bit}]'
        s.wire([(256,row+64),mux['D1']],f'DIN[{bit}]',label=True)
        s.wire([(544,row+224),(864,row+224),mux['S1']],'S1');s.junction((544,row+224))
        s.wire([(512,row+240),(896,row+240),mux['S0']],'S0');s.junction((512,row+240))
        ground=s.instance('gnd',704,row,f'supply_zero_{bit}')['1']
        s.wire([ground,(736,row),(736,row+32),mux['D0']],f'ZERO_{bit}')
        s.wire([(736,row+32),(736,row+152),mux['INH']],f'ZERO_{bit}');s.junction((736,row+32))
        s.wire([mux['Q'],ff['D']],f'NEXT_{bit}')
        s.wire([(1120,row+96),ff['CLK']],'CLK');s.junction((1120,row+96))
        s.wire([ff['Q'],(1344,row+80),(1408,row+80)],qi,label=True)
        s.wire([(1344,row+80),(1344,row+208),(608,row+208),(608,row+32)],qi)
        s.wire([(608,row+128),mux['D3']],qi)
        s.junction((1344,row+80));s.junction((608,row+128))
        if bit==0:
            toggle=s.instance('not',656,row+80,'invert_bit0')
            s.wire([(608,row+96),toggle['IN']],qi);s.junction((608,row+96))
            s.wire([toggle['OUT'],mux['D2']],f'PLUS1_{bit}')
            carry_start=(608,row+32)
        else:
            carry_in='Q[0]' if bit==1 else f'CARRY_{bit}'
            toggle=s.instance('xor',656,row+72,f'increment_xor_{bit:02}')
            s.wire([(608,row+88),toggle['IN1']],qi);s.junction((608,row+88))
            s.wire([(352,row+16),(352,row+104),toggle['IN2']],carry_in)
            s.junction((352,row+16))
            s.wire([toggle['OUT'],mux['D2']],f'PLUS1_{bit}')
            if bit<width-1:
                carry=s.instance('and2',400,row,f'carry_and_{bit:02}')
                s.wire([(352,row+16),carry['IN1']],carry_in)
                s.wire([(608,row+32),carry['IN2']],qi)
                carry_start=carry['OUT']
        if bit<width-1:
            s.wire([carry_start,(480,carry_start[1]),(480,row+272),(352,row+272)],qi if bit==0 else f'CARRY_{bit+1}',label=True)
        dff_supply(s,ff,row+56,1312,bit)
    s.save()


def build_bus():
    s=Sheet('bus16_mux8','16-bit BUS - sixteen parallel 8:1 multiplexers',
            'SEL[2..0]=k selects Dk[15..0]. Each MUX handles one bit; all share the same selection lines.')
    end=576+15*416
    for k in range(8):
        x=256+32*k
        pin=s.pin(f'D{k}[15..0]','input',200,128+40*k)
        s.wire([pin,(x,128+40*k),(x,end+32*(k+1))],f'D{k}[15..0]',True)
    sel=s.pin('SEL[2..0]','input',200,464)
    s.wire([sel,(608,464),(608,544)],'SEL[2..0]',True)
    for k,x in enumerate([640,688,736]):
        y=496+24*k
        s.wire([(608,y),(x,y),(x,end+360+16*k)],f'SEL[{k}]',label=True)
    out=s.pin('Y[15..0]','output',1216,128)
    s.wire([out,(1216,end+144)],'Y[15..0]',True)
    for bit in range(16):
        row=576+bit*416
        mux=s.instance('81mux',864,row,f'bus_mux_{bit:02}')
        for k in range(8):
            s.wire([(256+32*k,row+32*(k+1)),mux[f'D{k}']],f'D{k}[{bit}]',label=True)
        for k,(x,port) in enumerate([(640,'A'),(688,'B'),(736,'C')]):
            y=row+360+16*k
            s.wire([(x,y),(mux[port][0],y),mux[port]],f'SEL[{k}]')
            s.junction((x,y))
        gnd=s.instance('gnd',800,row+288,f'enable_zero_{bit}')['1']
        s.wire([gnd,mux['GN']],f'ZERO_{bit}')
        s.wire([mux['Y'],(1216,row+144)],f'Y[{bit}]',label=True)
        # The complementary output is intentionally unused.
    s.save()


def component_symbol(name,inputs,outputs):
    h=(max(len(inputs),len(outputs))+1)*32
    symbol(name,240,h,{p:(0,32*(i+1)) for i,p in enumerate(inputs)},
           {p:(240,32*(i+1)) for i,p in enumerate(outputs)})


def build():
    ROOT.mkdir(exist_ok=True)
    build_priority()
    for width in [16,12]:
        build_counter(width)
        component_symbol(f'counter{width}',['CLK','CLR','LD','INC',f'DIN[{width-1}..0]'],[f'Q[{width-1}..0]'])
    for width in [8,16]:
        build_register(width)
        component_symbol(f'register{width}',['CLK','LD',f'DIN[{width-1}..0]'],[f'Q[{width-1}..0]'])
    build_bus()
    component_symbol('bus16_mux8',[f'D{k}[15..0]' for k in range(8)]+['SEL[2..0]'],['Y[15..0]'])
    for name in ['priority_control',*TOPS]:
        (ROOT/(name+'.bsf')).write_text('(header "symbol" (version "1.1"))\n'+emit(SYMS[name])+'\n')
    (ROOT/'assignment2.qpf').write_text('QUARTUS_VERSION = "20.1"\n'+''.join(f'PROJECT_REVISION = "{t}"\n' for t in TOPS))
    for top in TOPS:
        assignments=['set_global_assignment -name FAMILY "Cyclone V"',
            'set_global_assignment -name DEVICE 5CGXFC7C7F23C8',
            f'set_global_assignment -name TOP_LEVEL_ENTITY {top}',
            'set_global_assignment -name ORIGINAL_QUARTUS_VERSION 20.1.0',
            'set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files',
            'set_global_assignment -name SEARCH_PATH .',
            'set_global_assignment -name NUM_PARALLEL_PROCESSORS 2']
        assignments += [f'set_global_assignment -name BDF_FILE {t}.bdf' for t in [*TOPS,'priority_control']]
        (ROOT/(top+'.qsf')).write_text('\n'.join(assignments)+'\n')
    print('Generated five component sheets and one shared priority encoder.')


if __name__=='__main__':
    build()
