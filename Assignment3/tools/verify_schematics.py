"""Functional checks of the actual BDF connectivity, using Boolean gate evaluation.

This is a synchronous, zero-delay logic check, not a Quartus/ModelSim waveform run.
"""
import json
import random
import re
from pathlib import Path
from build_schematics import parse

ROOT = Path(__file__).resolve().parents[1]


def child(node, kind):
    return next(x for x in node if isinstance(x,list) and x[0] == kind)


def label(node, index=0):
    return json.loads([x for x in node if isinstance(x,list) and x[0]=='text'][index][1])


def expand(net):
    match = re.fullmatch(r'(.*)\[(\d+)\.\.(\d+)\]',net)
    if not match:
        return [net]
    base,hi,lo = match.groups()
    assert int(hi) >= int(lo)
    return [f'{base}[{i}]' for i in range(int(lo),int(hi)+1)]


class Circuit:
    def __init__(self,top):
        self.drivers, self.ffs, self.state = {}, {}, {}
        self.flatten(top,'',{})
        self.state = {q:0 for q in self.ffs}

    def flatten(self,name,prefix,bindings):
        nodes = parse((ROOT/(name+'.bdf')).read_text())
        connections = {}
        for node in nodes:
            if node[0]=='connector':
                net = label(node)
                for p in [x for x in node if isinstance(x,list) and x[0]=='pt']:
                    xy = tuple(map(int,p[1:]))
                    connections.setdefault(xy,set()).add(net)

        def resolve(net):
            return [bindings.get(n,prefix+n) for n in expand(net)]

        for node in nodes:
            if node[0]!='symbol':
                continue
            kind,inst = label(node).lower(),label(node,1)
            rect = list(map(int,child(node,'rect')[1:]))
            ports = {}
            for p in [x for x in node if isinstance(x,list) and x[0]=='port']:
                point = list(map(int,child(p,'pt')[1:]))
                contact = (rect[0]+point[0],rect[1]+point[1])
                if contact not in connections:
                    assert kind=='81mux' and label(p)=='WN', (kind,label(p),contact)
                    continue  # Unused complementary output.
                candidates = connections[contact]
                scalar = [n for n in candidates if len(expand(n))==1]
                assert len(scalar)<=1, (name,contact,candidates)
                net = scalar[0] if scalar else next(iter(candidates))
                formal,actual = expand(label(p)),resolve(net)
                assert len(formal)==len(actual),(kind,formal,actual)
                ports.update(zip(formal,actual))
            if (ROOT/(kind+'.bdf')).exists():
                self.flatten(kind,prefix+inst+'/',ports)
            elif kind=='dff':
                q = ports['Q']
                assert q not in self.drivers
                self.drivers[q] = ('state',q)
                self.ffs[q] = ports
            elif kind in ['vcc','gnd']:
                self.drivers[ports['1']] = (kind,{})
            elif kind in ['21mux','mux41','81mux']:
                output = ports['Q'] if kind=='mux41' else ports['Y']
                assert output not in self.drivers
                self.drivers[output] = (kind,ports)
            else:
                assert kind in ['not','and2','or2','xor'],kind
                q = ports['OUT']
                assert q not in self.drivers
                self.drivers[q] = (kind,ports)

    def evaluate(self,inputs,tick=False):
        values = {'CLK':0}
        for net,value in inputs.items():
            for i,bit in enumerate(expand(net)):
                values[bit] = (value >> i)&1

        def read(net):
            if net in values:
                return values[net]
            kind,ports = self.drivers[net]
            if kind=='state':
                value = self.state[ports]
            elif kind=='vcc':
                value = 1
            elif kind=='gnd':
                value = 0
            elif kind=='21mux':
                value = read(ports['A' if read(ports['S']) else 'B'])
            elif kind=='mux41':
                select = 2*read(ports['S1'])+read(ports['S0'])
                value = 0 if read(ports['INH']) else read(ports[f'D{select}'])
            elif kind=='81mux':
                select = read(ports['A'])+2*read(ports['B'])+4*read(ports['C'])
                value = 0 if read(ports['GN']) else read(ports[f'D{select}'])
            elif kind=='not':
                value = 1-read(ports['IN'])
            else:
                a,b = read(ports['IN1']),read(ports['IN2'])
                value = a&b if kind=='and2' else a|b if kind=='or2' else a^b
            values[net] = value
            return value

        if tick:
            for ports in self.ffs.values():
                assert ports['CLK']=='CLK'
                assert read(ports['CLRN'])==read(ports['PRN'])==1
            self.state = {q:read(ports['D']) for q,ports in self.ffs.items()}
            return self.evaluate(inputs)
        self.read = read
        return self

    def word(self,name,width):
        return sum(self.read(f'{name}[{i}]') << i for i in range(width))


