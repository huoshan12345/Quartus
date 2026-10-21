"""Generate independent ModelSim checks for the compiled register netlists."""
from pathlib import Path

out=Path(__file__).resolve().parents[1]/'verification/modelsim_mux_fix'
out.mkdir(parents=True,exist_ok=True)
script=['onerror {quit -f -code 1}', 'transcript file native_register_check.log',
        'vmap -c', 'vlib native_check_work', 'vmap work native_check_work']
for width in [8,16]:
    name=f'register{width}'
    mask=(1<<width)-1
    cases=[(1,5,5),(0,9,5),(0,9,5),(1,9,9),(0,12,9),
           (1,12,12),(0,3,12),(0,mask,12),(1,0,0),(0,mask,0),(1,mask,mask),(0,0,mask)]
    for bit in range(width):
        value=1<<bit
        cases.extend([(1,value,value),(0,mask^value,value)])
    script += [f'vcom -93 -work work {name}.vho', f'vsim work.{name}',
               f'log sim:/{name}/*', f'force -freeze sim:/{name}/CLK 0']
    for i,(load,data,expected) in enumerate(cases):
        script += [f'force -freeze sim:/{name}/CLK 0',
                   f'force -freeze sim:/{name}/LD {load}',
                   f'force -freeze sim:/{name}/DIN 2#{data:0{width}b}',
                   'run 50ns', f'force -freeze sim:/{name}/CLK 1','run 50ns',
                   f'set observed [examine -radix unsigned sim:/{name}/Q]',
                   f'if {{$observed != {expected}}} {{puts "FAIL {name} case {i}: LD={load}, DIN={data}, expected {expected}, observed $observed"; quit -f -code 1}}']
    script += [f'puts "PASS {name}: {len(cases)} native gate-netlist load/hold cases, including every data bit"','quit -sim']
script += ['quit -f -code 0']
(out/'check_registers.do').write_text('\n'.join(script)+'\n')