def main():
    rng = random.Random(9861)
    report = []
    for width in [16,12]:
        c = Circuit(f'counter{width}')
        mask = (1 << width)-1
        count = 0
        for initial in [0,1,mask,mask-1,mask//2]+[rng.randrange(mask+1) for _ in range(80)]:
            for controls in range(8):
                c.evaluate({'LD':1,'CLR':0,'INC':0,f'DIN[{width-1}..0]':initial},True)
                assert c.word('Q',width)==initial
                clr,ld,inc = (controls>>2)&1,(controls>>1)&1,controls&1
                data = rng.randrange(mask+1)
                inputs = {'CLR':clr,'LD':ld,'INC':inc,f'DIN[{width-1}..0]':data}
                c.evaluate(inputs)
                assert c.word('Q',width)==initial, 'Changed without a clock edge'
                c.evaluate(inputs,True)
                expected = 0 if clr else data if ld else (initial+1)&mask if inc else initial
                assert c.word('Q',width)==expected,(width,initial,controls,data)
                count += 1
        c.evaluate({'CLR':1,'LD':0,'INC':0,f'DIN[{width-1}..0]':0},True)
        for expected in range(1,513):
            c.evaluate({'CLR':0,'LD':0,'INC':1,f'DIN[{width-1}..0]':0},True)
            assert c.word('Q',width)==expected
        report.append(f'PASS counter{width}: {count} priority/hold/overflow cases and 512 consecutive increments; {len(c.ffs)} DFFs')

    for width in [8,16]:
        c = Circuit(f'register{width}')
        expected = 0
        for _ in range(512):
            data,load = rng.randrange(1 << width),rng.randrange(2)
            inputs = {'LD':load,f'DIN[{width-1}..0]':data}
            c.evaluate(inputs)
            assert c.word('Q',width)==expected
            c.evaluate(inputs,True)
            expected = data if load else expected
            assert c.word('Q',width)==expected
        report.append(f'PASS register{width}: 512 load/hold/no-edge cases; {len(c.ffs)} DFFs')

    c = Circuit('bus16_mux8')
    count = 0
    patterns = [[(0x1111*i)&65535 for i in range(8)]]
    patterns += [[(1 << bit) if i==source else 0 for i in range(8)]
                 for source in range(8) for bit in range(16)]
    patterns += [[rng.randrange(65536) for _ in range(8)] for _ in range(80)]
    for words in patterns:
        for sel in range(8):
            inputs = {f'D{i}[15..0]':word for i,word in enumerate(words)}
            inputs['SEL[2..0]'] = sel
            c.evaluate(inputs)
            assert c.word('Y',16)==words[sel]
            count += 1
    assert not c.ffs
    report.append(f'PASS bus16_mux8: {count} cases, all 8 selectors, every input bit isolated, and random words; purely combinational')
    output = '\n'.join(report)+'\n'
    print(output)
    (ROOT/'verification').mkdir(exist_ok=True)
    (ROOT/'verification/logic_checks.txt').write_text(output)


if __name__=='__main__':
    main()
